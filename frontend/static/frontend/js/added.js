$('#bookingForm').submit(function(event) {
    alert("submitting");
    event.preventDefault();
    $.ajax({
        type:'POST',
        data: $('#bookingForm').serialize(),
        success: function(data) {
            alert("FOOFA");
        },
    });
});