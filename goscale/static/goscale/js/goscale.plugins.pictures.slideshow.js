(function($) {
    $.fn.goscalePluginsPictures = function() {
		var $picturesContainer = $(this),
			autoplay = $picturesContainer.data('autoplay') == 'True' ? true : false;
		
		if($picturesContainer.data('width')) {
			$picturesContainer.find(".slides_container").css('width', $picturesContainer.data('width'));
			$picturesContainer.find(".slides_container img").css('width', $picturesContainer.data('width') - 22);
		}
		if($picturesContainer.data('height')) {
			$picturesContainer.find(".slides_container").css('height', $picturesContainer.data('height'));
			$picturesContainer.find(".slides_container img").css('height', $picturesContainer.data('height') - 22);
		}
		$picturesContainer.find(".slides").slides({
			preload: true,
			preloadImage: $picturesContainer.find('.loader img').attr('src'),
			play: autoplay ? 4000 : 0,
			hoverPause: true
		});
	};
	$('.goscale-plugins-pictures').goscalePluginsPictures();
})(jQuery);