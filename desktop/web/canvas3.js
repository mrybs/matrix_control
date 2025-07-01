

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


