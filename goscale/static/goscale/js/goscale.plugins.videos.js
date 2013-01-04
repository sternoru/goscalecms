(function($) {
    $.fn.goscalePluginsVideos = function() {
		var $pluginContainer = $(this);
		$pluginContainer.find('.videoListContainer .videos').scrollable({
			horizontal:true,
			size: Math.floor($pluginContainer.find('.videoListContainer').width() / ($pluginContainer.find('.videoListContainer .VideoItem').width() + 13)),
			items: '.VideosList',
			next: '.NextScroll',
			prev: '.PrevScroll',
			disabledClass: 'disabled'
		});
		$pluginContainer.find('.videoListContainer .VideoItem .VideoContainer').click(function() {
			var $container = $pluginContainer.find('#content .selectedVideoContainer'),
				rand = Math.floor((Math.random()*1000)+1);
			
			/*$container.html(['<div id="video', rand, '"></div>'].join(''));
			swfobject.embedSWF(item.video_url, $container.find('.videoContainer'), "425", "344", "9.0.0");
			var html = [];
			html.push('<a href="'+item.permanent_link+langParam+'">'+item.title+'</a><br />');
			html.push(authorLabel+': <a href="'+item.author_url+'" target="_blank">'+item.author+'</a>');
			if (typeof(item.rating) != 'undefined') html.push('<div class="VideoRating">'+ratingLabel+': <img src="/media/images/rating/'+item.rating+'.gif" alt="'+item.rating+'" /></div>');
			html.push('<div>'+viewsLabel+': '+item.view_count+'</div>');
			$('#videoInformation').html(html.join(''));
			
			var content = '';*/
		});
	};
	$('.goscale-plugins-videos').goscalePluginsVideos();
})(jQuery);