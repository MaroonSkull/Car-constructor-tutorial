// When true, moving the pointer moving the stick
let isMoving = false;

window.onresize=setupSizesOfStickpad;

// event.offsetX, event.offsetY gives the (x,y) offset from the edge of the stickpad.
window.onload = function() {
	const stick = document.getElementById('stick');
	const stickpad = document.getElementById('stickpad');
	
	let timerId, angle, speed;
	
	setupSizesOfStickpad();
	
	// Add the event listeners for mousedown, mousemove, and mouseup
	stickpad.addEventListener('pointerdown', e => {
		isMoving = true;
		moveStickTo(stick, stickpad, getXY(e, stickpad));
		angle = getServoAngle(stick.style.left);
		speed = getSpeedValue(stick.style.top);
		fifo.push("/control?angle="+angle+"&speed="+speed);
		if (typeof interval !== 'undefined'){
			clearInterval(timerId);	// clearing prev interval to prevent memory leak
		}
		timerId = setInterval(() => {
			if (!fifo.isEmpty())
				httpGetAsync(fifo.shift(), msg => {console.log(msg+" have been recieved!");});
		}, 0.1e+3);
	});

	document.addEventListener('pointermove', e => {
		if (isMoving === true && (e.target === stick || (e.target === stickpad))) {
			moveStickTo(stick, stickpad, getXY(e, stickpad));
			angle = getServoAngle(stick.style.left);
			speed = getSpeedValue(stick.style.top);
			fifo.push("/control?angle="+angle+"&speed="+speed);
		}
	});

	document.addEventListener('pointerup', e => {
		if (isMoving === true) {
			moveStickTo(stick, stickpad, [stickpad.offsetWidth/2, stickpad.offsetHeight/2]);
			isMoving = false;
			angle = getServoAngle(stick.style.left);
			speed = getSpeedValue(stick.style.top);
			clearInterval(timerId);
			fifo.clear();
			httpGetAsync("/control?angle="+angle+"&speed="+speed, msg => {
				console.log(msg+" have been recieved, stopping interval!");
			})
		}
	});
}