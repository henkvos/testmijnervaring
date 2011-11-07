$(document).ready(function() {
	$(".starttest").click(function() {
				runWizard();
			});

	// send crsf token for django's csrf protection
	$("body").bind("ajaxSend", function(elm, xhr, s) {
				if (s.type == "POST") {
					xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
				}
			});
});

function runWizard() {
	$("#app").load('/startwizard', null, function() {

				$('#wizard').smartWizard({
							contentURL : '/wizard',
							// transitionEffect:'slideleft',
							contentCache : false,
							onLeaveStep : serForm,
							onFinish : submitTest

						});

			});
	function serForm() {
		if (self.stepNum == 2) {
			id = $("#uitstroom_id").val();
			if (!id) {
				$('#wizard').smartWizard('setError', {
							stepnum : 1,
							iserror : true
						});
				$('#wizard').smartWizard('showMessage', 'Kies eerst een beroep');
				$("#beroep").addClass("error");
				return false;
				// return true;
			} else {
				$('#wizard').smartWizard('setError', {
							stepnum : 1,
							iserror : false
						});
				$('#wizard').smartWizard('hideMessage');

				return true;
			}

		} else if (self.stepNum == 3) {

			var wpForm = $("#testwerkprocessen").validate({
				errorPlacement : function(error, element) {
					error.appendTo(element.parent().next());
				},
				success : function() {
					nrInvalid = wpForm.numberOfInvalids();
					if (nrInvalid == 0) {
						$('#wizard').smartWizard('hideMessage');
						$('#wizard').smartWizard('setError', {
									stepnum : 2,
									iserror : false
								});
						return true;
					} else {
						$('#wizard').smartWizard('setError', {
									stepnum : 2,
									iserror : true
								});
						$('#wizard').smartWizard('showMessage',
								'Vul de lijst volledig in');
						return false;
					}

				}

			});

			if ($("#testwerkprocessen").valid()) {
				$('#wizard').smartWizard('hideMessage');
				$('#wizard').smartWizard('setError', {
							stepnum : 2,
							iserror : false
						});
				wplist = $('#testwerkprocessen').serializeArray();
				$.post('/processtest', wplist);
				return true;

				//
			} else {
				$('#wizard').smartWizard('setError', {
							stepnum : 2,
							iserror : true
						});
				$('#wizard').smartWizard('showMessage',
						'Vul de lijst volledig in');
				return false;
			}

		} else if (self.stepNum == 4) {
			var st3Form = $("#stap3_toekomst").validate({
				errorPlacement : function(error, element) {
					error.appendTo(element.parent().next());
				},
				success : function() {
					nrInvalid = st3Form.numberOfInvalids();
					if (nrInvalid == 0) {
						$('#wizard').smartWizard('hideMessage');
						$('#wizard').smartWizard('setError', {
									stepnum : 3,
									iserror : false
								});
						return true;
					} else {
						$('#wizard').smartWizard('setError', {
									stepnum : 3,
									iserror : true
								});
						$('#wizard').smartWizard('showMessage',
								'Vul de lijst volledig in');
						return false;
					}

				}

			});

			if ($("#stap3_toekomst").valid()) {
				$('#wizard').smartWizard('setError', {
							stepnum : 3,
							iserror : false
						});
				$('#wizard').smartWizard('hideMessage');
				toekomst = $('#stap3_toekomst').serializeArray();
				$.post('/processtoekomst', toekomst);
				return true;
			} else {
				$('#wizard').smartWizard('setError', {
							stepnum : 3,
							iserror : true
						});
				$('#wizard').smartWizard('showMessage',
						'Vul de lijst volledig in');
				return false;

			}

		} else {
			return true;
		}

	};
	function submitTest() {
		jQuery.validator.setDefaults({
				// errorClass: "ui-state-error ui-corner-all"
				// errorElement : ""
				});
		var submitForm = $("#stap4_aanvraag").validate({
			errorPlacement : function(error, element) {
                    error.appendTo(element.parent().next());
                },
			success : function() {
				nrInvalid = submitForm.numberOfInvalids();
				if (nrInvalid == 0) {
					$('#wizard').smartWizard('hideMessage');
					$('#wizard').smartWizard('setError', {
								stepnum : 4,
								iserror : false
							});
					return true;
				} else {
					$('#wizard').smartWizard('setError', {
								stepnum : 4,
								iserror : true
							});
					$('#wizard')
							.smartWizard('showMessage',
									'Vul de verplichte velden in alvorens de aanvraag te verzenden');
					return false;
				}
			}

		});

		if ($("#stap4_aanvraag").valid()) {
			$('#wizard').smartWizard('hideMessage');
			$('#wizard').smartWizard('setError', {
						stepnum : 4,
						iserror : false
					});
			naw = $('#stap4_aanvraag').serializeArray();
			$.post('/submittest', naw, function() {
						$('#header-phrase').empty();
						$.post('/thankyou', function(data) {
									$('#app').html(data);
								});
					});

			//
		} else {
			$('#wizard').smartWizard('setError', {
						stepnum : 4,
						iserror : true
					});
			$('#wizard')
					.smartWizard('showMessage',
							'Vul de verplichte velden in alvorens je de aanvraag verzend');
			return false;
		}

	};
}

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

