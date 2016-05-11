window.setInterval(changeImage, 6 * 1000);

var i = 0;

function preloadImages() {
	for (var i = IMAGE_URLS.length - 1; i >= 0; i--) {
		var i = new Image();
		i.src = IMAGE_URLS[i]
	}
}()

function changeImage() {
	$('#header').css('background-image', "url(" + IMAGE_URLS[i] + ")");
	i++;
	if (i === IMAGE_URLS.length) {
		i = 0;
	}
}