var plugins = plugins || {};

(function($) {
	var calDatePicker = $('#calendar #datepicker').length > 0 ? true : false,
		calContent = $('.goscale-plugins-calendar').length > 0 ? true : false;
	
    $.fn.goscalePluginsCalendar = function() {
		var loadJSFiles = function() {
			var src = [$('head script[src*="goscale.plugins.calendar.js"]').attr('src').split('goscale/js/')[0], 'goscale/js/'].join(''),
				scripts = [
					[src, 'jquery.fancybox-1.3.4.pack.js'].join(''),
					[src, 'jquery.easing.1.3.js'].join(''),
					[src, 'jquery-ui-1.9.2.custom.min.js'].join(''),
					'http://maps.google.com/maps/api/js?sensor=true&callback=plugins.gMapsReady'
				],
				callback = function() {
					$('head script[src*="goscale.plugins.calendar.js"]').attr('rel', 'ready');
					initPlugin();
				},
				checkFiles = function() {
					var tmp = [];
					for(var i = 0, ln = scripts.length; i < ln; i++) {
						if($(['head script[src*="', scripts[i], '"]'].join('')).length == 0) {
							tmp.push(scripts[i]);
						}
					}
					scripts = tmp;
				},
				loadJSFile = function(filename, last) {
					var fileref = document.createElement('script');
					fileref.type = 'text/javascript';
					fileref.src = filename;
					if(last) {
						fileref.onload = callback;
					}
					document.getElementsByTagName("head")[0].appendChild(fileref);
				};
			
			checkFiles();
			if(scripts.length == 0) {
				callback();
			}
			else {
				for(var i = 0, ln = scripts.length; i < ln; i++) {
					loadJSFile(scripts[i], false/*(i == (ln - 1))*/);
				}
			}
		};
		var initPlugin = function() {
			if(calDatePicker) {
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
					window.location.href = $('#important-days').data('url').replace('startDate', date);
				};
				
				$("#datepicker").datepicker({
					beforeShowDay: importantDays,
					onSelect: dayClick,
					defaultDate: startDate ? startDate : null
				});
			}
			
			if(calContent) {
				$('.location-details .ContentDetailLinkLabel').click(function() {
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
		
		if($('head script[src*="goscale.plugins.form.js"]').length > 0) {
			if($('head script[src*="goscale.plugins.calendar.js"][rel="ready"]').length > 0) {
				initPlugin();
			}
			else {
				loadJSFiles();
			}
		}
		else {
			head.ready('goscale.plugins.form.js', function() {
				loadJSFiles();
			});
		}
	};
	
	plugins.goscalePluginsCalendar = function() {
		$.fn.goscalePluginsCalendar();
	};
	plugins.gMapsReady = function() {
		$('head script[src*="goscale.plugins.calendar.js"]').attr('rel', 'ready');
		plugins.goscalePluginsCalendar();
	};
	
	plugins.goscalePluginsCalendar();
})(jQuery);