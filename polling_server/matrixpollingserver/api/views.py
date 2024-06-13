from django.shortcuts import render
from django.http import HttpResponse
from classes import *
import datetime, time
import sqlite3
import hashlib
import json
import random
import re
import spdb

# Create your views here.

DB = spdb.Database('db.sqlite3')
DB.create_tables(['users', 'matrixes'])

tokenGen = spdb.TokenGenerator('mx')
textValidator = spdb.TextValidator()

def index(request):
	return HttpResponse('{"text": "Hello, world!"}')


def makeRequest(request):
	if not 'matrix_id' in list(request.GET):
		return HttpResponse('{"error": "matrix id not defined"}')
	GET = request.GET.dict()
	file = open(f'requests/{GET["matrix_id"]}.request', 'a')
	GET.pop('matrix_id')
	file.write(''.join(dictToArgs(GET)[1:])+'\n')
	file.close();
	return HttpResponse('{"status": "ok"}')


def poll(request):
	if not 'matrix_token' in list(request.GET):
		return HttpResponse('{"error": "matrix token not defined"}')
	if not validMatrixToken(request.GET['matrix_token']):
		return HttpResponse('{"error": "matrix token is not valid"}')
	file = None
	try:
		file = open(f'requests/{spdb.TokenGenerator.parse_token(request.GET["matrix_token"])["ID"]}.request', 'r+')
	except FileNotFoundError:
		return HttpResponse('')
	requests = file.read()
	file.truncate(0)
	file.close()
	return HttpResponse(requests)


def regUser(request):
	if not 'id' in list(request.GET):
		return HttpResponse('{"error": "id is not defined"}')
	if not DB.read_object(User, 'users', request.GET['id']) is None:
		return HttpResponse('{"error": "user is registered"}')
	if not 'username' in list(request.GET):
		return HttpResponse('{"error": "username is not defined"}')
	if not 'password' in list(request.GET):
		return HttpResponse('{"error": "password is not defined"}')
	if not 'session_name' in list(request.GET):
		return HttpResponse('{"error": "session name is not defined"}')
	if not textValidator.check(spdb.REstr.fromStr(request.GET['id'])):
		return HttpResponse('{"error": "id is not correct"}')
	if not textValidator.check(spdb.REstr.fromStr(request.GET['password'])):
		return HttpResponse('{"error": "password is not correct"}')

	user = User(request.GET['id'], request.GET['username'], spdb.utils.sha256(request.GET['password']))
	user.sessions.append(Session(
		request.GET['session_name'], get_now_unixtime(),
		tokenGen.gen('fa', request.GET['id'], spdb.utils.sha256(request.GET['password'])
	)))
	DB.write_object('users', request.GET['id'], user)
	return HttpResponse(json.dumps(spdb.Database.object_to_json(user)))


def regMatrix(request):
	if not 'token' in list(request.GET):
		return HttpResponse('{"error": "token is not defined"}')
	if not 'matrix_id' in list(request.GET):
		return HttpResponse('{"error": "matrix id is not defined"}')
	if not 'session_name' in list(request.GET):
		return HttpResponse('{"error": "session name is not defined"}')
	if not DB.read_object(Matrix, 'matrixes', request.GET['matrix_id']) is None:
		return HttpResponse('{"error": "matrix is registered"}')
	if not validUserToken(request.GET['token']):
		return HttpResponse('{"error": "token is not valid"}')

	matrix = Matrix(request.GET['matrix_id'], spdb.TokenGenerator.parse_token(request.GET['token'])['ID'])
	user = DB.read_object(User, 'users', matrix.owner)
	user.matrixes.append(request.GET['matrix_id'])
	DB.write_object('users', matrix.owner, user)
	matrix.sessions.append(Session(
		request.GET['session_name'], get_now_unixtime(),
		tokenGen.gen('fa', request.GET['matrix_id'], spdb.utils.sha256(request.GET['token'])
	)))
	DB.write_object('matrixes', request.GET['matrix_id'], matrix)
	return HttpResponse(json.dumps(spdb.Database.object_to_json(matrix)))


def deleteMatrix(request):
	if not 'token' in list(request.GET):
		return HttpResponse('{"error": "token is not defined"}')
	if not 'id' in list(request.GET):
		return HttpResponse('{"error": "id is not defined"}')

	matrix = DB.read_object(Matrix, 'matrixes', request.GET['id'])

	if matrix is None:
		return HttpResponse('{"status": "ok"}')
	if checkUserToken(matrix['owner'], request.GET['token']):
		return HttpResponse('{"error": "you have not permissions to delete matrix"}')
	user = DB.read_object(User, 'users', matrix.owner)
	user.matrixes.remove(request.GET['matrix_id'])
	DB.write_object('users', matrix.owner, user)
	DB.delete_object('matrixes', request.GET['id'])
	return HttpResponse('{"status": "ok"}')


def setUserPass(request):
	if not 'id' in list(request.GET):
		return HttpResponse('{"error": "id is not defined"}')
	if DB.read_object(User, 'users', request.GET['id']) is None:
		return HttpResponse('{"error": "user is not registered"}') 
	if not 'old_password' in list(request.GET):
		return HttpResponse('{"error": "old_password is not defined"}')
	if not 'new_password' in list(request.GET):
		return HttpResponse('{"error": "new_password is not defined"}')
	if not textValidator.check(request.GET['new_password']):
		return HttpResponse('{"error": "new_password is not correct"}')

	user = DB.read_object(User, 'users', request.GET['id'])
	
	if user.password_hash != spdb.utils.sha256(request.GET['old_password']):
		return HttpResponse('{"error": "old password is not correct"}') 

	user.password_hash = spdb.utils.sha256(request.GET['new_password'])
	user.sessions = [
		Session(
			'DefaultSession', 0,
			tokenGen.gen('fa', request.GET['id'], spdb.utils.sha256(request.GET['new_password']))
		)
	]
	DB.write_object('users', request.GET['id'], user)
	return HttpResponse(json.dumps(spdb.Database.object_to_json(user)))


def newUserSession(request):
	if not 'id' in list(request.GET):
		return HttpResponse('{"error": "id is not defined"}')
	if DB.read_object(User, 'users', request.GET['id']) is None:
		return HttpResponse('{"error": "user is not registered"}') 
	if not 'password' in list(request.GET):
		return HttpResponse('{"error": "password is not defined"}')
	if not 'session_name' in list(request.GET):
		return HttpResponse('{"error": "session name is not defined"}')

	user = DB.read_object(User, 'users', request.GET['id'])
	
	if user.password_hash != spdb.utils.sha256(request.GET['password']):
		return HttpResponse('{"error": "password is not correct"}') 

	session = Session(
		request.GET['session_name'], get_now_unixtime(),
		tokenGen.gen('fa', request.GET['id'], spdb.utils.sha256(request.GET['password']))
	)
	user.sessions.append(session)
	DB.write_object('users', request.GET['id'], user)
	return HttpResponse(json.dumps(spdb.Database.object_to_json(session)))


def newMatrixSession(request):
	if not 'token' in list(request.GET):
		return HttpResponse('{"error": "token is not defined"}')
	if not 'matrix_id' in list(request.GET):
		return HttpResponse('{"error": "matrix id is not defined"}')
	if not 'session_name' in list(request.GET):
		return HttpResponse('{"error": "session name is not defined"}')

	matrix = DB.read_object(Matrix, 'matrixes', request.GET['matrix_id'])
	if matrix is None:
		return HttpResponse('{"error": "matrix is not registered"}')
	if matrix.owner != spdb.TokenGenerator.parse_token(request.GET['token'])['ID']:
		return HttpResponse('{"error": "you have not permissions to create new matrix session"}')

	session = Session(
		request.GET['session_name'], get_now_unixtime(),
		tokenGen.gen('fa', request.GET['matrix_id'], spdb.TokenGenerator.parse_token(request.GET['token'])['ID'])
	)
	matrix.sessions.append(session)
	DB.write_object('matrixes', request.GET['matrix_id'], matrix)
	return HttpResponse(json.dumps(spdb.Database.object_to_json(session)))


def getAllMatrixes(request):
	if not 'user_id' in list(request.GET):
		return HttpResponse('{"error": "user id is not defined"}')

	user = DB.read_object(User, 'users', request.GET['user_id'])
	if user is None:
		return HttpResponse('{"error": "user is not registered"}')

	return HttpResponse(json.dumps({'matrixes': user.matrixes}))



def exitCurrentSession(request):
	if not 'token' in list(request.GET):
		return HttpResponse('{"error": "token is not defined"}')
	if not validUserToken(request.GET['token']):
		return HttpResponse('{"error": "token is not valid}')

	user = DB.read_object(User, 'users', spdb.TokenGenerator.parse_token(request.GET['token'])['ID'])
	for i in range(len(user.sessions)):
		if user.sessions[i].token == request.GET['token']:
			user.sessions.pop(i)
	DB.write_object('users', spdb.TokenGenerator.parse_token(request.GET['token'])['ID'], user)
	return HttpResponse('{"status": "ok"}')


def exitCurrentMatrixSession(request):
	if not 'matrix_token' in list(request.GET):
		return HttpResponse('{"error": "matrix token is not defined"}')
	if not validMatrixToken(request.GET['matrix_token']):
		return HttpResponse('{"error": "matrix token is not valid}')

	matrix = DB.read_object(Matrix, 'matrixes', spdb.TokenGenerator.parse_token(request.GET['matrix_token'])['ID'])
	for i in range(len(matrix.sessions)):
		if matrix.sessions[i].token == request.GET['matrix_token']:
			matrix.sessions.pop(i)
	DB.write_object('matrixes', spdb.TokenGenerator.parse_token(request.GET['matrix_token'])['ID'], matrix)
	return HttpResponse('{"status": "ok"}')


def exitAllMatrixSessions(request):
	if not 'token' in list(request.GET):
		return HttpResponse('{"error": "token is not defined"}')
	if not validUserToken(request.GET['token']):
		return HttpResponse('{"error": "token is not valid}')
	if not 'matrix_id' in list(request.GET):
		return HttpResponse('{"error": "matrix id is not defined"}')

	matrix = DB.read_object(Matrix, 'matrixes', request.GET['matrix_id'])
	if matrix is None:
		return HttpResponse('{"error": "matrix is not registered"}')

	matrix.sessions = []
	DB.write_object('matrixes', request.GET['matrix_id'], matrix)
	return HttpResponse('{"status": "ok"}')


def exitAllSessions(request):
	if not 'id' in list(request.GET):
		return HttpResponse('{"error": "id is not defined"}')
	if DB.read_object(User, 'users', request.GET['id']) is None:
		return HttpResponse('{"error": "user is not registered"}') 
	if not 'password' in list(request.GET):
		return HttpResponse('{"error": "password is not defined"}')

	user = DB.read_object(User, 'users', request.GET['id'])
	
	if user.password_hash != spdb.utils.sha256(request.GET['password']):
		return HttpResponse('{"error": "password is not correct"}') 

	user.sessions = []
	DB.write_object('users', request.GET['id'], user)
	return HttpResponse('{"status": "ok"}')


def checkUserToken(user_id: str, token: str):
	for session in DB.read_object(User, 'users', user_id).sessions:
		if token == session.token:
			return True
	return False


def validUserToken(token: str):
	return checkUserToken(spdb.TokenGenerator.parse_token(token)['ID'], token)


def checkMatrixToken(matrix_id: str, token: str):
	for session in DB.read_object(Matrix, 'matrixes', matrix_id).sessions:
		if token == session.token:
			return True
	return False


def validMatrixToken(token: str):
	return checkMatrixToken(spdb.TokenGenerator.parse_token(token)['ID'], token)


def dictToArgs(D: dict):
	args = ''
	for key in list(D):
		args+=f'&{key}={D[key]}'
	return args.replace('&', '?', 1)


def get_now_unixtime():
	return int(time.mktime(datetime.datetime.now().timetuple()))
