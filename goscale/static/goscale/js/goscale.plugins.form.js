(function($) {
	$.fn.goscalePluginsForm = function() {
		var token = $('#google-form form#ss-form input[name="csrfmiddlewaretoken"]')[0],
			url = $('#google-form form#ss-form input[name="url"]')[0];
	
		if($('#form-button').length > 0) {
			$('#form-button a').fancybox();
		}
		
		var handleForm = function() {
			$('#google-form #ss-form').submit(function(e) {
				e.preventDefault();
				$('#google-form input[type=submit]').attr('disabled', 'true');
				$.post('/goscale/utils/form/', $('#google-form #ss-form').serialize(), function(res) {
					if (res != 'error') {
						$(res).each(function() {
							if(typeof(this.innerHTML) != "undefined" && this.innerHTML.indexOf('ss-form-heading') > -1) {
								$('#google-form').html(this.innerHTML);
								$('#google-form form#ss-form').append(token);
								$('#google-form form#ss-form').append(url);
								handleForm();
							}
							else if(typeof(this.innerHTML) != "undefined" && this.innerHTML.indexOf('ss-confirmation') > -1) {
								$('#google-form').html(this.innerHTML);
							}
						});
					}
					else {
						alert('error');
					}
				});
				return false;
			});
		};
		handleForm();
	};
	$.fn.goscalePluginsForm();
})(jQuery);