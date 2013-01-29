var plugins = plugins || {};

(function($) {
	$.fn.goscalePluginsForm = function() {
		var $formContainer = $(this),
			token = $formContainer.find('input[name="csrfmiddlewaretoken"]')[0],
			url = $formContainer.find('input[name="url"]')[0];
		
		var handleForm = function($container) {
			if(!$container.is('form')) {
				var $container = $container.find('form.ss-form');
			}
			$container.submit(function(e) {
				e.preventDefault();
				var $form = $(this);
				$form.find('input[type=submit]').attr('disabled', 'true');
				$.post('/goscale/utils/form/', $form.serialize(), function(res) {
					if (res != 'error') {
						$(res).each(function() {
							if(typeof(this.innerHTML) != "undefined" && this.innerHTML.indexOf('ss-form-heading') > -1) {
								$parent = $form.parent();
								var title = $parent.find('h1.form-title').length > 0 ? $parent.find('h1.form-title').text() : false;
								$parent.html([
									title ? ['<h1 class="form-title">', title, '</h1>'].join('') : '',
									this.innerHTML
								].join(''));
								$form = $parent.find('form#ss-form');
								$form.attr('id', '').addClass('ss-form');
								$form.find('input[type=submit]').addClass('form-button').before(token).before(url).removeAttr('disabled');
								handleForm($form);
							}
							else if(typeof(this.innerHTML) != "undefined" && this.innerHTML.indexOf('ss-confirmation') > -1) {
								$form.html(this.innerHTML);
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
		
		if($formContainer.find('.form-button').length > 0) {
			$formContainer.find('.form-button a').click(function(e) {
				if($(this).attr('href') == '#form-lb') {
					return true;
				}
				else {
					e.preventDefault();
					$('.form-button a').attr('href', '');
					$('#form-lb').html($(this).parent().parent().find('.form-lb-container').html());
					handleForm($('#form-lb'));
					$(this).attr('href', '#form-lb').fancybox().trigger('click');
				}
			});
		}
		else {
			handleForm($formContainer);
		}
	};
	$('.goscale-plugins-form').each(function() {
		$(this).goscalePluginsForm();
	});
	
	plugins.goscalePluginsForm = function() {
		$('.goscale-plugins-form.content').goscalePluginsForm();
	};
	
	if($('.form-buttons').length > 0) {
		if($('head link[href*="ie.css"]').length == 0) {
			var formButtonsPos = function() {
				$('.form-buttons').css('marginTop', ($(window).height() * 43 / 100));
			};
			$(window).resize(function() {
				formButtonsPos();
			});
			formButtonsPos();
		}
		$('.form-buttons').show();
	}
})(jQuery);