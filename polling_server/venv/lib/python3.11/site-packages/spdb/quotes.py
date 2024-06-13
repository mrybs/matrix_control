from spdb.text_validator import TextValidator
from spdb.restr import REstr
import re


class Quotes:
	def __init__(self, open_quote: REstr=REstr.fromStr('<%'), close_quote: REstr=REstr.fromStr('%>'), validator: TextValidator=TextValidator()):
		self.open_quote: REstr = open_quote
		self.close_quote: REstr = close_quote
		self.validator: TextValidator = validator


	def replace_all(self, text: REstr, data: dict) -> REstr:
		return self.clean(self.replace(REstr.strOrREstr(text), data))


	def replace(self, text: REstr, data: dict) -> REstr:
		for i, dat in enumerate(data):
			i_dat: str = list(dat)[0]
			if not self.validator.check(REstr.fromStr(i_dat)):
				#continue
				pass
			text.replace(fr'{self.open_quote.toStr()}\s*{i_dat}\s*{self.close_quote.toStr()}', dat[i_dat])
		return text


	def clean(self, text: REstr) -> REstr:
		return text.toCleaned(fr'{self.open_quote.toStr()}.*{self.close_quote.toStr()}')


	def count(self, text: REstr) -> int:
		return text.matches(fr'{self.open_quote.toStr()}.*{self.close_quote.toStr()}')


	def count_trash(self, text: str, data: dict) -> int:
		i: int = self.count(text)
		for i, dat in enumerate(data):
			i_dat: str = list(dat)[0]
			if not self.validator.check(i_dat):
				continue
			if text.isReplacing(fr'{self.open_quote.toStr()}\s*{i_dat}\s*{self.close_quote.toStr()}', dat[i_dat]):
				i -= 1
		return i