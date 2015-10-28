// Submit post on submit
$('#post-form').on('submit', function(event) {
    event.preventDefault();
    do_post();
});
function do_post() {
    $.ajax({
        url : "",
        type : "POST",
        data : {
            
        },
        
    });
}