(function($) {
	var calDatePicker = $('#sidebar #calendar #datepicker').length > 0 ? true : false,
		calContent = $('.goscale-plugins-calendar').length > 0 ? true : false;
	
    $.fn.goscalePluginsCalendar = function() {
		if(calDatePicker) {
			var months = {
					en: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
				},
				impDays = [],
				lang = $('#important-days').data('lang'),
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
					var geo = new google.maps.Geocoder();
					
					geo.geocode({
							address: $span.data('where')
						},
						function(results, status) {
							if (status == google.maps.GeocoderStatus.OK) {
								$('#map').gmap().bind('init', function(ev, map) {
									$('#map').gmap('addMarker', {'position': results[0].geometry.location, 'bounds': true}).click(function() {
										var content = [
											$span.data('title'),
											' (', $span.data('when'), ')<br />',
											'Location : ', $span.data('where')
										].join('');
										$('#map').gmap('openInfoWindow', {'content': content}, this);
									});
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
	$.fn.goscalePluginsCalendar();
})(jQuery);