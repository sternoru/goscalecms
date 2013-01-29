var plugins = plugins || {};

(function($) {
    $.fn.goscalePluginsVideos = function() {
		var $pluginContainer = $(this),
			lightbox = $pluginContainer.find('a.video-lb').length > 0 ? true : false,
			scriptExists = function(src, script) {
				if($(['head script[src*="', src, script, '.js"]'].join('')).length > 0) {
					return true;
				}
			},
			loadJSFiles = function() {
				var src = [$('head script[src*="goscale.plugins.videos.js"]').attr('src').split('goscale/js/')[0], 'goscale/js/'].join(''),
					scripts = [
						[src, 'swfobject.js'].join(''),
						[src, 'jquery.mousewheel.js'].join(''),
						[src, 'tools.scrollable-1.0.5.min.js'].join(''),
						[src, 'jquery.fancybox-1.3.4.pack.js'].join(''),
						[src, 'jquery.easing.1.3.js'].join('')
					],
					callback = function() {
						$('head script[src*="goscale.plugins.videos.js"]').attr('rel', 'ready');
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
						loadJSFile(scripts[i], (i == (ln - 1)));
					}
				}
			},
			initPlugin = function() {
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
					var params = {
						wmode: "transparent"
					};
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
					setTimeout("$('.goscale-plugins-videos').find('a.video-lb').fancybox();", 500);
				}
				else {
					$pluginContainer.find('.videoListContainer .VideoItem .VideoContainer').eq(0).click();
				}
			};
		
		if($('head script[src*="goscale.plugins.form.js"]').length > 0) {
			if($('head script[src*="goscale.plugins.videos.js"][rel="ready"]').length > 0) {
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
	
	plugins.goscalePluginsVideos = function() {
		$('.goscale-plugins-videos').goscalePluginsVideos();
	};
	
	plugins.goscalePluginsVideos();
})(jQuery);