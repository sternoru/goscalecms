var plugins = plugins || {};

(function($) {
	$.fn.goscalePluginsForm = function() {
		if(navigator.appName == 'Microsoft Internet Explorer') {
			$('body').addClass('ie');
		}
		var $formContainer = $(this),
			token = $formContainer.find('input[name="csrfmiddlewaretoken"]')[0],
			url = $formContainer.find('input[name="url"]')[0],
			handler = $formContainer.data('ajax-handler'),
			handleForm = function($container) {
				$container.addClass('ready');
				if(!$container.is('form')) {
					var $container = $container.find('form.ss-form');
				}
				$container.submit(function(e) {
					e.preventDefault();
					var $form = $(this);
					$form.find('input[type=submit]').attr('disabled', 'true');
					$.post(handler, $form.serialize(), function(res) {
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
		
		if($formContainer.hasClass('popup') && !$formContainer.hasClass('ready')) {
			if($('#form-buttons').length == 0) {
				$('body').append('<div id="form-buttons"></div>');
				$('body').append('<div class="form-lb-container"><div id="form-lb"></div></div>');
				
				$('#form-buttons .form-button a').live('click', function(e) {
					if($(this).hasClass('current-lb')) {
						return true;
					}
					else {
						e.preventDefault();
						$('.form-button a').removeClass('current-lb');
						$('#form-lb').html($(this).parent().find('.form-lb-container').html());
						handleForm($('#form-lb'));
						if($(this).attr('href') != '#form-lb') {
							$(this).attr('href', '#form-lb').fancybox();
						}
						$(this).addClass('current-lb');
						$(this).trigger('click');
					}
				});
				
				if(!$('body').hasClass('ie')) {
					var formButtonsPos = function() {
						$('#form-buttons').css('marginTop', ($(window).height() * 43 / 100));
					};
					$(window).resize(function() {
						formButtonsPos();
					});
					formButtonsPos();
				}
			}
			
			$('#form-buttons').append($formContainer.find('.form-button'));
			$formContainer.remove();
		}
		else {
			if(!$formContainer.hasClass('ready')) {
				handleForm($formContainer);
			}
		}
	};
	
	plugins.goscalePluginsForm = function() {
		if($('.goscale-plugins-form').length > 0) {
			$('.goscale-plugins-form').each(function() {
				$(this).goscalePluginsForm();
			});
		}
	};
	
	$(function() {
		plugins.goscalePluginsForm();
	});
})(jQuery);