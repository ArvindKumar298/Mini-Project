let btn1 = document.getElementById("btn1");
let btn2 = document.getElementById("btn2");
let btn3 = document.getElementById("btn3");
let btn4 = document.getElementById("btn4");
let btn5 = document.getElementById("btn5"); 
let body = document.querySelector(".interface");
let para = document.querySelector("p");
let h2 = document.querySelector("h2");
let ipt = document.querySelector("#ipt");



function heading() {
    if(ipt.value=="") {
        alert("Please Enter any Word first")
    } else {
        h2.innerText = ipt.value;
    }
}

btn1.addEventListener("click", heading);

//-------------------------------------------------
function bg_color () {
    let r = Math.floor(Math.random()*255);
    let g = Math.floor(Math.random()*255);
    let b = Math.floor(Math.random()*255);

    body.style.backgroundColor= `rgb(${r},${g},${b})`;
}

btn2.addEventListener("click",bg_color);

//----------------------------------------------------

let count = 0;
function font_size() {
    count += 5;
   para.style.fontSize = `${16+count}px`;
}

btn3.addEventListener("click", font_size);

//--------------------------------------------------------

let orginal_text = para.innerText;
let clicks = 0
function hide() {
    clicks += 1;
    if(clicks%2==0) {
        para.innerText = orginal_text;
    } else {
        para.innerText = "";
    }
   
} 

btn4.addEventListener("click", hide);

//----------------------------------------------------------

let orginal_heading = h2.innerText;
let orginal_color = body.style.backgroundColor;

function rest() {
    h2.innerText = orginal_heading;
    para.innerText = orginal_text;
    para.style.fontSize = "16px";
    count = 0;
    clicks = 0;
    ipt.value="";
    body.style.backgroundColor = orginal_color;
}

btn5.addEventListener("click", rest);