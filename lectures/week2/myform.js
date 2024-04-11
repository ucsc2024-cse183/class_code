"use strict";

var input = document.querySelector('input[name=mytext]');
function update() {
    var div = document.querySelector('#myoutput');    
    div.innerText=input.value;
}
input.addEventListener("keyup", update);

