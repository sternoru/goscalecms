(function($) {
    $.fn.goscalePluginsPictures = function() {
		var $picturesContainer = $(this),
			autoplay = $picturesContainer.data('autoplay') == 'True' ? true : false,
			$gallery = $picturesContainer.find('.gallery');
		
		$gallery.galleryView({
			panel_width: $picturesContainer.data('width') ? $picturesContainer.data('width') : undefined,
			panel_height: $picturesContainer.data('height') ? $picturesContainer.data('height') : undefined,
			frame_width: $picturesContainer.data('thumbnailWidth') ? $picturesContainer.data('thumbnailWidth') : undefined,
			frame_height: $picturesContainer.data('thumbnailHeight') ? $picturesContainer.data('thumbnailHeight') : undefined,
			autoplay: autoplay
		});
	};
	$('.goscale-plugins-pictures').goscalePluginsPictures();
})(jQuery);