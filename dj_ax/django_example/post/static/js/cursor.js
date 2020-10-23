$(document).ready(function(){

    cursor_wait = function(){
        // switch to cursor wait for the current element over
        let elements = $(':hover');
        if (elements.length){
            // get the last element which is the one on top
            elements.last().addClass('cursor-wait');
        }
        // use .off() and a unique event name to avoid duplicates
        $('html').
        off('mouseover.cursorwait').
        on('mouseover.cursorwait', function(e){
            // switch to cursor wait for all elements you'll be over
            $(e.target).addClass('cursor-wait');
        });
    }

    remove_cursor_wait = function(){
        $('html').off('mouseover.cursorwait'); // remove event handler
        $('.cursor-wait').removeClass('cursor-wait'); // get back to default
    }

    wait_show = function(){
        showtime = $('#showtime').val()
        cursor_wait();
        setTimeout(remove_cursor_wait, showtime);
    }

    $(document).ajaxStart(function () {
        cursor_wait();
    });

    $(document).ajaxComplete(function () {
        remove_cursor_wait();
    });


// Promise exmple for show cursor by pressing pause button
    delay = (ms = 1000) => {
        return new Promise((resolve, reject) => {
            setTimeout(() => resolve("done"), ms);
        });
    };

    pause = function (){
        ms = $('#showtime').val()
        console.log('pause start:', ms);
        cursor_wait();
        delay(ms)
            .then((data)=>{
                console.log('resolve:', data);
                remove_cursor_wait();
            });
        };

});