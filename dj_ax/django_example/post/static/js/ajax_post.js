$(document).ready(function(){

    $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                function getCookie(name) {
                    var cookieValue = null;
                        if (document.cookie && document.cookie != '') {
                            var cookies = document.cookie.split(';');
                            for (var i = 0; i < cookies.length; i++) {
                                var cookie = jQuery.trim(cookies[i]);
                                // Does this cookie string begin with the name we want?
                                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                    break;
                                }
                            }
                        }
                    return cookieValue;
                }
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    // Only send the token to relative URLs i.e. locally.
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        });

    $("#mySelect").change(function(){
        selected = $("#mySelect option:selected").text()
        let likes_counter = $("#message").text();
         $( '#serv-response' ).text('awaiting...');

        $.ajax({
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            url: '/likepost_post/',
            processData: false,
            data: JSON.stringify({
                    fruit: selected
                  }),
            success: function(response) {
                        console.log('Ajax Post Success');
                        console.log(response)
                        $( '#serv-response' ).text(response['fruit'] + ' ' + response['count']);
            },
            error: function(response) {
                        console.log('Ajax Post Failure');
                        console.log(response);
                        $( '#serv-response' ).text('Failure');
            },
            complete: function( response ){
                    console.log('complete');
            }
        });
  });

    $('#postbtn').click(function(){
        //let button_text = $(this).text();
        let button_text = $(this).val();
        $.ajax({
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            url: '/button_ajax_post/',
            processData: false,
            data: JSON.stringify({
                    text: button_text
            }),
            success: function( response ) {
                    console.log('success');
                    console.log(response['backtext'])
                    $('#postbtn').val(response['backtext']);
                },
            error: function( response ) {
                    console.log('error');
            },
            complete: function( response ){
                    console.log('complete');
            }
        });
    });

});
