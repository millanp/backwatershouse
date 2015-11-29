$(document).ready(function() {
    $('#bookingForm').submit(function(event) {
        alert("submitting");
        event.preventDefault();
        $.ajax({
            type:'POST',
            data: $('#bookingForm').serialize(),
            dataType: 'html',
            success: function(data) {
                alert(JSON.stringify(data));
		alert("FAO");
		          $('#formWrapper').html(data + "<p class='successMessage'>Request sent for booking.<br>Track its approval status at My Visits.</p>");
            },
            error: function(jqXHR, textStatus, errorThrown) {
                alert(jqXHR.responseText);
		alert("FOO");
                $('#formWrapper').html(jqXHR.responseText);
		alert("FOOF");
            }
        });
    });
});
