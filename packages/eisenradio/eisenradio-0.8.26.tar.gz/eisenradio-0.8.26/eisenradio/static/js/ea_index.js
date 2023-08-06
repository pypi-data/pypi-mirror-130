$(document).ready(function(){

    var timer = setInterval( updateDisplay, 5001);
    var timer_master_progress = setInterval( updateMasterprogress, 5002);

    $("button").click(function(){

        if ( $(this).attr("class") == "navbar-toggle collapsed") {

        return;
        };

        let clicked = $(this).attr("name");
        console.log("send name "+clicked)
        let class_val = $(this).attr("class");  /* does not survive the request, this is strange */
        console.log("send button "+class_val)
        let id = $(this).attr("id");

		let dict = {
			'name': clicked, 
			'class_val': class_val,   /* pass it to server and get it back*/
			'button_id': id, 
		};
        req = $.ajax({
                type : 'POST',
                dataType : "json",
                url : "/",
                data : dict,
        });
        $('#'+id).fadeOut(1).fadeIn(3);

        req.done(function(data) {
/*
			  console.log("req.done result "+data.result);
			  console.log("req.done former_button_to_switch "+data.former_button_to_switch);
              console.log("req.done button "+data.class_val);
			  console.log("req.done current_station "+data.current_station);
			  console.log("req.done buttons (return from index_posts_clicked) "+data.buttons);
*/
            if (data.class_val == "btn btn-primary") {
                        $('#'+id).removeClass("btn btn-primary");
                        $('#'+id).addClass("btn btn-danger");
            };

            if (data.class_val == "btn btn-danger") {
                        $('#'+id).removeClass("btn btn-danger");
                        $('#'+id).addClass("btn btn-primary");
            };

            if (data.radio_table_id) {

                        var r_table_id = data.radio_table_id
            };
            if (data.table_ident) {
                        var current_station = data.table_ident
                        console.log('table_ident '+current_station)
                        
                        if (current_station != 'Null') {
						var radioLocation = 'http://localhost:5050/#'+current_station
						/* document.getElementById("lbl_div_audio").setAttribute('onclick', 'window.location.href=\'http://localhost:5050/body_color_select_all''); */
                        document.getElementById('lbl_div_audio').innerText = " > " + current_station;
                        document.getElementById('lbl_div_audio').style.color = "#cccccc";
						
						/*document.getElementById('progress_record_all').scrollIntoView();*/
						/* document.getElementById("lbl_div_audio").setAttribute('onclick', document.getElementById("progress_record_all").scrollIntoView(true)); */
						/* function ok = document.getElementById("lbl_div_audio").setAttribute('onclick', "window.location='" + "//www.google.de'"); */
						$("#lbl_div_audio").on('click', function(){
							/* window.location.href = "http://localhost:5050/#";    */
							location.hash = "#" + r_table_id;
							});
                        }
            if (data.former_button_to_switch) {
                        var num = data.former_button_to_switch
                        console.log('auto_click former_button_to_switch: '+num)
                        $("#"+num).click(); // Click on the button -> $("button").click(function(){ recall, should be last entry in fkt?
            };
            };

                if (data.result == 'deactivate_audio') {
                    console.log('deactivate_audio')

                        audio_control = 'audio_with_controls';
                        myAudio = document.getElementById(audio_control);
                        myAudio.pause();
                        myAudio.src = "";
                        myAudio.load();
                        document.getElementById('lbl_div_audio').innerText  = '*';
						document.getElementById('lbl_div_audio').style.color = "#f1f1f1";

                };

                if (data.result == 'activate_audio') {
                    console.log('activate_audio')

                        url = data.query_url;
                        console.log(url);
                        audio_control = 'audio_with_controls';
                	    myAudio = document.getElementById(audio_control);
                	    myAudio.pause();
                	    myAudio.src = "";
                	    // myAudio.load()

                	    myAudio.src = url;
                        myAudio.volume = 0.25;
                	    myAudio.load()
                	    myAudio.play = true;

                	    // myAudio.muted  = true;
                };

        });


	});

	function updateDisplay() {
        var req;
        var clicked;
        var id;
        var class_val;
        req = $.ajax({
                type: 'GET',
                url: "/display_info",
                cache: false,
        });

        req.done(function(data) {
            var displays = '';
            var display = '';
            var table_id = '';
            var title = '';

            displays = data.result.split(",");
                $.each(displays, function(idx, val) {

                    display = val;

                    if (display.length != 0) {

                        display = val.split("=");
                        table_id = display[0]
                        title = display[1]
                        if (title != 'Null') {
                        $('#Display_'+table_id).attr("value", title) ;
                        }
                        if (title == 'Null') {
                        $('#Display_'+table_id).attr("value", '') ;
                        }
                        // console.log(title)

                    }

                });

        });


    };

	function updateMasterprogress() {
        var req;

        req = $.ajax({
                type: 'POST',
                url: "/index_posts_percent",
                cache: false,
                data : {'percent': 'percent'}
        });

        req.done(function(data) {
            var percent = '';

            percent = data.result;
            // console.log('########### '+percent+' #########');
            if (percent == 0) {
                    $('.progress-bar').css('width', 25+'%').attr('aria-valuenow', 25).html('Timer Off');
                }
            if (percent != 0) {
                $('.progress-bar').css('width', percent+'%').attr('aria-valuenow', percent).html('Run, Forrest! RUN!');
                if (percent >= 100) {
                    window.location.href = "/page_flash";
                }
            }

        });


    };

});