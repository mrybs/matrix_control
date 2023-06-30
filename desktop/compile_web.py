BUILD_PATH = 'build_web'
SOURCE_PATH = 'web'

import os

def removeComments(text):
	rctext = ''
	lines = text.split('\n')
	for line in lines:
		if not line.startswith('//'):
			rctext+=line+'\n'
	return rctext

if not os.path.exists(BUILD_PATH):
	os.mkdir(BUILD_PATH)

files_names = os.listdir(SOURCE_PATH)
build_file = open(BUILD_PATH + '/build.ino','w');
for file_name in files_names:
	if file_name.endswith('.html') or file_name.endswith('.css') or file_name.endswith('.js'):
		source = open(SOURCE_PATH + '/' + file_name, 'r')
		build = open(BUILD_PATH + '/' + file_name + '.short', 'w')
		source_text = source.read()
		short = removeComments(source_text)
		short = short.replace('\\','\\\\').replace('\n','').replace('\t','').replace('  ',' ').replace('"','\\"')
		build.write(short)
		source.close()
		build.close()

		build_file.write(f'String {file_name.replace(".","_")} = \"{short}\";');

build_file.close()