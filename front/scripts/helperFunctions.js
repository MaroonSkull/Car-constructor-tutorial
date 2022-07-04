// крайние позиции стика (он внутри квадрата, так что по x и по y одинаковые лимиты)
let min = 0, max;

function map(x, minIn, maxIn, minOut, maxOut) {
	return Math.round((x - minIn) * (maxOut - minOut) / (maxIn - minIn) + minOut);
}

function clamp(num, min, max) {
	return num <= min ? min : num >= max ? max : num;
}

function setupSizesOfStickpad() {
	const stick = document.getElementById('stick');
	const stickpad = document.getElementById('stickpad');
	moveStickTo(stick, stickpad, [stickpad.offsetWidth/2, stickpad.offsetHeight/2]);
	max = stickpad.offsetWidth-stick.offsetWidth;
}

function getXY(e, target) {
	let offsetX = e.offsetX;
	let offsetY = e.offsetY;

	let element = e.target;

	while (element !== target) {
		offsetX += element.offsetLeft;
		offsetY += element.offsetTop;
		element = element.parentNode;
	}
	
	return [offsetX, offsetY];
}

function moveStickTo(stick, stickpad, XY) {
	stick.style.left = clamp(XY[0]-stick.offsetWidth/2, 0, stickpad.offsetWidth-stick.offsetWidth)+"px";
	stick.style.top = clamp(XY[1]-stick.offsetHeight/2, 0, stickpad.offsetHeight-stick.offsetHeight)+"px";
}