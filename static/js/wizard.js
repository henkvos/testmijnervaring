$(document).ready(function() {
	$("#startwizard").click(function() {
				$("#app").load('/startwizard', null, function() {
							// Smart Wizard
							// $('#wizard').smartWizard();
							$('#wizard').smartWizard({
										contentURL : '/wizard',
										// transitionEffect:'slideleft',
										contentCache : false,
										onLeaveStep : serForm,
										onFinish : submitTest

									});

						});
				function serForm() {
					if (self.stepNum == 3) {

						wplist = $('#testwerkprocessen').serializeArray();
						$.post('/processtest', wplist);

						return true;
						
					} else if (self.stepNum == 4) {
						
						toekomst = $('#stap3_toekomst').serializeArray();
						$.post('/processtoekomst', toekomst);
						
                        return true;
						
					} else {
						return true;
					}

				};
				function submitTest() {
					naw = $('#stap4_aanvraag').serializeArray();
					$.post('/submittest', naw);
					//$("#app").load('/thankyou');
					$.post('/thankyou', function(data){
						$('#app').html(data);
					});
					//$('#app').empty();
                    //$("<div/>").html(html).prependTo("#app");
					
					
				};
			});
	// send crsf token for django's csrf protection
	$("body").bind("ajaxSend", function(elm, xhr, s) {
				if (s.type == "POST") {
					xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
				}
			});
});

/*
 * $('form').submit(function() { alert($(this).serialize()); return false; });
 * 
 * 
 */

// The following code will serialize for use with JSON:

(function($) {
	$.fn.serializeJSON = function() {
		var json = {};
		jQuery.map($(this).serializeArray(), function(n, i) {
					json[n['name']] = n['value'];
				});
		return json;
	};
})(jQuery);

// Simply use as $('form').serializeJSON();

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = $.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length
						+ 1));
				break;
			}
		}
	}
	return cookieValue;
}

function setCookie(name, value, days) {
	if (days) {
		var date = new Date();
		date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
		var expires = "; expires=" + date.toGMTString();
	} else
		var expires = "";
	document.cookie = name + "=" + value + expires + "; path=/";
}

// xhr.setRequestHeader("X-CSRFToken", ;

