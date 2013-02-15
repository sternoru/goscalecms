var plugins = plugins || {};

(function($) {
    $.fn.goscalePluginsPicturesGrid = function() {
		if(navigator.appName == 'Microsoft Internet Explorer') {
			$('body').addClass('ie');
		}
		var $picturesContainer = $(this),
			autoplay = $picturesContainer.data('autoplay') == 'True' ? true : false,
			$container 	= $picturesContainer.find('.am-container'),
			$imgs		= $container.find('img').hide(),
			totalImgs	= $imgs.length,
			cnt			= 0;
			
		$imgs.each(function(i) {
			var $img	= $(this);
			$('<img/>').load(function() {
				++cnt;
				if( cnt === totalImgs ) {
					$container.removeClass('loading');
					$imgs.show();
					$container.montage({
						liquid : true,
						margin : 2,
						minw: 90,
						fillLastRow : false,
						alternateHeight	: true,
						alternateHeightRange : {
							min	: 90,
							max	: 288
						}
					});
				}
			}).attr('src',$img.attr('src'));
		});	
		
		$picturesContainer.find("a[rel^='prettyPhoto']").prettyPhoto({
			show_title: false, /* true/false */
			default_width: 500,
			default_height: 344,
			counter_separator_label: '/', /* The separator for the gallery counter 1 "of" 2 */
			theme: 'dark_rounded', /* light_rounded / dark_rounded / light_square / dark_square / facebook */
			horizontal_padding: 20, /* The padding on each side of the picture */
			deeplinking: true, /* Allow prettyPhoto to update the url to enable deeplinking. */
			overlay_gallery: true, /* If set to true, a gallery will overlay the fullscreen image on mouse over */
			keyboard_shortcuts: true, /* Set to false if you open forms inside prettyPhoto */
			changepicturecallback: function(){}, /* Called everytime an item is shown/changed */
			callback: function(){}, /* Called when prettyPhoto is closed */
			ie6_fallback: true,
			social_tools: false
		});
	};
	
	plugins.goscalePluginsPicturesGrid = function() {
		if($('.goscale-plugins-pictures.grid').length > 0) {
			$('.goscale-plugins-pictures.grid').goscalePluginsPicturesGrid();
		}
	};
	
	$(function() {
		plugins.goscalePluginsPicturesGrid();
	});
})(jQuery);