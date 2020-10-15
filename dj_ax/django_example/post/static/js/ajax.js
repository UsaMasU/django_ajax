$('.likebutton').click(function(){
    let catid = $(this).attr("data-catid");
    let likes_counter = $("#message").text();
    console.log('catid:', catid);
    $("#message").text('await...')
    $.ajax(
        {
            type:"GET",
            url: "/likepost_get/",
            data: {
                post_id: catid,
                counter: likes_counter
            },
            success: function( response ) {
                $( '#like' + catid ).remove();
                console.log('Ajax Get Success');
                $( '#message' ).text(JSON.parse(response)['count']);
            },
            error: function( response ) {
                        console.log('Ajax Get Failure');
                        console.log(response);
                        $( '#message' ).text('Ajax Get Failure');
                    }
        });
});

$(document).ready(function(){
    $("#mySelect").change(function(){
        selected = $("#mySelect option:selected").text()
        let likes_counter = $("#message").text();
         $( '#serv-response' ).text('awaiting...');

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
                    }
        });
  });
});

