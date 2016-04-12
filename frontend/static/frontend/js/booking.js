$(document).ready(function() {
	if (!Modernizr.inputtypes.date) {
	    $('input[type=date]').datepicker();
	}
	$('#calRefresh').click(function() {
	    var calIframe = document.getElementById('calIframe');
	    calIframe.src = calIframe.src;
	});
	$('label').after('<br>');
});