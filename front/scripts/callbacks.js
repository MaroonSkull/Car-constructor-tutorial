// When true, moving the pointer moving the stick
let isMoving = false;

window.onresize=setupSizesOfStickpad;

// event.offsetX, event.offsetY gives the (x,y) offset from the edge of the stickpad.
window.onload = function() {
	const stick = document.getElementById('stick');
	const stickpad = document.getElementById('stickpad');
	
	setupSizesOfStickpad();
	
	// Add the event listeners for mousedown, mousemove, and mouseup
	stickpad.addEventListener('pointerdown', e => {
		isMoving = true;
		moveStickTo(stick, stickpad, getXY(e, stickpad));
		console.log(map(parseInt(stick.style.left), min, max, servoMin, servoMax)+" "+map(parseInt(stick.style.top), min, max, speedMax, speedMin)); // ось y инвертирована, поэтому сначала идёт max.
	});

	document.addEventListener('pointermove', e => {
		if (isMoving === true && (e.target === stick || (e.target === stickpad))) {
			moveStickTo(stick, stickpad, getXY(e, stickpad));
			console.log(map(parseInt(stick.style.left), min, max, servoMin, servoMax)+" "+map(parseInt(stick.style.top), min, max, speedMax, speedMin));
		}
	});

	document.addEventListener('pointerup', e => {
		if (isMoving === true) {
			moveStickTo(stick, stickpad, [stickpad.offsetWidth/2, stickpad.offsetHeight/2]);
			isMoving = false;
			console.log(map(parseInt(stick.style.left), min, max, servoMin, servoMax)+" "+map(parseInt(stick.style.top), min, max, speedMax, speedMin));
		}
	});
}