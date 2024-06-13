from django.shortcuts import render
from django.http import HttpResponse
import ntml
from ntml import errors
from parglare import exceptions

# Create your views here.

def getFile(request):
	url = ''
	content_type = 'text/plain'
	raw = False
	if 'url' in request.GET:
		url = request.GET['url']
	if 'content_type' in request.GET:
		content_type = request.GET['content_type']
	if raw in request.GET:
		raw = bool(request.GET['raw'])
	return renderFile(url, content_type=content_type, raw=raw)


def renderFile(url: str, renderer=lambda text: text, content_type='text/plain', raw=False):
	if url == '':
		return HttpResponse(ntmlc(renderer(open('pages/docs/fm_guide.ntml', 'r').read())))
	if '..' in url:
		return HttpResponse(renderer('<b>403 - Forbidden</b><br><br>MMatrix'))
	try:
		if not raw:
			if content_type == 'text/ntml':
				return HttpResponse(ntmlc(renderer(open(f'pages/{url}', 'r').read()), f'pages/{url}'), content_type='text/html')
			else:
				return HttpResponse(renderer(open(f'pages/{url}', 'r').read()), content_type=content_type)
		else:
			return HttpResponse(open(f'pages/{url}', 'r').read(), content_type=content_type)
	except IsADirectoryError:
		try:
			if not raw:
				if content_type == 'text/ntml':
					return HttpResponse(ntmlc(renderer(open(f'pages/{url}/index.html', 'r').read()), f'pages/{url}'), content_type='text/html')
				else:
					return HttpResponse(renderer(open(f'pages/{url}/index.html', 'r').read(), f'pages/{url}'), content_type=content_type)
			else:
				return HttpResponse(open(f'pages/{url}/index.html', 'r').read(), content_type=content_type)
		except FileNotFoundError:
			return HttpResponse(renderer('<b>404 - Not Found</b><br><br>MMatrix'))
	except FileNotFoundError:
		return HttpResponse(renderer('<b>404 - Not Found</b><br><br>MMatrix'))


def ntmlc(text: str, file: str) -> str:
	try:
		print(ntml.compile(text, file))
		return ntml.compile(text, file)
	except exceptions.ParseError as pe:
		print()
		nl, ns, dt = str(pe).split(":", 2)
		nl = int(nl.split()[-1])
		ns = int(ns)
		errors.print_parse_error((nl, ns), file, dt)
	return 'Error during parsing ntml file'
