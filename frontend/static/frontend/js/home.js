window.setInterval(changeImage, 6 * 1000);

var i = 0;
function changeImage() {
	$('#header').css('background-image', "url(" + IMAGE_URLS[i] + ")");
	i++;
	if (i === IMAGE_URLS.length) {
		i = 0;
	}
}