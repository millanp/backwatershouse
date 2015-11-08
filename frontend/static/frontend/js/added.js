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
            },
            error: function(jqXHR, textStatus, errorThrown) {
                alert(jqXHR.responseText);
                alert($("#formWrapper").html());
            }
        });
    });
});
