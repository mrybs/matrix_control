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
