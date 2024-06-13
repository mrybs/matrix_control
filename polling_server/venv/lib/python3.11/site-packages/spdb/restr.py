import re


class REstr:
	def __init__(self):
		self.string: str = ''


	def replace(self, find: str, to: str):
		find: REstr = REstr.strOrREstr(find)
		to: REstr = REstr.strOrREstr(to)
		self.string = re.sub(find.string, to.string, self.string)
		return self


	def toReplaced(self, find: str, to: str):
		find: REstr = REstr.strOrREstr(find)
		to: REstr = REstr.strOrREstr(to)
		return REstr.fromStr(re.sub(find.string, to.string, self.string))


	def clean(self, find: str):
		find: REstr = REstr.strOrREstr(find)
		self.replace(find, '')
		return self


	def toCleaned(self, find: str):
		find: REstr = REstr.strOrREstr(find)
		return self.toReplaced(find, '')


	def isReplacing(self, find: str, to: str='') -> bool:
		find: REstr = REstr.strOrREstr(find)
		to: REstr = REstr.strOrREstr(to)
		return self.string != self.toReplaced(find, to)


	def isMatches(self, find: str) -> bool:
		find: REstr = REstr.strOrREstr(find)
		return self.toReplaced(find, '').isEmpty()


	def matches(self, find: str) -> int:
		find: REstr = REstr.strOrREstr(find)
		return len(self.match(find))


	def match(self, find: str) -> re.Match:
		find: REstr = REstr.strOrREstr(find)
		return re.match(find.string, self.string)


	def setFromStr(self, string: str) -> None:
		self.string = string


	def toStr(self) -> str:
		return self.string


	def len(self) -> int:
		return len(self.string)


	def isEmpty(self) -> bool:
		return self.string == ''


	def at(self, index):
		if type(index) == int:
			return REstr.fromStr(self.string[index])
		elif type(index) == tuple:
			if len(index) == 1:
				return REstr.fromStr(self.string[index[0]])
			elif len(index) == 2:
				return REstr.fromStr(self.string[index[0]:index[1]])
			elif len(index) == 3:
				return REstr.fromStr(self.string[index[0]:index[1]:index[2]])
		return REstr()


	def join(self, array: list):
		return REstr.fromStr(self.string.join(array))


	def convertFrom(self, var):
		return REstr.fromStr(str(var))


	def convertTo(self, Class):
		return Class(self.string)


	@staticmethod
	def strOrREstr(string):
		if type(string) == str:
			return REstr.fromStr(string)
		elif type(string) == REstr:
			return string
		return REstr()


	@staticmethod
	def fromStr(string: str):
		restr = REstr()
		restr.string = string
		return restr