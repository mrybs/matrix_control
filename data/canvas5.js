function updatePaintToolsOptions(){let e=document.getElementById("brushSize"),i=document.getElementById("opacity");options.brushSize=e.value,options.opacity=i.value/100;let t=document.getElementById("brushSizeLabel"),a=document.getElementById("opacityLabel");t.innerText=e.value+"пкс",a.innerText=i.value+"%"}function icthc(e,i,t){let a=e.toString(16),l=i.toString(16),n=t.toString(16);return 1==a.length&&(a="0"+a),1==l.length&&(l="0"+l),1==n.length&&(n="0"+n),"#"+a+l+n}tippy("#paint-tool-options",{content:`
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
	</div>`,interactive:!0,allowHTML:!0,theme:"light-border",animation:"shift-away",arrow:tippy.roundArrow}),websocket.addEventListener("open",e=>{websocket.send("get_matrix")}),websocket.addEventListener("message",e=>{let i=0;e.data.stream().getReader().read().then(e=>{for(let t=0;t<HEIGHT;t++)for(let a=0;a<WIDTH;a++)pixels[t][a]=icthc(e.value[3*i],e.value[3*i+1],e.value[3*i+2]),i++})}),eBrush(),setInterval(()=>{render()},6),setInterval(()=>{play&&websocket.send("get_matrix")},50);