tippy('#paint-tool-options', {
	content: `
	<div id="paint-tools-options" style="padding-top: 20px">
		<div class="slider" id="brushSizeSlider">
			<div class="sliderLabel" id="brushSizeLabel">1пкс</div>
			<input class="sliderMain" type="range" id="brushSize" name="hue" min="1" max="16" value="1" onchange="updatePaintToolsOptions()">
			<div class="label" id="brushSizeTitle">Размер кисти</div><br>
		</div>
		<div class="slider" id="opacitySlider">
			<div class="sliderLabel" id="opacityLabel">100%</div>
			<input class="sliderMain" type="range" id="opacity" name="hue" min="0" max="100" value="100" onchange="updatePaintToolsOptions()">
			<div class="label" id="opacityTitle">Прозрачность</div><br>
		</div>
	</div>`,
	interactive: true,
	allowHTML: true,
	theme: 'light-border',
	animation: 'shift-away',
	arrow: tippy.roundArrow
})
function updatePaintToolsOptions(){
	let brushSizeSlider = document.getElementById('brushSize')
	let opacitySlider = document.getElementById('opacity')

	options['brushSize'] = brushSizeSlider.value
	options['opacity'] = opacitySlider.value/100

	let brushSizeLabel = document.getElementById('brushSizeLabel')
	let opacityLabel = document.getElementById('opacityLabel')

	brushSizeLabel.innerText = brushSizeSlider.value + 'пкс'
	opacityLabel.innerText = opacitySlider.value + '%'
}

function icthc(r, g, b){
	let hr = r.toString(16)
	let hg = g.toString(16)
	let hb = b.toString(16)
	if(hr.length == 1) hr = '0' + hr
	if(hg.length == 1) hg = '0' + hg
	if(hb.length == 1) hb = '0' + hb
	return '#'+hr+hg+hb
}

websocket.addEventListener("open", (event) => {
	websocket.send('get_matrix')
});


websocket.addEventListener('message', (event) => {
	let i = 0
	event.data.stream().getReader().read().then((read) => {
		for(let y = 0; y < HEIGHT; y++){
			for(let x = 0; x < WIDTH; x++){
				pixels[y][x] = icthc(read.value[i*3], read.value[i*3+1], read.value[i*3+2])
				i++
			}
		}
	})
})


eBrush()

setInterval(() => {
	render()
}, 6)

setInterval(() => {
	if(play) websocket.send('get_matrix')
}, 1000/20) 
