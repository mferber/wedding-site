function setup() {
	$('#submitBtn').click(function() {
		var params = {
			name: $('input#name').val(),
			email1: $('input#email1').val(),
			email2: $('input#email2').val()
		};
		var url = "maint/add.cgi?" + $.param(params);
		$.get(url).done(success).fail(failure);
	});
}

function success(data) {
	var response = $('#emailSignupResponse');
	response.text('Thanks — you’ll be notified when we have news!');
	response.removeClass('failure').addClass('success');

	var form = $('.emailSignup form');
	form.css('opacity', 0.25);
	form.find(':input').prop('disabled', true);
}

function failure(xhr, textStatus, error) {
	var response = $('#emailSignupResponse');

	message = xhr.responseText;
	if (message.startsWith('MISSING:')) {
		response.text('Please fill in all the fields!');
	} else if (message.startsWith('EMAIL-MISMATCH')) {
		response.text('Email addresses didn\'t match — check your input!');
	} else {
		response.text('Something went wrong: ' + message);
	}

	response.removeClass('success').addClass('failure');
}