(function($) {
    $.fn.goscalePluginsCalendar = function() {
		var months = {
				en: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
			},
			impDays = [],
			lang = $('#important-days').data('lang'),
			url = window.location.href,
			startDate = url.indexOf('start=') ? url.substr(url.indexOf('start=') + 6, 10) : false;
		
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
			impDays.push([tmp[3], months[lang].indexOf(tmp[1]), tmp[2].replace(',', '')]);
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
			var $dateLink = $('#important-days #start-date');
			$dateLink.attr('href', $dateLink.attr('href').replace('start=startDate', date));
			$dateLink.click();
		};
		
		$("#datepicker").datepicker({
			beforeShowDay: importantDays,
			onSelect: dayClick,
			defaultDate: startDate ? startDate : null
		});
	};
	$('#sidebar #calendar #datepicker').goscalePluginsCalendar();
})(jQuery);