 
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