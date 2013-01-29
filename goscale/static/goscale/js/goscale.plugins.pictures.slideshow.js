var plugins = plugins || {};

(function($) {
    $.fn.goscalePluginsPicturesSlideshow = function() {
		var $picturesContainer = $(this),
			autoplay = $picturesContainer.data('autoplay') == 'True' ? true : false,
			scriptExists = function(src, script) {
				if($(['head script[src*="', src, script, '.js"]'].join('')).length > 0) {
					return true;
				}
			},
			loadJSFiles = function() {
				var src = [$('head script[src*="goscale.plugins.pictures.slideshow.js"]').attr('src').split('goscale/js/')[0], 'goscale/js/'].join(''),
					scripts = [
						[src, 'slides.min.jquery.js'].join('')
					],
					callback = function() {
						$('head script[src*="goscale.plugins.pictures.slideshow.js"]').attr('rel', 'ready');
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
			
		if($('head script[src*="goscale.plugins.form.js"]').length > 0) {
			if($('head script[src*="goscale.plugins.pictures.slideshow.js"][rel="ready"]').length > 0) {
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
	
	plugins.goscalePluginsPicturesSlideshow = function() {
		$('.goscale-plugins-pictures.slideshow').goscalePluginsPicturesSlideshow();
	};
	
	plugins.goscalePluginsPicturesSlideshow();
})(jQuery);