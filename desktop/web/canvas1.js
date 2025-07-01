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
