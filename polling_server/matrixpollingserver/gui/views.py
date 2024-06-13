from django.shortcuts import render
from django.http import HttpResponse
from fm.views import renderFile
import re
import spdb
import json


EFFECTS_SETTINGS = [{
						'slider': 'speed',
						'slider-name': 'Скорость',
						'type': 'slider',
						'slider-value-type': 'degree',
						'slider-max': 500,
						'slider-map-max-to': 50,
						'default-slider': 200
					},{
						'slider': 'hue',
						'checkbox': 'rainbow',
						'slider-name': 'Тон',
						'checkbox-name': 'Переливающийся тон',
						'type': 'slider-checkbox',
						'slider-value-type': 'value',
						'slider-max': 360,
						'slider-map-max-to': 255,
						'default-slider': 0,
						'default-checkbox': False
					},{
						'slider': 'chance',
						'slider-name': 'Шанс',
						'type': 'slider',
						'slider-value-type': 'percent',
						'slider-max': 100,
						'slider-map-max-to': 100,
						'default-slider': 20
					},{
						'slider': 'saturation',
						'slider-name': 'Насыщенность',
						'type': 'slider',
						'slider-value-type': 'percent',
						'slider-max': 100,
						'slider-map-max-to': 255,
						'default-slider': 100
					}]
EFFECTS = [('off','<выключено>',[]),('rainbow','Радуга',['speed', 'saturation']),('confetti','Конфетти',['speed', 'saturation']),
		   ('ball','Мяч',['hue', 'speed', 'saturation']),('snowing','Снегопад', ['hue', 'speed', 'chance', 'saturation']),('sinusoid','Синусоида', ['hue', 'speed', 'saturation']),
		   ('doubleSinusoid','Двойная синусоида', ['hue', 'speed', 'saturation'])]


quotes = spdb.Quotes(open_quote=spdb.REstr.fromStr(r'holder\(name="'), close_quote=spdb.REstr.fromStr(r'"\)'), validator=spdb.TextValidator(min=3))

# Create your views here.
def matrixControl(request, matrix_id, url):
	if matrix_id == '':
		return HttpResponse(quotes.replace_all(open('pages/index.html')))
	content_type = 'text/plain'
	if url.endswith('.html'):
		content_type = 'text/html'
	elif url.endswith('.css'):
		content_type = 'text/css'
	elif url.endswith('.js'):
		content_type = 'text/javascript'
	elif url.endswith('.ntml'):
		content_type = 'text/ntml'
	if '..' in url:
		return HttpResponse('<b>403 - Forbidden</b><br><br>MMatrix')
	return renderFile(f'matrix_control/{url}', renderer=lambda text: makeMatrixControlPage(text, matrix_id), content_type=content_type)


def checkPages(text: str, pages_ids: list[str]):
	for page_id in pages_ids:
		if checkPage(text, page_id):
			return True
	return False


def checkPage(text: str, page_id: str):
	return quotes.replace(spdb.REstr.fromStr(text), [{page_id: ''}]).toStr() != text


def makeMatrixControlPage(text: str, matrix_id: str, data: list[dict]=[]):
	data += makeEffects(EFFECTS)
	data += makeEffectsSettings(EFFECTS_SETTINGS)
	data.append({'matrix_id': matrix_id})
	return quotes.replace_all(spdb.REstr.fromStr(text), data).toStr()


def makeEffectsSettings(effects_settings: list[dict]):
	defaultsJS = ''
	onChangeJS = ''
	changeParamsJS = ''
	reloadJS = ''
	showEffectSettingsJS = ''
	for effect_settings in effects_settings:
		if effect_settings['type'] in ['slider', 'slider-checkbox']:
			defaultsJS += f'let {effect_settings["slider"]}={effect_settings["default-slider"]};'
		if effect_settings['type'] in ['checkbox', 'slider-checkbox']:
			defaultsJS += f'let {effect_settings["checkbox"]}={str(effect_settings["default-checkbox"]).lower()};'

		if effect_settings['type'] in ['slider', 'slider-checkbox']:
			onChangeJS += f'let {effect_settings["slider"]}SliderLabel=document.getElementById("{effect_settings["slider"]}Label");'
			onChangeJS += F'let {effect_settings["slider"]}Slider=document.getElementById("{effect_settings["slider"]}");'
			if effect_settings['slider-value-type'] == 'value':
				onChangeJS += f'{effect_settings["slider"]}SliderLabel.innerHTML={effect_settings["slider"]}Slider.value;'
			elif effect_settings['slider-value-type'] == 'percent':
				onChangeJS += f'{effect_settings["slider"]}SliderLabel.innerHTML={effect_settings["slider"]}Slider.value+"%";'
			elif effect_settings['slider-value-type'] == 'degree':
				onChangeJS += f'{effect_settings["slider"]}SliderLabel.innerHTML={effect_settings["slider"]}Slider.value+"°";'
			onChangeJS += f'{effect_settings["slider"]} = {effect_settings["slider"]}Slider.value*{effect_settings["slider-map-max-to"]/effect_settings["slider-max"]};'
		if effect_settings['type'] in ['checkbox', 'slider-checkbox']:
			onChangeJS += f'let {effect_settings["checkbox"]}CB = document.getElementById("{effect_settings["checkbox"]}");'
			onChangeJS += f'{effect_settings["checkbox"]} = {effect_settings["checkbox"]}CB.checked;'

		if effect_settings['type'] in ['slider', 'slider-checkbox']:
			changeParamsJS += f'"{effect_settings["slider"]}": {effect_settings["slider"]},'
		if effect_settings['type'] in ['checkbox', 'slider-checkbox']:
			changeParamsJS += f'"{effect_settings["checkbox"]}": {effect_settings["checkbox"]},'

		if effect_settings['type'] in ['slider', 'slider-checkbox']:
			reloadJS += f'{effect_settings["slider"]} = effectSettings["{effect_settings["slider"]}"];'
			reloadJS += f'let {effect_settings["slider"]}SliderLabel = document.getElementById("{effect_settings["slider"]}Label");'
			reloadJS += f'{effect_settings["slider"]}Slider.value = {effect_settings["slider"]}/{effect_settings["slider-map-max-to"]/effect_settings["slider-max"]};'
			if effect_settings['slider-value-type'] == 'value':
				reloadJS += f'{effect_settings["slider"]}SliderLabel.innerHTML={effect_settings["slider"]}Slider.value;'
			elif effect_settings['slider-value-type'] == 'percent':
				reloadJS += f'{effect_settings["slider"]}SliderLabel.innerHTML={effect_settings["slider"]}Slider.value+"%";'
			elif effect_settings['slider-value-type'] == 'degree':
				reloadJS += f'{effect_settings["slider"]}SliderLabel.innerHTML={effect_settings["slider"]}Slider.value+"°";'
		if effect_settings['type'] in ['checkbox', 'slider-checkbox']:
			reloadJS += f'{effect_settings["checkbox"]} = !!(effectSettings["{effect_settings["checkbox"]}"]-0);'
			reloadJS += f'let {effect_settings["checkbox"]}CB = document.getElementById("{effect_settings["checkbox"]}");'
			reloadJS += f'{effect_settings["checkbox"]}CB.checked = {effect_settings["checkbox"]};'

		if effect_settings['type'] in ['slider', 'slider-checkbox']:
			showEffectSettingsJS += f'let {effect_settings["slider"]}SliderLabel = document.getElementById("{effect_settings["slider"]}Label");\n'
			showEffectSettingsJS += f'let {effect_settings["slider"]}Slider = document.getElementById("{effect_settings["slider"]}Slider");\n'
		if effect_settings['type'] in ['checkbox', 'slider-checkbox']:
			showEffectSettingsJS += f'let {effect_settings["checkbox"]}Checkbox = document.getElementById("{effect_settings["checkbox"]}Checkbox");\n'
			showEffectSettingsJS += f'let {effect_settings["checkbox"]}CB = document.getElementById("{effect_settings["checkbox"]}");\n'

	for effect_settings in effects_settings:
		if effect_settings['type'] == 'slider':
			showEffectSettingsJS += """
				if(settings[effectCombobox.value].indexOf(\""""+effect_settings["slider"]+"""\")!=-1){
					"""+effect_settings["slider"]+"""Slider.style.display="flex";
				}else{
					"""+effect_settings["slider"]+"""Slider.style.display="none";
				}
			"""
		elif effect_settings['type'] == 'checkbox':
			showEffectSettingsJS += 'if(settings[effectCombobox.value].indexOf("'+effect_settings["checkbox"]+'")!=-1){'+effect_settings["checkbox"]+'Checkbox.style.display="flex";}else{'+effect_settings["checkbox"]+'Checkbox.style.display="none";}'
		elif effect_settings['type'] == 'slider-checkbox':
			showEffectSettingsJS += """
				    if(settings[effectCombobox.value].indexOf(\""""+effect_settings["slider"]+"""\")!=-1){
				    	"""+effect_settings["checkbox"]+"""Checkbox.style.display="flex";
				    	if(!"""+effect_settings["checkbox"]+"""CB.checked){
				    		"""+effect_settings["slider"]+"""Slider.style.display="flex";
				    	}
				    	else{
				    		"""+effect_settings["slider"]+"""Slider.style.display="none";
				   		}
				    }else{
				    	"""+effect_settings["slider"]+"""Slider.style.display = 'none';
				    	"""+effect_settings["checkbox"]+"""Checkbox.style.display = 'none';
				    }
			"""

	defaultsJS = defaultsJS.replace('\n', '').replace('\t', '').replace('  ', ' ')
	onChangeJS = onChangeJS.replace('\n', '').replace('\t', '').replace('  ', ' ')
	changeParamsJS = changeParamsJS.replace('\n', '').replace('\t', '').replace('  ', ' ')
	reloadJS = reloadJS.replace('\n', '').replace('\t', '').replace('  ', ' ')
	showEffectSettingsJS = showEffectSettingsJS.replace('\n', '').replace('\t', '').replace('  ', ' ')
	return [{'defaultsJS': defaultsJS}, {'onChangeJS': onChangeJS}, {'changeParamsJS': changeParamsJS}, {'reloadJS': reloadJS}, {'showEffectSettingsJS': showEffectSettingsJS}]



def makeEffects(effects: list[tuple[str,str,list[str]]]):
	settings = []
	ntml = ''
	settingsJS = {}
	for effect in effects:
		ntml += 'option(value="'+effect[0]+'"){'+effect[1]+'}'
		settingsJS[effect[0]] = effect[2]
	return [{'effects': ntml}, {'settings': json.dumps(settingsJS)}]