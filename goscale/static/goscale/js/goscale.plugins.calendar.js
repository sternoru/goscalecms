var plugins = plugins || {};

(function($) {
	$.fn.goscalePluginsCalendar = function() {
		var $container = $(this);
		
		if(navigator.appName == 'Microsoft Internet Explorer') {
			$('body').addClass('ie');
		}
		
		if($container.find('#datepicker').length > 0 && !$container.hasClass('ready')) {
			$container.addClass('ready');
			var months = {
					en: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
				},
				impDays = [],
				lang = 'en',//$('#important-days').data('lang'),
				url = window.location.href,
				startDate = url.indexOf('start=') > -1 ? url.substr((url.indexOf('start=') + 6), 10) : false;
			
			if(!Array.prototype.indexOf) {
				Array.prototype.indexOf = function(needle) {
					for(var i = 0; i < this.length; i++) {
						if(this[i] === needle) {
							return i;
						}
					}
					return -1;
				};
			}
			
			$('#important-days span.day').each(function() {
				var tmp = $(this).data('date').split(' ');
				impDays.push([tmp[3], months[lang].indexOf(tmp[1]) + 1, tmp[2].replace(',', '')]);
			});
			
			var importantDays = function(date) {
				for(var i = 0, ln = impDays.length; i < ln; i++) {
					if((date.getFullYear() == impDays[i][0]) && (date.getMonth() == impDays[i][1] - 1) && (date.getDate() == impDays[i][2])) {
						return [true, 'DayOfEvent'];
					}
				}
				return [true, ''];
			};
			
			var dayClick = function(date) {
				var newHref = $('#important-days').data('url').replace('startDate', date);
				if(window.location.href.indexOf('#!path=') > -1) {
					newHref = ['#!path=', newHref].join('');
				}
				window.location.href = newHref;
			};
			
			$("#datepicker").datepicker({
				beforeShowDay: importantDays,
				onSelect: dayClick,
				defaultDate: startDate ? startDate : null
			});
		}
		else if($container.hasClass('content') && !$container.hasClass('ready')) {
			$container.addClass('ready');
			$container.find('.location-details .ContentDetailLinkLabel').click(function() {
				var $span = $(this),
					$link = $span.parent().find('a.link');
				
				if(typeof($link.attr('href')) == "undefined") {
					$('.location-details .ContentDetailLinkLabel').each(function() {
						$(this).attr('href', '');
					});
					
					var geo = new google.maps.Geocoder();
					geo.geocode({
							address: $span.data('where')
						},
						function(results, status) {
							if (status == google.maps.GeocoderStatus.OK) {
								var myLatlng = results[0].geometry.location,
									mapOptions = {
									  zoom: 6,
									  center: myLatlng,
									  mapTypeId: google.maps.MapTypeId.ROADMAP
									},
									map = new google.maps.Map(document.getElementById('map'), mapOptions),
									content = [
										'<b>', $span.data('title'), '</b><br /><br />',
										$span.data('when'), '<br />',
										$span.data('where')
									].join(''),
									infowindow = new google.maps.InfoWindow({
										content: content
									}),
									marker = new google.maps.Marker({
										position: myLatlng,
										map: map,
										title: $span.data('title')
									});
									
								google.maps.event.addListener(marker, 'click', function() {
								  infowindow.open(map,marker);
								});
								
								$link.attr('href', '#map').fancybox().trigger('click');
							}
							else {
								$span.parent().parent().parent().css('background', 'none');
								$span.parent().parent().find('.error').show();
								$span.parent().remove();
							}
						}
					);
				}
				else {
					$link.trigger('click');
				}
			});
		}
	};
	
	plugins.goscalePluginsCalendar = function() {
		if($('.goscale-plugins-calendar').length > 0) {
			$('.goscale-plugins-calendar').each(function() {
				$(this).goscalePluginsCalendar();
			});
		}
	};
	
	$(function() {
		if($(['head script[src="http://maps.google.com/maps/api/js?sensor=true&callback=plugins.goscalePluginsCalendar"]'].join('')).length == 0) {
			var fileref = document.createElement('script');
			fileref.type = "text/javascript";
			fileref.src = "http://maps.google.com/maps/api/js?sensor=true&callback=plugins.goscalePluginsCalendar";
			document.getElementsByTagName("head")[0].appendChild(fileref);
		}
		else {
			plugins.goscalePluginsCalendar();
		}
	});
})(jQuery);