const WIDTH = 16;
const HEIGHT = 16;

class Vector2{
	constructor(x, y){
		this.x = x;
		this.y = y;
	}
	toString() {
		return this.x+' '+this.y;
	}
}

let canvasBox = document.getElementById('imageDrawCanvasBox');
let colorPicker = document.getElementById('imageDrawColorPicker');
let canvas = document.getElementById('imageDrawCanvas');
canvas.width = canvasBox.offsetWidth - 30;
canvas.height = canvas.width/WIDTH*HEIGHT;
let ctx = canvas.getContext('2d');

let palleteCanvas = document.getElementById('palleteCanvas');
palleteCanvas.width = canvasBox.offsetWidth - 30;
palleteCanvas.height = palleteCanvas.width/4;
let pctx = palleteCanvas.getContext('2d');

var cScale = 1
var pixels = []
var play = false
var pallete = ['#ffffff', '#7f7f7f', '#000000', '#f07088', '#ff3f7f', '#ff0000', '#ff3000', '#ba2a0d', '#ffff00', '#fad818', '#00ff00', '#30e850', '#00ffff', '#54c4ff', '#0000ff', '#7f00ff'] 


let isPressed = false;
let moveOnPixel = new Vector2(-1, -1);
let figure = [];
let figureType = null;
let cursor = new Vector2(-1, -1);
let options = {
	brushSize: 1,
	opacity: 1
};

for(let y = 0; y < HEIGHT; y++){
	pixels.push([]);
	for(let x = 0; x < WIDTH; x++){
		pixels[y][x] = '#000000';
	}
}

function copyPixels(){
	let pxls = []
	for(let y = 0; y < HEIGHT; y++){
		pxls.push([]);
		for(let x = 0; x < WIDTH; x++){
			pxls[y].push(pixels[y][x]);
		}
	}
	return pxls
}
function eqPixels(pixels1, pixels2){
	for(let y = 0; y < HEIGHT; y++){
		for(let x = 0; x < WIDTH; x++){
			if(pixels1[y][x] != pixels2[y][x])
				return false
		}
	}
	return true
}

var prevs = [copyPixels()]
var selectedPrev = 0


function opacityRGB(opacity, fcolor, bcolor){
	let r = Math.round(parseInt(fcolor.slice(1, 3), 16)*opacity+parseInt(bcolor.slice(1, 3), 16)*(1-opacity)).toString(16);
	let g = Math.round(parseInt(fcolor.slice(3, 5), 16)*opacity+parseInt(bcolor.slice(3, 5), 16)*(1-opacity)).toString(16);
	let b = Math.round(parseInt(fcolor.slice(5, 7), 16)*opacity+parseInt(bcolor.slice(5, 7), 16)*(1-opacity)).toString(16);
	if(r.length % 2 != 0) r = '0' + r;
	if(g.length % 2 != 0) g = '0' + g;
	if(b.length % 2 != 0) b = '0' + b;
	return '#'+r+g+b;
}

canvas.addEventListener('mouseup', function(){
	isPressed = false
	moveOnPixel.x = -1
	moveOnPixel.y = -1
	prevs = prevs.slice(0, selectedPrev)
	prevs.push(copyPixels())
	selectedPrev++
})
canvas.addEventListener('mousedown', function(e){
	isPressed = true;
	let pos = windowToCanvas(canvas, e.clientX, e.clientY);
	moveOnPixel.x = Math.floor(pos.x/(canvas.width/WIDTH));
	moveOnPixel.y = Math.floor(pos.y/(canvas.height/HEIGHT));
	if(mode == 'brush'){
		for(let y = 0; y < options['brushSize']; y++){
			for(let x = 0; x < options['brushSize']; x++){
				let posx = Math.round(pos.x/(canvas.width/WIDTH)-options['brushSize']/2+x,1);
				let posy = Math.round(pos.y/(canvas.height/HEIGHT)-options['brushSize']/2+y,1);
				if(posx >= 0 && posx < WIDTH && posy >= 0 && posy < HEIGHT)
					pixels[posy][posx]=opacityRGB(options['opacity'], colorPicker.value, pixels[posy][posx]);
			}
		}
	}else if(mode == 'eraser'){
		for(let y = 0; y < options['brushSize']; y++){
			for(let x = 0; x < options['brushSize']; x++){
				let posx = Math.round(pos.x/(canvas.width/WIDTH)-options['brushSize']/2+x,1);
				let posy = Math.round(pos.y/(canvas.height/HEIGHT)-options['brushSize']/2+y,1);
				if(posx >= 0 && posx < WIDTH && posy >= 0 && posy < HEIGHT)
					pixels[posy][posx]=opacityRGB(options['opacity'], '#000000', pixels[posy][posx]);
			}
		}
	}else if(mode == 'fill'){
		for(let y = 0; y < HEIGHT; y++){
			for(let x = 0; x < WIDTH; x++){
				pixels[y][x] = opacityRGB(options['opacity'], colorPicker.value, pixels[y][x]);
			}
		}
	}else if(mode == 'eye-dropper'){
		colorPicker.value=pixels[Math.floor(pos.y/(canvas.height/HEIGHT),1)][Math.floor(pos.x/(canvas.width/WIDTH),1)];
		colorPicker.dispatchEvent(new Event('input', { bubbles: true }));
		eBrush();
	}else if(mode == 'square'){
		figure.push(new Vector2(Math.floor(pos.x/(canvas.width/WIDTH),1), Math.floor(pos.y/(canvas.height/HEIGHT),1)))
		if(figure.length == 2){
			if(figureType != 'square') figure = [];
			else{
				for(let y = Math.min(figure[0].y, figure[1].y); y < Math.max(figure[0].y, figure[1].y)+1; y++){
					for(let x = Math.min(figure[0].x, figure[1].x); x < Math.max(figure[0].x, figure[1].x)+1; x++){
						pixels[y][x] = opacityRGB(options['opacity'], colorPicker.value, pixels[y][x]);
					}
				}
				figure = [];
				figureType = null;
			}
		}
		figureType = 'square';
	}
})
canvas.addEventListener('mousemove', function(e){
	let pos = windowToCanvas(canvas, e.clientX, e.clientY);
	if(isPressed && (moveOnPixel.x != Math.floor(pos.x/(canvas.width/WIDTH)) || moveOnPixel.y != Math.floor(pos.y/(canvas.height/HEIGHT)))){
		if(mode == 'brush'){
			for(let y = 0; y < options['brushSize']; y++){
				for(let x = 0; x < options['brushSize']; x++){
					let posx = Math.round(pos.x/(canvas.width/WIDTH)-options['brushSize']/2+x,1);
					let posy = Math.round(pos.y/(canvas.height/HEIGHT)-options['brushSize']/2+y,1);
					if(posx >= 0 && posx < WIDTH && posy >= 0 && posy < HEIGHT)
						pixels[posy][posx]=opacityRGB(options['opacity'], colorPicker.value, pixels[posy][posx]);
				}
			}
		}else if(mode == 'eraser'){
			for(let y = 0; y < options['brushSize']; y++){
				for(let x = 0; x < options['brushSize']; x++){
					let posx = Math.round(pos.x/(canvas.width/WIDTH)-options['brushSize']/2+x,1);
					let posy = Math.round(pos.y/(canvas.height/HEIGHT)-options['brushSize']/2+y,1);
					if(posx >= 0 && posx < WIDTH && posy >= 0 && posy < HEIGHT)
						pixels[posy][posx]=opacityRGB(options['opacity'], '#000000', pixels[posy][posx]);
				}
			}
		}else if(mode == 'fill'){
			for(let y = 0; y < HEIGHT; y++){
				for(let x = 0; x < WIDTH; x++){
					pixels[y][x] = opacityRGB(options['opacity'], colorPicker.value, pixels[y][x]);
				}
			}
		}else if(mode == 'eye-dropper'){
			colorPicker.value=pixels[Math.round(pos.y/(canvas.height/HEIGHT),1)][Math.round(pos.x/(canvas.width/WIDTH),1)];
			colorPicker.dispatchEvent(new Event('input', { bubbles: true }));
			eBrush();
		}
		moveOnPixel.x = Math.round(pos.x/(canvas.width/WIDTH));
		moveOnPixel.y = Math.round(pos.y/(canvas.height/HEIGHT));
	}else if(moveOnPixel.x != Math.round(pos.x/(canvas.width/WIDTH)) || moveOnPixel.y != Math.round(pos.y/(canvas.height/HEIGHT))){
		cursor = new Vector2(Math.floor(pos.x/(canvas.width/WIDTH)), Math.floor(pos.y/(canvas.height/HEIGHT)));
	}
})
palleteCanvas.addEventListener('mousedown', function(e){
	pos = windowToCanvas(palleteCanvas, e.clientX, e.clientY);
	colorPicker.value=pallete[Math.floor(pos.x/(palleteCanvas.width/8))*2+Math.floor(pos.y/(palleteCanvas.height/2))];
	colorPicker.dispatchEvent(new Event('input', { bubbles: true }));
})

function render(){
	ctx.scale(cScale, cScale);
	ctx.fillStyle = '#ffffff';
	ctx.fillRect(0, 0, canvas.width-1, canvas.height-1);
	for(let y = 0; y < canvas.height; y+=canvas.height/HEIGHT){
		for(let x = 0; x < canvas.width; x+=canvas.width/WIDTH){
			ctx.fillStyle = pixels[y/canvas.height*HEIGHT][x/canvas.width*WIDTH];
			if(mode == 'brush'){
				for(let iy = 0; iy < options['brushSize']; iy++){
					for(let ix = 0; ix < options['brushSize']; ix++){
						let posx = Math.round(cursor.x-options['brushSize']/2+ix);
						let posy = Math.round(cursor.y-options['brushSize']/2+iy);
						if(posx == x/canvas.width*WIDTH && posy == y/canvas.height*HEIGHT)
							ctx.fillStyle = opacityRGB(options['opacity'], colorPicker.value, pixels[posy][posx]);
					}
				}
			}else if(mode == 'eraser'){
				for(let iy = 0; iy < options['brushSize']; iy++){
					for(let ix = 0; ix < options['brushSize']; ix++){
						let posx = Math.round(cursor.x-options['brushSize']/2+ix);
						let posy = Math.round(cursor.y-options['brushSize']/2+iy);
						if(posx == x/canvas.width*WIDTH && posy == y/canvas.height*HEIGHT)
							ctx.fillStyle = opacityRGB(options['opacity'], '#000000', pixels[posy][posx]);
					}
				}
			}else if(mode == 'fill'){
				ctx.fillStyle = opacityRGB(options['opacity'], colorPicker.value, pixels[y/canvas.height*HEIGHT][x/canvas.width*WIDTH]);
			}else if(mode == 'square'){
				if(figure.length == 1){
					if(figureType == 'square'){
						for(let iy = Math.min(figure[0].y, cursor.y); iy < Math.max(figure[0].y, cursor.y)+1; iy++){
							for(let ix = Math.min(figure[0].x, cursor.x); ix < Math.max(figure[0].x, cursor.x)+1; ix++){
								if(ix == x/canvas.width*WIDTH && iy == y/canvas.height*HEIGHT)
								ctx.fillStyle = opacityRGB(options['opacity'], colorPicker.value, pixels[iy][ix]);
							}
						}
					}
				}
			}
			ctx.fillRect(x, y, canvas.width/WIDTH-1, canvas.height/HEIGHT-1);
		}
	}

	pctx.scale(cScale, cScale)
	let i = 0;
	for(let x = 0; x < palleteCanvas.width; x+=palleteCanvas.width/8){
		for(let y = 0; y < palleteCanvas.height; y+=palleteCanvas.height/2){
			pctx.fillStyle = pallete[i];
			pctx.fillRect(x, y, palleteCanvas.width/8, palleteCanvas.height/2);
			i++;
		}
	}
}

function windowToCanvas(cnvs, x, y) {
    let bbox = cnvs.getBoundingClientRect();
    return { x: x - bbox.left * (cnvs.width / bbox.width),
        y: y - bbox.top * (cnvs.height / bbox.height)
    };
}

async function sendImage(){
	let data = []
	for(let y = 0; y < HEIGHT; y++){
		for(let x = 0; x < WIDTH; x++){
			data.push(parseInt(pixels[y][x].slice(1, 3), 16))
			data.push(parseInt(pixels[y][x].slice(3, 5), 16))
			data.push(parseInt(pixels[y][x].slice(5, 7), 16))
		}
	}
	console.log(new Uint8Array(data))
	console.log(new Blob([new Uint8Array(data)]))
    await fetch('http://' + IP + '/api?function=image', {
		method: 'POST',
		mode: "cors",
    	ache: "no-cache",
		body: new Blob([new Uint8Array(data)])
	})
    await showEffectSettings()
}

var mode = 'brush';

var playPauseIcon = document.querySelector('#playpause-btn>i')
var paintToolBrush = document.getElementById('paint-tool-brush')
var paintToolEraser = document.getElementById('paint-tool-eraser')
var paintToolFill = document.getElementById('paint-tool-fill')
var paintToolSquare = document.getElementById('paint-tool-square')
var paintToolEyeDropper = document.getElementById('paint-tool-eye-dropper')


function undo(){
	if(selectedPrev > 0){
		selectedPrev--
		pixels = prevs[selectedPrev]
	}
}
function redo(){
	if(selectedPrev < prevs.length-1){
		selectedPrev++
		pixels = prevs[selectedPrev]
	}
}
function eBrush(){
	paintToolBrush.style.background = '#ddd'
	paintToolEraser.style.background = '#fff'
	paintToolFill.style.background = '#fff'
	paintToolSquare.style.background = '#fff'
	paintToolEyeDropper.style.background = '#fff'
	mode = 'brush'
}
function eEraser(){
	paintToolBrush.style.background = '#fff'
	paintToolEraser.style.background = '#ddd'
	paintToolFill.style.background = '#fff'
	paintToolSquare.style.background = '#fff'
	paintToolEyeDropper.style.background = '#fff'
	mode = 'eraser'
}
function eFill(){
	paintToolBrush.style.background = '#fff'
	paintToolEraser.style.background = '#fff'
	paintToolFill.style.background = '#ddd'
	paintToolSquare.style.background = '#fff'
	paintToolEyeDropper.style.background = '#fff'
	mode = 'fill'
}
function eSquare(){
	paintToolBrush.style.background = '#fff'
	paintToolEraser.style.background = '#fff'
	paintToolFill.style.background = '#fff'
	paintToolSquare.style.background = '#ddd'
	paintToolEyeDropper.style.background = '#fff'
	mode = 'square'
}
function eEyeDropper(){
	paintToolBrush.style.background = '#fff'
	paintToolEraser.style.background = '#fff'
	paintToolFill.style.background = '#fff'
	paintToolSquare.style.background = '#fff'
	paintToolEyeDropper.style.background = '#ddd'
	mode = 'eye-dropper'
}
async function ePlayPause(){
	if(play){
		playPauseIcon.classList.remove('fa-pause')
		playPauseIcon.classList.add('fa-play')
		play = false
	}else{
		playPauseIcon.classList.remove('fa-play')
		playPauseIcon.classList.add('fa-pause')
		play = true
	}
	prevs = []
	selectedPrev = -1
}
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