const CONNECT_TYPE = 'mmatrix';
const MMATRIX_IP = 'http://192.168.50.161:8000';
const IP = 'holder(name="matrix_id")';
 
holder(name="defaultsJS")

let settings = holder(name="settings");

async function setEffect(){
    let effectCombobox = document.getElementById("effectSelect");
    if(CONNECT_TYPE == 'local'){
        await fetch(IP + 'api?function=effect&effect='+effectCombobox.value);
    }else if(CONNECT_TYPE == 'current'){
        await fetch('api?function=effect&effect='+effectCombobox.value);
    }else if(CONNECT_TYPE == 'mmatrix'){
        await fetch(MMATRIX_IP + '/api/request?matrix_id='+IP+'&function=effect&effect='+effectCombobox.value);
    }
    await showEffectSettings();
}
async function imageLoad(){
    let imageTB = document.getElementById("imageTB");
    await fetch(IP + 'api?function=image&image='+imageTB.value);
    await onChange();
}
async function onChange(){
    holder(name="onChangeJS")

    let params = new URLSearchParams({"function": "effectSettings", holder(name="changeParamsJS")});

    if(CONNECT_TYPE == 'local'){
        let response = await fetch(IP + 'api?' + params);
    }else if(CONNECT_TYPE == 'current'){
        let response = await fetch('api?' + params);
    }else if(CONNECT_TYPE == 'mmatrix'){
        let response = await fetch(MMATRIX_IP + '/api/request?' + params + '&matrix_id=' + IP);
    }
    await reloadSettings();
}
async function reloadSettings(){
    let response = undefined;
    if(CONNECT_TYPE == 'local'){
        response = await fetch(IP + 'api?' + new URLSearchParams({
            'function': 'getEffectSettings'
        }));
    }else if(CONNECT_TYPE == 'current'){
        response = await fetch('api?' + new URLSearchParams({
            'function': 'getEffectSettings'
        }));
    }else if(CONNECT_TYPE == 'mmatrix'){
        /*Not implemented*/
        return await showEffectSettings();
    }
    let effectSettings = await response.json();
    let effectCombobox = document.getElementById("effectSelect");

    effectCombobox.value = effect_id;

    holder(name="reloadJS")

    await showEffectSettings();
}
async function showEffectSettings(){
    let effectCombobox = document.getElementById("effectSelect");

    holder(name="showEffectSettingsJS")
}