class Session:
	def __init__(self, name: str, time: int, token: str):
		self.name = name
		self.time = time
		self.token = token


	@staticmethod
	def fromJSON(JSON: dict):
		session = Session('', 0, '')
		session.name = JSON['name']
		session.time = JSON['time']
		session.token = JSON['token']
		return session


class Matrix:
	def __init__(self, matrix_id: str, owner: str):
		self.matrix_id = matrix_id
		self.owner = owner
		self.sessions = []


	@staticmethod
	def fromJSON(JSON: dict):
		matrix = Matrix('', '')
		matrix.matrix_id = JSON['matrix_id']
		matrix.owner = JSON['owner']
		for session in JSON['sessions']:
			matrix.sessions.append(Session.fromJSON(session))
		return matrix


class User:
	def __init__(self, username: str, name: str, password_hash: str, sessions: list[Session]=[], matrixes: list[Matrix]=[]):
		self.username = username
		self.name = name
		self.password_hash = password_hash
		self.matrixes = matrixes
		self.sessions = sessions


	@staticmethod
	def fromJSON(JSON: dict):
		print(JSON)
		user = User('', '', '')
		user.username = JSON['username']
		user.name = JSON['name']
		user.password_hash = JSON['password_hash']
		user.matrixes = JSON['matrixes']
		user.sessions = []
		for session in JSON['sessions']:
			user.sessions.append(Session.fromJSON(session))
		return user

