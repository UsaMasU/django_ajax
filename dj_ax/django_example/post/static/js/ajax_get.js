$(document).ready(function(){

    $('.likebutton').click(function(){
        let catid = $(this).attr("data-catid");
        let likes_counter = $("#message").text();
        console.log('catid:', catid);
        $("#message").text('await...')
        $.ajax({
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

    $('a#getbtn').click(function(){
        let button_text = $(this).text();
        $.ajax({
                type:"GET",
                url: "/button_ajax_get/",
                data: {
                    text: button_text
                },
                success: function( response ) {
                    console.log('success');
                    console.log(JSON.parse(response)['backtext'])
                    $('a#getbtn').text(JSON.parse(response)['backtext']);
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

