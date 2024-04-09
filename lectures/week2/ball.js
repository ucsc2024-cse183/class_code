"use strict";

function main() {
    let ball = document.querySelectorAll(".ball")[0];
    let range = document.querySelectorAll('[name=speed]')[0];
    ball.style.left = "300px";
    ball.style.top = "300px";
    let x = 100;
    let y = window.innerHeight - 100;
    let vx = 2;
    let vy = 0;
    let g = -1;

    function tick() {
        let dt = parseFloat(range.value) * 0.01;
        console.log(dt);
        ball.style.left = x + "px";
        ball.style.top = (window.innerHeight - y) + "px";

        x += vx * dt;
        y += vy * dt;
        vy += g * dt;

        if (y < 40) vy = -vy;
    };

    setInterval(tick, 30);
}

main();