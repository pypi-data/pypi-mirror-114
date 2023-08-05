"""Print in fancy ways.
"""
from __future__ import annotations

import sys
from enum import Enum
from typing import TextIO


class LogCode(str, Enum):
	"""Provide the capability to use an enum for logcodes if the user prefers.

	BOLD = "bold"
	ITALIC = "italic"
	HEADING = "head"
	DEBUG = "d"
	INFO = "i"
	OK = "ok"
	WARNING = "w"
	ERROR = "e"
	CRITICAL = "crit"
	"""

	BOLD = "bold"
	ITALIC = "italic"
	HEADER = HEADING = "head"
	DEBUG = "d"
	INFO = "i"
	SUCCESS = OK = "ok"
	WARNING = "w"
	ERROR = "e"
	CRITICAL = "crit"


LogType = LogCode


class Logger:
	"""Logger class. Can be used to make a custom logger.

	pprint and pstr methods have the same signature as the inbuilt print
	method so migration is easy and use ll/loglevel. For prefab methods
	supplied by this library, ll/loglevel can be any of:

	"bold": For bold text,
	"italic": For italic text,
	"head": For a heading,
	"d": For a debug message,
	"i": Info message,
	"ok": For some successful operation,
	"w": For a warning,
	"e": For some error,
	"crit": For some critical event,

	However, you can create your own... eg `mylogger = Logger({"cat": "🐱 {}"})
	to add a cat emoji before a message (if so inclined)
	"""

	def __init__(self, mapping: dict[str, str] = None) -> None:
		"""Logger class. Can be used to make a custom logger.

		pprint and pstr methods have the same signature as the inbuilt print
		method so migration is easy and use ll/loglevel. For prefab methods
		supplied by this library, ll/loglevel can be any of:

		"bold": For bold text,
		"italic": For italic text,
		"head": For a heading,
		"d": For a debug message,
		"i": Info message,
		"ok": For some successful operation,
		"w": For a warning,
		"e": For some error,
		"crit": For some critical event,

		However, you can create your own... eg `mylogger = Logger({"cat": "🐱 {}"})
		to add a cat emoji before a message (if so inclined)

		Args:
			mapping (dict[str, str], optional): [description]. Defaults to dict().
		"""
		self.mapping = {} if mapping is None else mapping

	def _lookup(self, key: str):
		if key in self.mapping:
			return self.mapping[key]
		return "{}"

	def pprint(
		self,
		*values: object,
		sep: str = " ",
		end: str = "\n",
		file: TextIO = sys.stdout,
		flush: bool = False,
		ll: LogCode | LogType | str = "",
		loglevel: LogCode | LogType | str = None,
	):
		r"""pprint function with the same signature as the inbuilt print...

		method so migration is easy and use ll/loglevel. For prefab methods
		supplied by this library, ll/loglevel can be any of:

		"bold": For bold text,
		"italic": For italic text,
		"head": For a heading,
		"d": For a debug message,
		"i": Info message,
		"ok": For some successful operation,
		"w": For a warning,
		"e": For some error,
		"crit": For some critical event,

		Args:
			*values (tuple[object]): values to print to stream
			sep (str, optional): string inserted between values. Defaults to " ".
			end (str, optional): string appended after last value. Defaults to "\n".
			file (TextIO, optional): a file like object/ stream. Defaults to sys.stdout.
			flush (bool, optional): whether to forcibly flush the stream. Defaults to False.
			ll (str, optional): set the loglevel (shorthand). Defaults to "".
			loglevel (str, optional): set the loglevel, omit this for normal print behaviour. Defaults to "".
		"""
		print(
			self.pstr(*values, sep=sep, end=end, ll=ll, loglevel=loglevel),
			end="",
			file=file,
			flush=flush,
		)

	def pstr(
		self,
		*values: object,
		sep: str = " ",
		end: str = "\n",
		ll: LogCode | LogType | str = "",
		loglevel: LogCode | LogType | str = None,
	) -> str:
		r"""pstr function with a similar signature as the inbuilt print...

		method so migration is easy and use ll/loglevel. For prefab methods
		supplied by this library, ll/loglevel can be any of:

		"bold": For bold text,
		"italic": For italic text,
		"head": For a heading,
		"d": For a debug message,
		"i": Info message,
		"ok": For some successful operation,
		"w": For a warning,
		"e": For some error,
		"crit": For some critical event,

		Args:
			*values (tuple[object]): values to create string from
			sep (str, optional): string inserted between values. Defaults to " ".
			end (str, optional): string appended after last value. Defaults to "\n".
			ll (str, optional): set the loglevel (shorthand). Defaults to "".
			loglevel (str, optional): set the loglevel, omit this for normal print behaviour. Defaults to "".

		Returns:
			str: Formatted string
		"""
		pStr = sep.join([str(value) for value in values])
		return self._lookup(loglevel or ll).format(pStr) + end


metLogger = Logger(
	{
		"bold": "\033[01m{}\033[00m",
		"italic": "\033[03m{}\033[00m",
		"head": "\033[01m\033[04m{}\033[00m",
		"d": "\033[01m\033[96m[$]\033[00m {}",
		"i": "\033[01m\033[36m[*]\033[00m {}",
		"ok": "\033[01m\033[32m[+]\033[00m {}",
		"w": "\033[01m\033[33m[/]\033[00m {}",
		"e": "\033[01m\033[31m[-]\033[00m {}",
		"crit": "\033[01m\033[91m[!]\033[00m {}",
	}
)
metPrint = metLogger.pprint
metStr = metLogger.pstr


fhLogger = Logger(
	{
		"bold": "\033[01m{}\033[00m",
		"italic": "\033[03m{}\033[00m",
		"head": "\033[01m\033[04m{}\033[00m",
		"d": "[\033[01m\033[96m$  Deb\033[00m] {}",
		"i": "[\033[36m* Info\033[00m] {}",
		"ok": "[\033[32m+   Ok\033[00m] {}",
		"w": "[\033[33m/ Warn\033[00m] {}",
		"e": "[\033[31m-  Err\033[00m] {}",
		"crit": "[\033[01m\033[91m! Crit\033[00m] {}",
	}
)
fhPrint = fhLogger.pprint
fhStr = fhLogger.pstr


fhnfLogger = Logger(
	{
		"bold": "\033[01m{}\033[00m",
		"italic": "\033[03m{}\033[00m",
		"head": "\033[01m\033[04m{}\033[00m",
		"d": "[\033[01m\033[96m\uf46f  Deb\033[00m] {}",
		"i": "[\033[36m\uf449 Info\033[00m] {}",
		"ok": "[\033[32m\uf42e   Ok\033[00m] {}",
		"w": "[\033[33m\uf467 Warn\033[00m] {}",
		"e": "[\033[31m\uf46e  Err\033[00m] {}",
		"crit": "[\033[01m\033[91m\uf421 Crit\033[00m] {}",
	}
)
fhnfPrint = fhnfLogger.pprint
fhnfStr = fhnfLogger.pstr


pythonLogger = Logger(
	{
		"head": "HEADER:{}",
		"d": "DEBUG:{}",
		"i": "INFO:{}",
		"ok": "SUCCESS:{}",
		"w": "WARNING:{}",
		"e": "ERROR:{}",
		"crit": "CRITICAL:{}",
	}
)
pythonPrint = pythonLogger.pprint
pythonStr = pythonLogger.pstr


colorlogLogger = Logger(
	{
		"bold": "\033[01m{}\033[00m",
		"italic": "\033[03m{}\033[00m",
		"head": "\033[01m\033[04m{}\033[00m",
		"d": "\033[36mDEBUG    \033[00m\033[34m{}\033[00m",
		"i": "\033[32mINFO     \033[00m\033[34m{}\033[00m",
		"ok": "\033[32mSUCCESS  \033[00m\033[34m{}\033[00m",
		"w": "\033[33mWARNING  \033[00m\033[34m{}\033[00m",
		"e": "\033[31mERROR    \033[00m\033[34m{}\033[00m",
		"crit": "\033[31mCRITICAL \033[00m\033[34m{}\033[00m",
	}
)
colorlogPrint = colorlogLogger.pprint
colorlogStr = colorlogLogger.pstr


printtagsLogger = Logger(
	{
		"bold": "\033[01m{}\033[00m",
		"italic": "\033[03m{}\033[00m",
		"head": "\033[01m\033[04m{}\033[00m",
		"d": "\033[36m[debug] {}\033[00m",
		"i": "\033[36m[info] {}\033[00m",
		"ok": "\033[32m[success] {}\033[00m",
		"w": "\033[35m[warn] {}\033[00m",
		"e": "\033[31m[error] {}\033[00m",
		"crit": "\033[31m[critical] {}\033[00m",
	}
)
printtagsPrint = printtagsLogger.pprint
printtagsStr = printtagsLogger.pstr


xaLogger = Logger(
	{
		"bold": "\033[01m{}\033[00m",
		"italic": "\033[03m{}\033[00m",
		"head": "\033[01m\033[40m\033[93m TITLE \033[00m {}",
		"d": "\033[01m\033[106m\033[30m DEBUG \033[00m {}",
		"i": "\033[01m\033[46m\033[30m INFO \033[00m {}",
		"ok": "\033[01m\033[42m\033[30m SUCCESS \033[00m {}",
		"w": "\033[01m\033[43m\033[30m WARNING \033[00m {}",
		"e": "\033[01m\033[41m\033[30m ERROR \033[00m {}",
		"crit": "\033[01m\033[101m\033[30m CRITICAL \033[00m {}",
	}
)
xaPrint = xaLogger.pprint
xaStr = xaLogger.pstr


lamuLogger = Logger(
	{
		"bold": "\033[01m{}\033[00m",
		"italic": "\033[03m{}\033[00m",
		"head": "\033[01m\033[04m{}\033[00m",
		"d": "\033[96m   debug\033[00m  : :  {}",
		"i": "\033[36m    info\033[00m  : :  {}",
		"ok": "\033[32m success\033[00m  : :  {}",
		"w": "\033[33m warning\033[00m  : :  {}",
		"e": "\033[31m   error\033[00m  : :  {}",
		"crit": "\033[91mcritical\033[00m  : :  {}",
	}
)
lamuPrint = lamuLogger.pprint
lamuStr = lamuLogger.pstr
