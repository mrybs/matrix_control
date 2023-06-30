
const IP = '';

let effect_id = "rainbow";
let hue = 50;
let rainbow = false;
let speed = 249;
let saturation = 50;
let chance = 50;

let settings = {
    'off': [],
    'rainbow': ['speed', 'saturation'],
    'confetti': ['speed', 'saturation'],
    'ball': ['hue', 'speed', 'saturation'],
    'snowing': ['hue', 'speed', 'chance', 'saturation'],
    'sinusoid': ['hue', 'speed', 'saturation'],
    'doubleSinusoid': ['hue', 'speed', 'saturation']
};

async function setEffect(){
    let effectCombobox = document.getElementById("effectSelect");
    await fetch(IP + 'api?function=effect&effect='+effectCombobox.value);
    await showEffectSettings();
}
async function imageLoad(){
    let imageTB = document.getElementById("imageTB");
    await fetch(IP + 'api?function=image&image='+imageTB.value);
    await onChange();
}
async function onChange(){
    let hueSliderLabel = document.getElementById('hueLabel');
    let speedSliderLabel = document.getElementById('speedLabel');
    let chanceSliderLabel = document.getElementById('chanceLabel');
    let saturationSliderLabel = document.getElementById('saturationLabel');

    let hueSlider = document.getElementById('hue');
    let speedSlider = document.getElementById('speed');
    let chanceSlider = document.getElementById('chance');
    let saturationSlider = document.getElementById('saturation');

    let rainbowCB = document.getElementById('rainbow');

    hueSliderLabel.innerHTML = hueSlider.value + '%';
    speedSliderLabel.innerHTML = speedSlider.value;
    chanceSliderLabel.innerHTML = chanceSlider.value + '%';
    saturationSliderLabel.innerHTML = saturationSlider.value + '%';

    hue = hueSlider.value*2.55;
    speed = speedSlider.value;
    chance = chanceSlider.value;
    saturation = saturationSlider.value*2.55;
    rainbow = rainbowCB.checked;

    let response = await fetch(IP + 'api?' + new URLSearchParams({
        'function': 'effectSettings',
        'hue': hue,
        'rainbow': rainbow-0,
        'speed': speed,
        'saturation': saturation,
        'chance': chance
    }));
    await reloadSettings();
}
async function reloadSettings(){
    let response = await fetch(IP + 'api?' + new URLSearchParams({
        'function': 'getEffectSettings'
    }));
    let effectSettings = await response.json();
    effect_id = effectSettings['effect_id'];
    hue = effectSettings['hue'];
    rainbow = !!(effectSettings['rainbow']-0);
    speed = effectSettings['speed'];
    chance = effectSettings['chance'];
    saturation = effectSettings['saturation'];

    let hueSliderLabel = document.getElementById('hueLabel');
    let speedSliderLabel = document.getElementById('speedLabel');
    let chanceSliderLabel = document.getElementById('chanceLabel');
    let saturationSliderLabel = document.getElementById('saturationLabel');

    let hueSlider = document.getElementById('hue');
    let speedSlider = document.getElementById('speed');
    let chanceSlider = document.getElementById('chance');
    let saturationSlider = document.getElementById('saturation');

    let effectCombobox = document.getElementById("effectSelect");

    let rainbowCB = document.getElementById('rainbow');

    hueSlider.value = hue/2.55;
    speedSlider.value = speed;
    chanceSlider.value = chance;
    saturationSlider.value = saturation/2.55;

    hueSliderLabel.innerHTML = hueSlider.value + '%';
    speedSliderLabel.innerHTML = speedSlider.value;
    chanceSliderLabel.innerHTML = chanceSlider.value + '%';
    saturationSliderLabel.innerHTML = saturationSlider.value + '%';

    effectCombobox.value = effect_id;

    rainbowCB.checked = rainbow;

    await showEffectSettings();
}
async function showEffectSettings(){
    let effectCombobox = document.getElementById("effectSelect");

    let hueSliderLabel = document.getElementById('hueLabel');
    let speedSliderLabel = document.getElementById('speedLabel');
    let chanceSliderLabel = document.getElementById('chanceLabel');
    let saturationSliderLabel = document.getElementById('saturationLabel');

    let hueSlider = document.getElementById('hueSlider');
    let rainbowCheckbox = document.getElementById('rainbowCheckbox');
    let speedSlider = document.getElementById('speedSlider');
    let chanceSlider = document.getElementById('chanceSlider');
    let saturationSlider = document.getElementById('saturationSlider');

    let rainbowCB = document.getElementById('rainbow');

    if(settings[effectCombobox.value].indexOf('hue') != -1){
        rainbowCheckbox.style.display = 'flex';
        if(!rainbowCB.checked)
            hueSlider.style.display = 'flex';
        else
            hueSlider.style.display = 'none';
    }else{
        hueSlider.style.display = 'none';
        rainbowCheckbox.style.display = 'none';
    }
    if(settings[effectCombobox.value].indexOf('speed') != -1){
        speedSlider.style.display = 'flex';
    }else{
        speedSlider.style.display = 'none';
    }
    if(settings[effectCombobox.value].indexOf('chance') != -1){
        chanceSlider.style.display = 'flex';
    }else{
        chanceSlider.style.display = 'none';
    }
    if(settings[effectCombobox.value].indexOf('saturation') != -1){
        saturationSlider.style.display = 'flex';
    }else{
        saturationSlider.style.display = 'none';
    }
}