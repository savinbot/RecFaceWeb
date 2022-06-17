'use strict';

// =====
window.onload = (event) => {
	// -----
	const IMAGE = document.createElement('img');
	const PHOTO = document.getElementById('photo');
	const BUTTON = document.getElementById('button');
	BUTTON.setAttribute('play', true);
	// -----
	const CANVAS = document.getElementById('canvas');
	const CONTEXT = CANVAS.getContext('2d');
	// -----
	CANVAS.width = IMAGE.width = 720;
	CANVAS.height = IMAGE.height = 480;
	CANVAS.style.width = IMAGE.style.width = CANVAS.width + 'px';
	CANVAS.style.height = IMAGE.style.height = CANVAS.height + 'px';
	CANVAS.style.backgroundColor = '#212121';
	// -----
	CONTEXT.setTransform(1, 0, 0, 1, 0, 0);
	// -----
	let animationId = 0;
	const animation = (timestamp) => {
		CONTEXT.drawImage(IMAGE, 0, 0, CANVAS.width, CANVAS.height);
		animationId = window.requestAnimationFrame(animation);
	};
	// -----
	BUTTON.addEventListener('click', (event) => {
		if (BUTTON.getAttribute('play') === 'false') {
			BUTTON.textContent = 'Stop stream';
			BUTTON.setAttribute('play', true);
			IMAGE.src = `http://192.168.0.100/video?play=1&width=${CANVAS.width}&height=${CANVAS.height}`;
			animationId = window.requestAnimationFrame(animation);
		} else if (BUTTON.getAttribute('play') === 'true') {
			BUTTON.textContent = 'Start stream';
			BUTTON.setAttribute('play', false);
			IMAGE.src = `http://192.168.0.100/video?play=0&width=${CANVAS.width}&height=${CANVAS.height}`
			window.cancelAnimationFrame(animationId);
		}
	});
};
