# -*- coding: utf-8 -*-
import asyncio
import enum
import functools
import io
import itertools
import json
import logging
import os
import pickle
import random
import subprocess
import sys
import time
import uuid
from contextvars import ContextVar
from dataclasses import asdict, dataclass, field
from string import punctuation
from typing import Awaitable, Generator, Dict, List, AsyncGenerator, Tuple
from urllib.parse import urlparse, quote

import aiofiles
import aiohttp
import langdetect
import pandas as pd
import validators
import pdfkit
from async_lru import alru_cache as lru_cache
from bs4 import BeautifulSoup
from desert import metadata, schema
from facebook_scraper import get_posts
from faker import Faker
from instaloader import Instaloader, Profile
from instaloader.exceptions import LoginRequiredException
from marshmallow import fields, validate, ValidationError
from pdfminer.high_level import extract_text
from PyPDF3 import PdfFileReader
from rich import box
from rich.console import Console
from rich.errors import LiveError
from rich.live import Live
from rich.table import Table
from snscrape.modules import vkontakte as sns_vk, telegram as sns_tg, twitter as sns_tw
from summa import summarizer, keywords
from tumblpy import Tumblpy


__app_name__ = "SEARCH-ME"
__base_dir__ = os.getcwd()


logger = logging.getLogger(__app_name__)
stream = logging.StreamHandler()
stream.setFormatter(logging.Formatter('%(asctime)s	|	%(levelname)s	|	%(name)s	|	%(message)s'))
logger.addHandler(stream)
logger.addHandler(logging.NullHandler())


@dataclass
class Data(fields.Field):

	def to_dict(self):
		return asdict(self)


@dataclass
class SettingsWeb(Data):
	results: int = field(metadata=metadata(fields.Int(
		required=False,
		validate=validate.Range(min=1, error="Search results must be >= 1")
		)), default=10)
	retry: int = field(metadata=metadata(fields.Int(
		required=False,
		validate=validate.Range(min=0, error="Search retries must be >= 0")
		)), default=10)
	timeout: int = field(metadata=metadata(fields.Int(
		required=False,
		validate=validate.Range(min=0, error="Search timeout must be >= 0")
		)), default=60)
	wait_min: float = field(metadata=metadata(fields.Float(
		required=False,
		validate=validate.Range(min=0.0, error="Time for wait must be >= 0")
		)), default=0.0)
	wait_max: float = field(metadata=metadata(fields.Float(
		required=False,
		validate=validate.Range(min=0.0, error="Time for wait must be >= 0")
		)), default=1.5)
	headers: Dict = field(metadata=metadata(fields.Dict(
		required=False
		)), default_factory=lambda: {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})


@dataclass
class SettingsPdf(Data):
	timeout: int = field(metadata=metadata(fields.Int(
		required=False,
		validate=validate.Range(min=1, error="Pdf timeout >= 1")
		)), default=20)
	summary_params: Tuple = field(metadata=metadata(fields.Tuple((fields.Str(required=False), fields.Float(required=False)))), default=("ratio", 0.15))
	text: bool = field(metadata=metadata(fields.Boolean(required=False)), default=True)
	summary: bool = field(metadata=metadata(fields.Boolean(required=False)), default=True)
	urls: bool = field(metadata=metadata(fields.Boolean(required=False)), default=True)
	keywords: bool = field(metadata=metadata(fields.Boolean(required=False)), default=True)

	def __post_init__(self):
		summary_types = list(PdfSummaryTypes.__members__.keys())
		_type, _value = self.summary_params
		if not(_type in summary_types):
			raise ValidationError(f"Wrong summarize type. Choose one of: {', '.join(summary_types)}")
		if _type == PdfSummaryTypes.ratio.name and (_value <= 0 or _value >= 1):
			raise ValidationError(f"Summarize value must be in range (0,1) not: {_value}")
		if _type == PdfSummaryTypes.words.name and _value <= 0:
			raise ValidationError(f"Summarize value must be > 0 not: {_value}")


@dataclass
class SettingsSocial(Data):
	posts_limit: int = field(metadata=metadata(fields.Int(
		required=False,
		validate=validate.Range(min=1, error="Posts limit must be >= 1")
		)), default=10)
	timeout: float = field(metadata=metadata(fields.Float(
		required=False,
		validate=validate.Range(min=0.0, error="Timeout for download media must be >= 0")
		)), default=300)
	download_media: bool = field(metadata=metadata(fields.Boolean(required=False)), default=True)
	export_data: bool = field(metadata=metadata(fields.Boolean(required=False)), default=True)
	export_format: str = field(metadata=metadata(fields.Str(required=False)), default="csv")

	def __post_init__(self):
		export_formats = list(ExportFormats.__members__.keys())
		if not(self.export_format in export_formats):
			raise ValidationError(f"Not supported export format. Choose one of: {', '.join(export_formats)}")


@dataclass
class SettingsApp(Data):
	interactive: bool = field(metadata=metadata(fields.Boolean(required=False)), default=True)
	cache: bool = field(metadata=metadata(fields.Boolean(required=False)), default=True)


@dataclass
class Settings(Data):
	pdf_report: bool = field(metadata=metadata(fields.Boolean(required=False)), default=False)
	pdf_parse: bool = field(metadata=metadata(fields.Boolean(required=False)), default=False)
	social_search: bool = field(metadata=metadata(fields.Boolean(required=False)), default=False)
	socials: List = field(metadata=metadata(fields.List(fields.Str(required=False), required=False)), default_factory=lambda: [
		"vk", "instagram", "telegram", "twitter",
		"youtube", "facebook", "tumblr", "snapchat"
		])
	app: Dict = field(metadata=metadata(fields.Dict(required=False)), default_factory=SettingsApp)
	web: Dict = field(metadata=metadata(fields.Dict(required=False)), default_factory=SettingsWeb)
	pdf: Dict = field(metadata=metadata(fields.Dict(required=False)), default_factory=SettingsPdf)
	social: Dict = field(metadata=metadata(fields.Dict(required=False)), default_factory=SettingsSocial)

	def __post_init__(self):
		self.socials = tuple(self.socials)
		socials_types = list(Socials.__members__.keys())
		for social in self.socials:
			if not(social in socials_types):
				raise ValidationError(f"Not supported social: {social}")


@dataclass
class ResultPdf(Data):
	path: str = None
	text: str = None
	summary: str = None
	urls: List = None
	keywords: List = None


@dataclass
class ResultSocial(Data):
	vk: Dict = None
	instagram: Dict = None
	telegram: Dict = None
	twitter: Dict = None
	youtube: Dict = None
	facebook: Dict = None
	tumblr: Dict = None
	snapchat: Dict = None


@dataclass
class ResultSearch(Data):
	q: str = None
	rating: int = None
	uri: str = None
	social: Dict = None
	pdf: Dict = None


class Utils:

	@staticmethod
	def random_sleep(min, max):
		time.sleep(random.uniform(min, max))

	@staticmethod
	@functools.lru_cache(maxsize=64)
	def parse_url(url):
		return urlparse(url)

	@staticmethod
	def catch_log(f):
		async def wrapper(*args, **kwargs):
			obj = args[0]
			try:
				result = await f(*args, **kwargs)
			except Exception as e:
				logger.error(f"{obj.name}	|	F	|	{str(e)}")
			else:
				logger.debug(f"{obj.name}	|	OK")
				return result
		return wrapper


class SocialSearch:

	def __init__(self, **kwargs):
		self.cli = CliDesigner()
		self.settings = SettingsSocial(**kwargs)
		self.stop_words = list(StopWords.__members__.keys())
		for social in (Socials):
			if isinstance(self, social.value):
				__name = social.name
				self.name = __name
				if isinstance(self, Tumblr) and self.settings.download_media:
					self.api = Tumblpy(
						app_key='zLgPh6LeV7DyczfPALkTEfr8rOgzcYAY8TzAlabVIYrgpATPON',
						app_secret='mGP5mVle2ZUNKHzK4ayjAGpfUCkLTmQm91ic9YtWTTcDkdFLPE',
						oauth_token='hRwAn1CoZJ5Q96T8o51aQL2YcKnh1k66RlnCRLQtqjtWf0WZ4W',
						oauth_token_secret='oqlple5FP9MVRTxbUQHjrEVSs4DDLFP7h4zBE5D4g952qeqRo3'
						)
					self.api_youtube = Youtube(**kwargs)
				if isinstance(self, Instagram):
					self.api = Instaloader()
				break
		else:
			logger.error(f"APP	|	S01	|	{Errors.get_msg_by_code('S01')}")
			sys.exit()

	@staticmethod
	def catch_log(f):
		async def wrapper(*args, **kwargs):
			obj, result_obj = args[0], kwargs["result"]
			try:
				result = await f(*args, **kwargs)
			except Exception as e:
				logger.error(f"{obj.name}	|	S	|	{result_obj}	|	{str(e)}")
				return (obj.name, None)
			else:
				logger.debug(f"{obj.name}	|	{result_obj}	|	OK")
				return (obj.name, result)
			finally:
				if (
					isinstance(obj, Instagram) or
					isinstance(obj, Youtube) or
					isinstance(obj, Tumblr) or
					isinstance(obj, Snapchat)
					):
					os.chdir(__base_dir__)
		return wrapper

	async def search(self):
		raise NotImplementedError()

	async def export_data(self, array, q):
		data = pd.DataFrame(array)
		file_path = f'{os.path.join(__base_dir__, q, self.name)}.{self.settings.export_format}'
		if self.settings.export_format == ExportFormats.json.name:
			with open(file_path, "w") as f:
				json.dump({self.name: array}, f)
		else:
			export_map = \
				{
					ExportFormats.csv.name: data.to_csv,
					ExportFormats.xls.name: data.to_excel,
					ExportFormats.html.name: data.to_html,
					ExportFormats.parquet.name: data.to_parquet,
					ExportFormats.pkl.name: data.to_pickle
				}
			export_map[self.settings.export_format](file_path, index=False)
		logger.debug(f'{self.name}	|	{file_path}')

	async def get_user_from_link(self, link, item=1):
		user = Utils.parse_url(link).path.split("/")[item]
		return None if user in self.stop_words else user

	async def download(self, cmd, result):
		try:
			await asyncio.wait_for(self.__download__(cmd), timeout=self.settings.timeout)
		except (asyncio.TimeoutError, Exception) as e:
			logger.error(f"{self.name}	|	S03	|	{result}	|	{str(e)}")

	@staticmethod
	async def __download__(cmd):
		proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.DEVNULL)
		await proc.wait()


class Vk(SocialSearch):

	@SocialSearch.catch_log
	async def search(self, result):
		user = await self.get_user_from_link(result.uri)
		if user is None:
			return user
		else:
			vk_posts = []
			for limit, vk_post in enumerate(
				sns_vk.VKontakteUserScraper(
					user
					).get_items()
				):
				if limit == self.settings.posts_limit:
					break
				vk_posts.append({
					'date': vk_post.date,
					'url': vk_post.url,
					'content': vk_post.content
					})
			if self.settings.export_data:
				await self.export_data(array=vk_posts, q=result.q)
			return vk_posts


class Instagram(SocialSearch):

	@SocialSearch.catch_log
	async def search(self, result):
		user = await self.get_user_from_link(result.uri)
		if user is None:
			return user
		else:
			lre_raised = False
			ig_posts = []
			attrs = [
				'caption', 'caption_hashtags', 'comments',
				'date', 'is_sponsored', 'is_video', 'likes',
				'location', 'mediacount', 'mediaid', 'owner_id',
				'owner_profile', 'owner_username', 'profile',
				'shortcode', 'sponsor_users', 'tagged_users',
				'title', 'typename', 'url', 'video_duration',
				'video_url', 'video_view_count',
				'viewer_has_liked'
			]
			os.chdir(os.path.join(__base_dir__, result.q, self.name))
			for limit, post in enumerate(
				Profile.from_username(
					self.api.context,
					user
					).get_posts()
				):
				if limit == self.settings.posts_limit:
					break
				ig_post = {}
				try:
					if not(lre_raised):
						for attr in attrs:
							value = getattr(post, attr)
							if callable(value): 
								ig_post[attr] = list(value()) if isinstance(
									value(),
									Generator
									) else value()
							else:
								ig_post[attr] = value
						if self.settings.download_media:
							self.api.download_post(post, user)
				except LoginRequiredException as e:
					logger.error(f"{self.name}	|	S02	|	{result}	|	{str(e)}")
					lre_raised = True
				else:
					if ig_post:
						ig_posts.append(ig_post)
			if self.settings.download_media and lre_raised:
				await self.download(
					cmd=[
						"instaloader",
						f"{user}",
						"-c",
						f"{self.settings.posts_limit}"
					],
					result=result
					)
			if self.settings.export_data:
				await self.export_data(array=ig_posts, q=result.q)
			return ig_posts


class Telegram(SocialSearch):

	@SocialSearch.catch_log
	async def search(self, result):
		user = await self.get_user_from_link(result.uri)
		if user is None:
			return user
		else:
			tg_posts = []
			for limit, tg_post in enumerate(
				sns_tg.TelegramChannelScraper(
					name=user
					).get_items()
				):
				if limit == self.settings.posts_limit:
					break
				tg_posts.append({
					'date': tg_post.date,
					'url': tg_post.url,
					'content': tg_post.content
					})
			if self.settings.export_data:
				await self.export_data(array=tg_posts, q=result.q)
			return tg_posts


class Twitter(SocialSearch):

	@SocialSearch.catch_log
	async def search(self, result):
		user = await self.get_user_from_link(result.uri)
		if user is None:
			return user
		else:
			tw_posts = []
			for limit, tw_post in enumerate(
				sns_tw.TwitterSearchScraper(
					query=user
					).get_items()
				):
				if limit == self.settings.posts_limit:
					break
				tw_posts.append({
					'date': tw_post.date,
					'id': tw_post.id,
					'username': tw_post.username,
					'url': tw_post.url,
					'content': tw_post.content,
					'outlinks': tw_post.outlinks
					})
			if self.settings.export_data:
				await self.export_data(tw_posts, q=result.q)
			return tw_posts


class Youtube(SocialSearch):

	@SocialSearch.catch_log
	async def search(self, result):
		pre_user = await self.get_user_from_link(result.uri)
		user = await self.get_user_from_link(
			result.uri,
			item=2
			) if pre_user == "c" or pre_user == "channel" else None
		if self.settings.download_media:
			os.chdir(os.path.join(__base_dir__, result.q, self.name))
			await self.download(
					cmd=[
						"youtube-dl",
						f"{result.uri}",
						"--playlist-end",
						f"{self.settings.posts_limit}"
					],
					result=result
					)
		return user


class Facebook(SocialSearch):

	@SocialSearch.catch_log
	async def search(self, result):
		user = await self.get_user_from_link(result.uri)
		if user is None:
			return user
		else:
			fb_posts = []
			for limit, fb_post in enumerate(
				get_posts(
					user,
					pages=self.settings.posts_limit
					)
				):
				if limit == self.settings.posts_limit:
					break
				fb_posts.append(fb_post)
			if self.settings.export_data:
				await self.export_data(fb_posts, q=result.q)
			return fb_posts


class Tumblr(SocialSearch):

	@staticmethod
	async def get_user_from_link(link):
		return link.split("/")[2].split(".")[0]

	@SocialSearch.catch_log
	async def search(self, result):

		tblr_posts = []

		async def _get_posts(user):
			for post in self.api.posts(user)['posts']:
				tblr_posts.append(post)
				post_type = post.get("type", None)
				if post_type == MediaTypes.photo.name:
					for ph in post["photos"]:
						yield ("media", ph["original_size"]["url"])
				if post_type == MediaTypes.video.name:
					post_video_type = post.get("video_type", None)
					if post_video_type == self.name:
						__type, __url = "media", post.get("video_url", None)
					if post_video_type == self.api_youtube.name:
						__type, __url = "youtube", post.get("permalink_url", None)
					if not(__url is None):
						yield (__type, __url)

		user = await self.get_user_from_link(result.uri)
		if self.settings.download_media:
			os.chdir(os.path.join(__base_dir__, result.q, self.name))
			async with aiohttp.ClientSession(
				timeout=aiohttp.ClientTimeout(total=self.settings.timeout)
				) as session:
				async for __type, __url in _get_posts(user=user):
					if __type == "media":
						async with aiofiles.open(__url.split("/")[-1], mode='wb') as f:
							async with session.get(__url) as resp:
								if resp.status == 200:
									await f.write(await resp.read())
				if __type == self.api_youtube.name:
					self.api_youtube.search(result)
		if self.settings.export_data:
				await self.export_data(array=tblr_posts, q=result.q)
		return tblr_posts


class Snapchat(SocialSearch):

	@SocialSearch.catch_log
	async def search(self, result):
		pre_user = await self.get_user_from_link(result.uri)
		user = await self.get_user_from_link(
			result.uri,
			item=2
			) if pre_user == "u" or pre_user == "add" else None
		if self.settings.download_media and not(user is None):
			os.chdir(os.path.join(__base_dir__, result.q, self.name))
			await self.download(
					cmd=[
						"snapchat-dl",
						f"{user}",
						"-l",
						f"{self.settings.posts_limit}"
					],
					result=result
					)
		return user


class CliDesigner:

	def __init__(self, startup=False):
		self.colors = [
			'#F0F8FF', '#FAEBD7', '#00FFFF', '#7FFFD4', '#F0FFFF', '#F5F5DC',
			'#FFE4C4', '#000000', '#FFEBCD', '#0000FF', '#8A2BE2', '#A52A2A',
			'#DEB887', '#5F9EA0', '#7FFF00', '#D2691E', '#FF7F50', '#6495ED',
			'#FFF8DC', '#DC143C', '#00FFFF', '#00008B', '#008B8B', '#B8860B',
			'#A9A9A9', '#006400', '#A9A9A9', '#BDB76B', '#8B008B', '#556B2F',
			'#FF8C00', '#9932CC', '#8B0000', '#E9967A', '#8FBC8F', '#483D8B',
			'#2F4F4F', '#2F4F4F', '#00CED1', '#9400D3', '#FF1493', '#00BFFF',
			'#696969', '#696969', '#1E90FF', '#B22222', '#FFFAF0', '#228B22',
			'#FF00FF', '#DCDCDC', '#F8F8FF', '#FFD700', '#DAA520', '#808080',
			'#008000', '#ADFF2F', '#808080', '#F0FFF0', '#FF69B4', '#CD5C5C',
			'#4B0082', '#FFFFF0', '#F0E68C', '#E6E6FA', '#FFF0F5', '#7CFC00',
			'#FFFACD', '#ADD8E6', '#F08080', '#E0FFFF', '#FAFAD2', '#D3D3D3',
			'#90EE90', '#D3D3D3', '#FFB6C1', '#FFA07A', '#20B2AA', '#87CEFA',
			'#778899', '#778899', '#B0C4DE', '#FFFFE0', '#00FF00', '#32CD32',
			'#FAF0E6', '#FF00FF', '#800000', '#66CDAA', '#0000CD', '#BA55D3',
			'#9370DB', '#3CB371', '#7B68EE', '#00FA9A', '#48D1CC', '#C71585',
			'#191970', '#F5FFFA', '#FFE4E1', '#FFE4B5', '#FFDEAD', '#000080',
			'#FDF5E6', '#808000', '#6B8E23', '#FFA500', '#FF4500', '#DA70D6',
			'#EEE8AA', '#98FB98', '#AFEEEE', '#DB7093', '#FFEFD5', '#FFDAB9',
			'#CD853F', '#FFC0CB', '#DDA0DD', '#B0E0E6', '#800080', '#663399',
			'#FF0000', '#BC8F8F', '#4169E1', '#8B4513', '#FA8072', '#F4A460',
			'#2E8B57', '#FFF5EE', '#A0522D', '#C0C0C0', '#87CEEB', '#6A5ACD',
			'#708090', '#708090', '#FFFAFA', '#00FF7F', '#4682B4', '#D2B48C',
			'#008080', '#D8BFD8', '#FF6347', '#40E0D0', '#EE82EE', '#F5DEB3',
			'#FFFFFF', '#F5F5F5', '#FFFF00', '#9ACD32'
			]
		self.startup = startup
		self.init_console_and_table()

	def init_console_and_table(self):
		headers = [f"{self.get_rnd_color()}SEARCH", f"{self.get_rnd_color()}ME"]
		self.console = Console()
		self.table = Table(box=box.SQUARE_DOUBLE_HEAD)
		for column in headers:
			self.table.add_column(column, justify="left")
		if self.startup:
			self.console.rule(" ".join(headers))

	def get_rnd_color(self):
		return f"[bold {random.choice(self.colors)}]"


class PdfSummaryTypes(enum.Enum):
	words = enum.auto()
	ratio = enum.auto()


class PdfLanguages(enum.Enum):
	ar = "arabic"
	da = "danish"
	de = "german"
	en = "english"
	es = "spanish"
	fi = "finnish"
	fr = "french"
	hu = "hungarian"
	it = "italian"
	nb = "norwegian"
	nl = "dutch"
	pl = "polish"
	pt = "portuguese"
	ro = "romanian"
	ru = "russian"
	sv = "swedish"

	@classmethod
	@functools.lru_cache(maxsize=16)
	def get_lang_by_code(cls, code):
		for k, v in cls.__members__.items():
			if k == code:
				return v.value
		else:
			raise Exception(f"Can't find language with code {code}")


class PdfWorker:

	def __init__(self, path, summary_params):
		self.path = path
		self.__summary_type, self.__summary_value = summary_params

	@lru_cache(maxsize=2)
	async def get_bytes(self):
		async with aiofiles.open(self.path, mode='rb') as f:
			return io.BytesIO(await f.read())

	@lru_cache(maxsize=2)
	async def get_text(self) -> Tuple:
		return "text", extract_text(await self.get_bytes())

	async def get_summary(self) -> Tuple:
		summary = ""
		_, pdf_text = await self.get_text()
		try:
			lang_code = langdetect.detect(pdf_text)
			lang = PdfLanguages.get_lang_by_code(lang_code)
		except (
			langdetect.lang_detect_exception.LangDetectException,
			Exception
			) as e:
			logger.error(f"PDF SUMMARY	|	P02	|	{str(e)}")
			summary = str(e)
		else:
			if self.__summary_type == PdfSummaryTypes.words.name:
				self.__words = len(pdf_text.split())
				if self.__summary_value > self.__words:
					self.__summary_value = self.__words
				summary = summarizer.summarize(
					pdf_text,
					language=lang,
					words=self.__summary_value)
			if self.__summary_type is PdfSummaryTypes.ratio.name:
				summary = summarizer.summarize(
					pdf_text,
					language=lang,
					ratio=self.__summary_value)
		return "summary", summary

	async def get_keywords(self) -> Tuple:
		_, pdf_text = await self.get_text()
		try:
			return ("keywords", [
				keyword for keyword in (
					keywords.keywords(pdf_text)
					).splitlines()
				])
		except (MemoryError, Exception) as e:
			logger.error(f"PDF KEYWORDS	|	P03	|	{str(e)}")
			return "keywords", None

	async def get_urls(self) -> Tuple:
		urls = []
		pdf = PdfFileReader(await self.get_bytes())
		for page in range(0, pdf.numPages):
			pdf_page = pdf.getPage(page)
			if '/Annots' in pdf_page:
				for item in (pdf_page['/Annots']):
					pdf_obj = item.getObject()
					if "/A" in pdf_obj and "/URI" in pdf_obj["/A"]:
						urls.append(pdf_obj["/A"]["/URI"])
		return "urls", urls

	async def get_path(self) -> Tuple:
		return "path", self.path


class Engine:

	def __init__(self, **kwargs):
		for engine in (Engines):
			if isinstance(self, engine.value):
				self.name = engine.name
				break
		else:
			logger.error(f"APP	|	E01	|	{Errors.get_msg_by_code('E01')}")
			sys.exit()
		settings_schema = schema(Settings)
		if kwargs:
			try:
				self.settings = settings_schema.load(kwargs)
				self.settings.app = SettingsApp(**self.settings.app)
				self.settings.web = SettingsWeb(**self.settings.web)
				self.settings.pdf = SettingsPdf(**self.settings.pdf)
				self.settings.social = SettingsSocial(**self.settings.social)
			except ValidationError as e:
				logger.error(f"{self.name}	|	E02	|	{str(e)}")
				sys.exit()
		else:
			self.settings = Settings()
		self.cli = CliDesigner()
		self.socials = Socials.__members__
		self.black_symbols = "".join(list(punctuation)) + "\n"
		self.ssi = ContextVar("SearchSessionId")
		if self.settings.app.interactive:
			self.__cli = CliDesigner(startup=True)
			with Live(self.__cli.table, refresh_per_second=4):
				for arg, value in self.settings.to_dict().items():
					if isinstance(value, dict):
						value_new = json.dumps(value, indent=4)
					elif isinstance(value, list) or isinstance(value, tuple):
						value_new = "\n".join(value)
					else:
						value_new = value
					self.__cli.table.add_row(f"{self.__cli.get_rnd_color()}{arg}", f"{self.__cli.get_rnd_color()}{value_new}")
					Utils.random_sleep(min=0.3, max=0.5)
			del self.__cli
		self.map_obj = {k: v.value for k, v in self.socials.items()}
		self.map_addr = {
			k: "t.me" if k == Socials.telegram.name else f"{k}.com" for k in list(
				self.socials.keys()
				)
				}
		for __social, __obj in self.map_obj.items():
			setattr(
				self,
				__social, __obj(
					**self.settings.social.to_dict()
					))if __social in self.settings.socials else setattr(self, __social, None)
		self.map_dir = {
			Socials.instagram.name: self.instagram,
			Socials.youtube.name: self.youtube,
			Socials.tumblr.name: self.tumblr,
			Socials.snapchat.name: self.snapchat
			}
		self.map_main = {k: getattr(self, k) for k in list(self.socials.keys())}
		for engine in (Engines):
			if isinstance(self, engine.value):
				__name = engine.name
				self.name = __name
				break

	def __str__(self):
		return f"{(self.name).upper()}()"

	def __repr__(self):
		return f"{(self.name).upper()}({self.settings})"

	@property
	async def results(self) -> AsyncGenerator:
		if not(hasattr(self, "search_results")) or len(self.search_results) <= 0:
			yield
		else:
			if self.settings.app.interactive:
				with self.cli.console.status(f"{self.cli.get_rnd_color()}", spinner="aesthetic") as status:
					for count, __result in enumerate(self.search_results):
						Utils.random_sleep(min=0.1, max=0.3)
						status.update(f"{self.cli.get_rnd_color()}{count + 1}")
						yield __result
			else:
				for __result in self.search_results:
					yield __result

	async def test(self, samples=3):
		fake = Faker()
		await self.search(*list(itertools.chain(
			[fake.name() for _ in range(random.randint(1, samples))],
			[fake.address() for _ in range(random.randint(1, samples))],
			[fake.text()[:random.randint(10, 30)] for _ in range(
				random.randint(1, samples)
				)])))
		async for r in self.results:
			print(f"{r.q}	|	{r.rating}	|	{r.uri}")

	def mkdir(self, *dirs):
		os.makedirs(os.path.join(__base_dir__, *dirs), exist_ok=True, mode=0o777)

	@Utils.catch_log
	async def cache_pkl(self):
		with open(f"{__app_name__}-{self.ssi.get()}.pkl", "wb") as pkl:
			pickle.dump(self.data4cache, pkl)

	@Utils.catch_log
	async def cache_json(self):
		with open(f"{__app_name__}-{self.ssi.get()}.json", "w") as js:
			json.dump(self.data4cache, js, indent=5, ensure_ascii=True)

	async def parse_pdf(self, path) -> ResultPdf:
		pdf = PdfWorker(path=path, summary_params=self.settings.pdf.summary_params)
		tasks = [pdf.get_path]
		if self.settings.pdf.text:
			tasks.append(pdf.get_text)
		if self.settings.pdf.summary:
			tasks.append(pdf.get_summary)
		if self.settings.pdf.urls:
			tasks.append(pdf.get_urls)
		if self.settings.pdf.keywords:
			tasks.append(pdf.get_keywords)
		return ResultPdf(**{
			k: v for k, v in await asyncio.gather(
				*[t() for t in tasks]
				)
				})

	async def export_pdf(self, result) -> ResultPdf:
		path = os.path.join(
			__base_dir__,
			result.q,
			f"{result.rating}. {Utils.parse_url(result.uri).netloc}.pdf"
			)
		await pdfkit.from_url(result.uri, path)
		return ResultPdf(path=path)

	async def generate_pdf(self, result) -> ResultPdf:
		result_pdf = ResultPdf()
		try:
			result_pdf = await asyncio.wait_for(
				self.export_pdf(result),
				timeout=self.settings.pdf.timeout
				)
		except (asyncio.TimeoutError, OSError) as e:
			logger.error(f"PDF EXPORT	|	P01	|	{str(e)}")
		else:
			if os.path.exists(result_pdf.path) and self.settings.pdf_parse:
				result_pdf = await self.parse_pdf(result_pdf.path)
		return result_pdf

	async def social_search(self, result) -> ResultSocial:
		website = Utils.parse_url(result.uri).netloc
		tasks = []
		for __social, __social_obj in self.map_main.items():
			if (self.map_addr[__social] in website and not(__social_obj is None)):
				if __social in self.map_dir:
					self.mkdir(result.q, __social)
				tasks.append((__social_obj.search, result))
			else:
				continue
		return ResultSocial(**{
			k: v for k, v in await asyncio.gather(*[
				t(result=result) for t, result in tasks
				])
				})

	async def search(self, *args) -> Awaitable:
		ssi = self.ssi.set(str(uuid.uuid4()).upper())
		logger.debug(f"Search start	|	{self.ssi.get()}	|	{args}")
		self.search_results, self.data4cache = [], []
		await asyncio.gather(*(
			self.search_q(str(q).translate(
				str.maketrans("", "", self.black_symbols)
				)) for q in args
				))
		logger.debug(f"Search end	|	{self.ssi.get()}	|	{args}")
		self.ssi.reset(ssi)

	async def search_q(self, q) -> Awaitable:
		self.mkdir(q)
		page = await self.send_request(q)
		if self.settings.app.interactive:
			self.cli.table.add_row(u"🔎", f"{self.cli.get_rnd_color()}{q}")
			try:
				with Live(self.cli.table, refresh_per_second=5):
					async for result in self.parse_page(q, page):
						self.cli.table.add_row(
							f"{self.cli.get_rnd_color()}{result.rating}",
							f"{self.cli.get_rnd_color()}{result.uri}"
							)
						Utils.random_sleep(min=0.2, max=0.4)
						if self.settings.pdf_report:
							result.pdf = await self.generate_pdf(result)
						if self.settings.social_search:
							result.social = await self.social_search(result)
						self.search_results.append(result)
						self.data4cache.append(result.to_dict())
			except LiveError:
				pass
		else:
			async for result in self.parse_page(q, page):
				if self.settings.pdf_report:
					result.pdf = await self.generate_pdf(result)
				if self.settings.social_search:
					result.social = await self.social_search(result)
				self.search_results.append(result)
				print(result.to_dict())
				self.data4cache.append(result.to_dict())
		if self.settings.app.cache:
			await asyncio.gather(*(self.cache_pkl(), self.cache_json()))


class Google(Engine):

	domains = (
		'com', 'al', 'dz', 'as', 'ad', 'am', 'ac', 'at', 'az', 'bs', 'by', 'be',
		'bj', 'ba', 'vg', 'bg', 'bf', 'cm', 'ca', 'cv', 'cat', 'cf', 'td', 'cl',
		'cn', 'cd', 'cg', 'ci', 'hr', 'cz', 'dk', 'dj', 'dm', 'tl', 'ec', 'ee',
		'fm', 'fi', 'fr', 'ga', 'gm', 'ps', 'ge', 'de', 'gr', 'gl', 'gp', 'gg',
		'gy', 'ht', 'hn', 'hu', 'is', 'iq', 'ie', 'im', 'it', 'jp', 'je', 'jo',
		'kz', 'ki', 'kg', 'la', 'lv', 'li', 'lt', 'lu', 'mk', 'mg', 'mw', 'mv',
		'ml', 'mu', 'md', 'mn', 'me', 'ms', 'nr', 'nl', 'ne', 'ng', 'nu', 'no',
		'ps', 'pn', 'pl', 'pt', 'ro', 'ru', 'rw', 'sh', 'ws', 'sm', 'st', 'sn',
		'rs', 'sc', 'sk', 'si', 'so', 'es', 'lk', 'sr', 'ch', 'tg', 'tk', 'to',
		'tt', 'tn', 'tm', 'ae', 'vu'
		)

	languages = (
		'af', 'ach', 'ak', 'am', 'ar', 'az', 'be', 'bem', 'bg', 'bh', 'bn', 'br',
		'bs', 'ca', 'chr', 'ckb', 'co', 'crs', 'cs', 'cy', 'da', 'de', 'ee', 'el',
		'en', 'eo', 'es', 'es-419', 'et', 'eu', 'fa', 'fi', 'fo', 'fr', 'fy',
		'ga', 'gaa', 'gd', 'gl', 'gn', 'gu', 'ha', 'haw', 'hi', 'hr', 'ht', 'hu',
		'hy', 'ia', 'id', 'ig', 'is', 'it', 'iw', 'ja', 'jw', 'ka', 'kg', 'kk',
		'km', 'kn', 'ko', 'kri', 'ku', 'ky', 'la', 'lg', 'ln', 'lo', 'loz', 'lt',
		'lua', 'lv', 'mfe', 'mg', 'mi', 'mk', 'ml', 'mn', 'mo', 'mr', 'ms', 'mt',
		'ne', 'nl', 'nn', 'no', 'nso', 'ny', 'nyn', 'oc', 'om', 'or', 'pa', 'pcm',
		'pl', 'ps', 'pt-BR', 'pt-PT', 'qu', 'rm', 'rn', 'ro', 'ru', 'rw', 'sd',
		'sh', 'si', 'sk', 'sl', 'sn', 'so', 'sq', 'sr', 'sr-ME', 'st', 'su', 'sv',
		'sw', 'ta', 'te', 'tg', 'th', 'ti', 'tk', 'tl', 'tn', 'to', 'tr', 'tt',
		'tum', 'tw', 'ug', 'uk', 'ur', 'uz', 'vi', 'wo', 'xh', 'xx-bork',
		'xx-elmer', 'xx-hacker', 'xx-klingon', 'xx-pirate', 'yi', 'yo', 'zh-CN',
		'zh-TW', 'zu'
		)

	async def parse_page(self, q, html) -> AsyncGenerator:
		soup = BeautifulSoup(html, 'html.parser')
		blocks = soup.find_all('div', attrs={'class': 'g'})
		for count, block in enumerate(blocks):
			uri, title = block.find('a', href=True), block.find('h3')
			if uri and title:
				url = uri["href"]
				if validators.url(url):
					search_result = ResultSearch(q=q, rating=count + 1, uri=url)
					yield search_result

	async def send_request(self, q, retry=0):
		uri_req = f"https://www.google.{random.choice(self.domains)}/search?q={q.replace(' ', '+')}&num={self.settings.web.results}&hl={random.choice(self.languages)}"
		response_text = None
		try:
			async with aiohttp.ClientSession(
				timeout=aiohttp.ClientTimeout(total=self.settings.web.timeout),
				headers=self.settings.web.headers
				) as session:
				response = await session.get(uri_req)
				response_text = await response.text()
			Utils.random_sleep(
				min=self.settings.web.wait_min,
				max=self.settings.web.wait_max
				)
			if response.status != 200:
				raise Exception(f"Not valid request, status: {response.status}")
		except (aiohttp.ClientError, Exception) as e:
			logger.error(f"{q}	|	E03	|	{retry}	|	{str(e)}")
			response_text = None
			while retry < self.settings.web.retry and not(response_text):
				response_text = await self.send_request(q=q, retry=retry + 1)
			return response_text
		else:
			return response_text


class Rambler(Engine):

	async def parse_page(self, q, html) -> AsyncGenerator:
		soup = BeautifulSoup(html, 'html.parser')
		blocks = soup.find_all('article')
		for count, block in enumerate(blocks):
			url = block.find_all('a')[0]['href']
			if url and not("yabs.yandex.ru" in url):
				if validators.url(url):
					search_result = ResultSearch(q=q, rating=count + 1, uri=url)
					yield search_result

	async def send_request(self, q, retry=0):
		uri_req = f"https://nova.rambler.ru/search?query={quote(q.replace(' ', '+'))}&utm_source=search_r0&utm_campaign=self_promo&utm_medium=form&utm_content=search"
		response_text = None
		try:
			async with aiohttp.ClientSession(
				timeout=aiohttp.ClientTimeout(total=self.settings.web.timeout),
				headers=self.settings.web.headers
				) as session:
				response = await session.get(uri_req)
				response_text = await response.text()
			Utils.random_sleep(
				min=self.settings.web.wait_min,
				max=self.settings.web.wait_max
				)
			if response.status != 200:
				raise Exception("Not valid request")
		except (aiohttp.ClientError, Exception) as e:
			logger.error(f"{q}	|	E03	|	{retry}	|	{str(e)}")
			response_text = None
			while retry < self.settings.web.retry and not(response_text):
				response_text = await self.send_request(q=q, retry=retry + 1)
			return response_text
		else:
			return response_text


class Searx(Engine):

	domains = (
		'7m.ee', 'bar', 'bissisoft.com', 'decatec.de', 'devol.it',
		'divided-by-zero.eu', 'dresden.network', 'feneas.org', 'fmac.xyz',
		'gnu.style', 'lelux.fi', 'likkle.monster', 'lnode.net', 'mastodontech.de',
		'mdosch.de', 'monicz.pl', 'mxchange.org', 'nakhan.net', 'nevrlands.de',
		'ninja', 'nixnet.services', 'openhoofd.nl', 'org', 'prvcy.eu', 'pwoss.org',
		'rasp.fr', 'roflcopter.fr', 'roughs.ru', 'ru', 'silkky.cloud', 'sk',
		'sp-codes.de', 'sunless.cloud', 'tux.land', 'tyil.nl', 'webheberg.info',
		'xyz', 'zackptg5.com'
		)

	languages = (
		'af-ZA', 'all', 'ar-EG', 'be-BY', 'bg-BG', 'ca-ES', 'cs-CZ', 'da-DK',
		'de', 'de-AT', 'de-CH', 'de-DE', 'el-GR', 'en', 'en-AU', 'en-CA', 'en-GB',
		'en-IE', 'en-IN', 'en-NZ', 'en-PH', 'en-SG', 'en-US', 'es', 'es-AR',
		'es-CL', 'es-ES', 'es-MX', 'et-EE', 'fa-IR', 'fi-FI', 'fr', 'fr-BE',
		'fr-CA', 'fr-CH', 'fr-FR', 'he-IL', 'hr-HR', 'hu-HU', 'hy-AM', 'id-ID',
		'is-IS', 'it-IT', 'ja-JP', 'ko-KR', 'lt-LT', 'lv-LV', 'ms-MY', 'nb-NO',
		'nl', 'nl-BE', 'nl-NL', 'pl-PL', 'pt', 'pt-BR', 'pt-PT', 'ro-RO', 'ru-RU',
		'sk-SK', 'sl-SI', 'sr-RS', 'sv-SE', 'sw-TZ', 'th-TH', 'tr-TR', 'uk-UA',
		'vi-VN', 'zh', 'zh-CN', 'zh-TW'
		)

	async def parse_page(self, q, html) -> AsyncGenerator:
		for count, block in enumerate(html["results"]):
			if "url" in block:
				url = block["url"]
				if validators.url(url):
					search_result = ResultSearch(q=q, rating=count + 1, uri=url)
					yield search_result

	async def send_request(self, q, retry=0):
		uri_req = f"http://searx.{random.choice(self.domains)}/search?q={q.replace(' ', '+')}&format=json&language={random.choice(self.languages)}"
		response_json = None
		try:
			async with aiohttp.ClientSession(
				timeout=aiohttp.ClientTimeout(total=self.settings.web.timeout),
				headers=self.settings.web.headers
				) as session:
				response = await session.get(uri_req)
				response_json = await response.json()
			Utils.random_sleep(
				min=self.settings.web.wait_min,
				max=self.settings.web.wait_max
				)
			if response.status != 200 or len(response_json["results"]) <= 0:
				raise Exception("Not valid request")
		except (
			aiohttp.client_exceptions.ContentTypeError,
			aiohttp.ClientError,
			Exception
			) as e:
			logger.error(f"{q}	|	E03	|	{retry}	|	{str(e)}")
			print(response_json)
			while retry < self.settings.web.retry and (response_json is None or response_json["number_of_results"] == 0):
				response_json = await self.send_request(q=q, retry=retry + 1)
			return response_json
		else:
			return response_json


class Socials(enum.Enum):
	vk = Vk
	instagram = Instagram
	telegram = Telegram
	twitter = Twitter
	youtube = Youtube
	facebook = Facebook
	tumblr = Tumblr
	snapchat = Snapchat


class Engines(enum.Enum):
	google = Google
	rambler = Rambler
	searx = Searx


class ExportFormats(enum.Enum):
	csv = enum.auto()
	xls = enum.auto()
	html = enum.auto()
	json = enum.auto()
	parquet = enum.auto()
	pkl = enum.auto()


class StopWords(enum.Enum):
	explore = enum.auto()
	tags = enum.auto()
	wall = enum.auto()
	music = enum.auto()


class MediaTypes(enum.Enum):
	photo = enum.auto()
	video = enum.auto()


class Errors(enum.Enum):
	E01 = "Created class is not engine"
	E02 = enum.auto()
	E03 = enum.auto()
	F = enum.auto()
	P01 = enum.auto()
	P02 = enum.auto()
	P03 = enum.auto()
	S = enum.auto()
	S01 = "Created class is not social"
	S02 = enum.auto()
	S03 = enum.auto()

	@classmethod
	@functools.lru_cache(maxsize=4)
	def get_msg_by_code(cls, code):
		for error in (Errors):
			if error.name == code:
				return error.value


__all__ = ["Searx", "Google", "Rambler"]
