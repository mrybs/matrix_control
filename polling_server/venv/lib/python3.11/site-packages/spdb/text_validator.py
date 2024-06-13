from spdb.restr import REstr
import re


class TextValidator:
	def __init__(self, min: int=4, max: int=64, regexp: str=r'([A-z]|[0-9]|_|-)+'):
		self.min = min
		self.max = max
		self.regexp = regexp


	def check(self, text: str):
		text: REstr = REstr.strOrREstr(text)
		if not text.isMatches(self.regexp):
			return False
		if text.len() > self.max or text.len() < self.min:
			return False
		return True
