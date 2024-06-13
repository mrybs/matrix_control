import sqlite3
import json


class Database:
	def __init__(self, path: str):
		self.path = path


	def create_tables(self, tables_names: list[str]):
		for table_name in tables_names:
			self.execute(f'create table if not exists {table_name}(id text, data text)')


	def execute(self, code: str) -> str:
		database = sqlite3.connect(self.path, isolation_level=None)
		cursor = database.cursor()
		cursor.execute(code)
		result = cursor.fetchall()
		database.commit()
		database.close()
		return result


	@staticmethod
	def object_to_dict(object) -> dict:
		if object is None:
			return {}
		return object.__dict__


	@staticmethod
	def object_to_json(object) -> dict:
		return Database.dict_to_json(Database.object_to_dict(object))


	@staticmethod
	def dict_to_json(Dict) -> dict:
		D = {}
		for key in list(Dict):
			if type(Dict[key]) in [bool, int, float, str]:
				D[key] = Dict[key]
			elif type(Dict[key]) == dict:
				D[key] = Database.dict_to_json(Dict[key])
			elif type(Dict[key]) == list:
				D[key] = []
				for e in Dict[key]:
					D[key].append(Database.object_to_json(e))
			else:
				D[key] = Database.object_to_json(Dict[key])
		return D


	@staticmethod
	def dict_to_object(Class, Dict: dict):
		try:
			return Class(**Dict)
		except TypeError:
			return None


	@staticmethod
	def json_to_object(Class, JSON: dict):
		try:
			return Class.fromJSON(JSON)
		except NameError:
			return Database.dict_to_object(Class, JSON)
		except KeyError:
			return Database.dict_to_object(Class, JSON)


	def read_json(self, name: str, data_id: str) -> dict:
		objects = self.execute(f'select data from {name} where id = \'{data_id}\'')
		if len(objects) == 0:
			return {}
		return json.loads(objects[0][0])


	def read_object(self, Class, name: str, object_id: str):
		return Database.json_to_object(Class, self.read_json(name, object_id))


	def write_json(self, name: str, data_id: str, JSON: dict):
		data = json.dumps(JSON)
		objects = self.execute(f'select data from {name} where id = \'{data_id}\'')
		if len(objects) == 0:
			self.execute(f'insert into {name}(id, data) values(\'{data_id}\', \'{data}\')')
		else:
			self.execute(f'update {name} set data = \'{data}\' where id = \'{data_id}\'')


	def write_object(self, name: str, object_id: str, object: str):
		self.write_json(name, object_id, Database.object_to_json(object))


	def delete_dict(self, name: str, dict_id: str):
		self.execute(f'delete from {name} where id = {dict_id}')


	def delete_json(self, name: str, json_id: str):
		self.delete_dict(name, json_id)


	def delete_object(self, name: str, object_id: str):
		self.delete_dict(name, object_id)
