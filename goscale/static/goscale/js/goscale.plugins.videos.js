(function($) {
    $.fn.goscalePluginsVideos = function() {
		var $pluginContainer = $(this),
			lightbox = $pluginContainer.find('a.video-lb').length > 0 ? true : false;
		
		$pluginContainer.find('.videoListContainer .videos').scrollable({
			horizontal:true,
			size: Math.floor($pluginContainer.find('.videoListContainer').width() / ($pluginContainer.find('.videoListContainer .VideoItem').width() + 13)),
			items: '.VideosList',
			next: '.NextScroll',
			prev: '.PrevScroll',
			disabledClass: 'disabled'
		});
		$pluginContainer.find('.videoListContainer .VideoItem .VideoContainer').click(function(event) {
			event.preventDefault();
			$pluginContainer.find('.videoListContainer .VideoItem .VideoContainer').removeClass('selected');
			$(this).addClass('selected');
			var $container = $pluginContainer.find('.video-content .selectedVideoContainer'),
				rand = Math.floor((Math.random()*1000)+1);
			
			$container.html(['<div id="video', rand, '"></div>'].join(''));
			swfobject.embedSWF($(this).data('url'), ['video', rand].join(''), "425", "344", "9.0.0");
			var html = [];
			html.push('<a href="#">', $(this).data('title'), '</a><br />');
			if($(this).data('author')) {
				var authorUrl = $(this).data('authorUrl') ? $(this).data('authorUrl') : '#';
				html.push('Author: <a href="', authorUrl, '" target="_blank">', $(this).data('author'), '</a>');
			}
			if($(this).data('rating')) {
				html.push('<div class="VideoRating">Rating: <img src="/media/images/rating/', $(this).data('rating'), '.gif" /></div>');
			}
			if($(this).data('views')) {
				html.push('<div>Views: ', $(this).data('views'), '</div>');
			}
			$pluginContainer.find('.video-content .selectedVideoInformation').html(html.join(''));
		});
		
		if(lightbox) {
			$pluginContainer.find('a.video-lb').fancybox();
		}
		else {
			$pluginContainer.find('.videoListContainer .VideoItem .VideoContainer').eq(0).click();
		}
	};
	$('.goscale-plugins-videos').goscalePluginsVideos();
})(jQuery);