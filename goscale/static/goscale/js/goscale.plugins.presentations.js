var plugins = plugins || {};

(function($) {
    $.fn.goscalePluginsPresentations = function() {
		if(navigator.appName == 'Microsoft Internet Explorer') {
			$('body').addClass('ie');
		}
		var $pluginContainer = $(this),
			$iframe = $pluginContainer.find('iframe');
		
		if($pluginContainer.data('width') == 'None') {
			var ratio = $pluginContainer.data('ratio'),
				ratioWidth = ratio.split(':')[0],
				ratioHeight = ratio.split(':')[1];
			
			if($pluginContainer.data('height') == 'None') {
				$iframe.attr('width', '100%').attr('height', ($iframe.css('width').replace('px', '') / ratioWidth * ratioHeight + 30));
			}
			else {
				$iframe.attr('width', ($iframe.css('height') / ratioHeight * ratioWidth));
			}
		}
	};
	
	plugins.goscalePluginsPresentations = function() {
		if($('.goscale-plugins-presentation').length > 0) {
			$('.goscale-plugins-presentation').goscalePluginsPresentations();
		}
	};
	
	$(function() {
		plugins.goscalePluginsPresentations();
	});
})(jQuery);