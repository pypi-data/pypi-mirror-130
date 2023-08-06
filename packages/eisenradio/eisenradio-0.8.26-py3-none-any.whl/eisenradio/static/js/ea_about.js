$(document).ready(function(){

    var req;
    // var timer = setInterval( updateMasterprogress, 10000);

	function updateMasterprogress() {

        req = $.ajax({
                type: 'POST',
                url: "/about",
                cache: false,
                data : {'data': 'percent'}
        });

        req.done(function(data) {
            var percent = '';

            percent = data.result;

            if (percent != 0) {
            console.log('###############################################'+percent);
                $('.progress-bar').css('width', percent+'%').attr('aria-valuenow', percent).html(percent+'%');
                if (percent >= 100) {
                    window.location.href = "/page_flash";
                }
            }

        });


    };


});