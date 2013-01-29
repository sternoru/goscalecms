var plugins = plugins || {};

(function($) {
    $.fn.goscalePluginsPicturesThumbnails = function() {
		var $picturesContainer = $(this),
			autoplay = $picturesContainer.data('autoplay') == 'True' ? true : false,
			$gallery = $picturesContainer.find('.gallery'),
			scriptExists = function(src, script) {
				if($(['head script[src*="', src, script, '.js"]'].join('')).length > 0) {
					return true;
				}
			},
			loadJSFiles = function() {
				var src = [$('head script[src*="goscale.plugins.pictures.thumbnails.js"]').attr('src').split('goscale/js/')[0], 'goscale/js/'].join(''),
					scripts = [
						[src, 'jquery.easing.1.3.js'].join(''),
						[src, 'jquery.galleryview-3.0-dev.js'].join(''),
						[src, 'jquery.timers-1.2.js'].join('')
					],
					callback = function() {
						$('head script[src*="goscale.plugins.pictures.thumbnails.js"]').attr('rel', 'ready');
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
				$gallery.galleryView({
					panel_width: $picturesContainer.data('width') ? $picturesContainer.data('width') : undefined,
					panel_height: $picturesContainer.data('height') ? $picturesContainer.data('height') : undefined,
					frame_width: $picturesContainer.data('thumbnailWidth') ? $picturesContainer.data('thumbnailWidth') : undefined,
					frame_height: $picturesContainer.data('thumbnailHeight') ? $picturesContainer.data('thumbnailHeight') : undefined,
					autoplay: autoplay
				});
			};
		
		if($('head script[src*="goscale.plugins.form.js"]').length > 0) {
			if($('head script[src*="goscale.plugins.pictures.thumbnails.js"][rel="ready"]').length > 0) {
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
	
	plugins.goscalePluginsPicturesThumbnails = function() {
		$('.goscale-plugins-pictures.thumbnails').goscalePluginsPicturesThumbnails();
	};
	
	plugins.goscalePluginsPicturesThumbnails();
})(jQuery);