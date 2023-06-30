const WIDTH = 5;
const HEIGHT = 5;

let scale = 1;

let pixels = [];

for(let y = 0; y < HEIGHT; y++){
	pixels.push([]);
	for(let x = 0; x < WIDTH; x++){
		pixels[y][x] = '#000000';
	}
}


let canvasBox = document.getElementById('imageDrawCanvasBox');
let colorPicker = document.getElementById('imageDrawColorPicker');
let canvas = document.getElementById('imageDrawCanvas');
canvas.width = canvasBox.offsetWidth - 30;
canvas.height = canvas.width;
let ctx = canvas.getContext('2d');

let isPressed = false;

canvas.addEventListener('mouseup', function(){
	isPressed = false;
});
canvas.addEventListener('mousedown', function(e){
	isPressed = true;
	if(mode == 'brush'){
			pos = windowToCanvas(canvas, e.clientX, e.clientY);
			pixels[Math.floor(pos.y/(canvas.height/HEIGHT),1)][Math.floor(pos.x/(canvas.width/WIDTH),1)]=colorPicker.value;
		}else if(mode == 'fill'){
			for(let y = 0; y < HEIGHT; y++){
				for(let x = 0; x < WIDTH; x++){
					pixels[y][x] = colorPicker.value;
				}
			}
		}else if(mode == 'eye-dropper'){
			pos = windowToCanvas(canvas, e.clientX, e.clientY);
			colorPicker.value=pixels[Math.floor(pos.y/(canvas.height/HEIGHT),1)][Math.floor(pos.x/(canvas.width/WIDTH),1)];
			colorPicker.dispatchEvent(new Event('input', { bubbles: true }));
			eBrush();
		}
});

canvas.addEventListener('mousemove', function(e){
	if(isPressed){
		if(mode == 'brush'){
			pos = windowToCanvas(canvas, e.clientX, e.clientY);
			pixels[Math.floor(pos.y/(canvas.height/HEIGHT),1)][Math.floor(pos.x/(canvas.width/WIDTH),1)]=colorPicker.value;
		}else if(mode == 'fill'){
			for(let y = 0; y < HEIGHT; y++){
				for(let x = 0; x < WIDTH; x++){
					pixels[y][x] = colorPicker.value;
				}
			}
		}else if(mode == 'eye-dropper'){
			pos = windowToCanvas(canvas, e.clientX, e.clientY);
			colorPicker.value=pixels[Math.floor(pos.y/(canvas.height/HEIGHT),1)][Math.floor(pos.x/(canvas.width/WIDTH),1)];
			colorPicker.dispatchEvent(new Event('input', { bubbles: true }));
			eBrush();
		}
	}
});

function render(){
	ctx.scale(scale, scale);
	ctx.fillStyle = '#ffffff';
	ctx.fillRect(0, 0, canvas.width, canvas.height);

	for(let y = 0; y < canvas.height; y+=canvas.height/HEIGHT){
		for(let x = 0; x < canvas.width; x+=canvas.width/WIDTH){
			ctx.fillStyle = pixels[y/(canvas.height/HEIGHT)][x/(canvas.width/WIDTH)];
			ctx.fillRect(x, y, canvas.width/WIDTH-1, canvas.height/HEIGHT-1);
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
	let data = '';
	for(let y = 0; y < HEIGHT; y++){
		for(let x = 0; x < WIDTH; x++){
			if(pixels[y][x].length == 9){
				data += pixels[y][x].substr(1,9);
			}else{
				data += pixels[y][x].substr(1,7) + 'ff';
			}
		}
	}
    await fetch(IP + 'api?function=image&image='+data);
    await showEffectSettings();
}

let mode = 'brush';

function eBrush(){
	let paintToolBrush = document.getElementById('paint-tool-brush');
	let paintToolFill = document.getElementById('paint-tool-fill');
	let paintToolEyeDropper = document.getElementById('paint-tool-eye-dropper');

	paintToolBrush.style.background = '#ddd';
	paintToolFill.style.background = '#fff';
	paintToolEyeDropper.style.background = '#fff';
	mode = 'brush';
}
function eFill(){
	let paintToolBrush = document.getElementById('paint-tool-brush');
	let paintToolFill = document.getElementById('paint-tool-fill');
	let paintToolEyeDropper = document.getElementById('paint-tool-eye-dropper');

	paintToolBrush.style.background = '#fff';
	paintToolFill.style.background = '#ddd';
	paintToolEyeDropper.style.background = '#fff';
	mode = 'fill';
}
function eEyeDropper(){
	let paintToolBrush = document.getElementById('paint-tool-brush');
	let paintToolFill = document.getElementById('paint-tool-fill');
	let paintToolEyeDropper = document.getElementById('paint-tool-eye-dropper');

	paintToolBrush.style.background = '#fff';
	paintToolFill.style.background = '#fff';
	paintToolEyeDropper.style.background = '#ddd';
	mode = 'eye-dropper';
}
async function eRefresh(){
	let response = await fetch(IP + 'api?function=getMatrix');
	let data = await response.text();
	let i = 0;
	for(let y = 0; y < HEIGHT; y++){
		for(let x = 0; x < WIDTH; x++){
			pixels[y][x] = '#'+data.substr(i*6, 6);
			i++;
		}
	}
    await showEffectSettings();
}

eBrush();
eRefresh();

setInterval(() => {
	render();
}, 6);