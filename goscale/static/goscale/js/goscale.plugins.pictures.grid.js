var plugins = plugins || {};

(function($) {
    $.fn.goscalePluginsPicturesGrid = function() {
		var $picturesContainer = $(this),
			autoplay = $picturesContainer.data('autoplay') == 'True' ? true : false,
			$container 	= $picturesContainer.find('.am-container'),
			$imgs		= $container.find('img').hide(),
			totalImgs	= $imgs.length,
			cnt			= 0,
			scriptExists = function(src, script) {
				if($(['head script[src*="', src, script, '.js"]'].join('')).length > 0) {
					return true;
				}
			},
			loadJSFiles = function() {
				var src = [$('head script[src*="goscale.plugins.pictures.grid.js"]').attr('src').split('goscale/js/')[0], 'goscale/js/'].join(''),
					scripts = [
						[src, 'jquery.montage.min.js'].join(''),
						[src, 'jquery.prettyPhoto.js'].join('')
					],
					callback = function() {
						$('head script[src*="goscale.plugins.pictures.grid.js"]').attr('rel', 'ready');
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
		
		if($('head script[src*="goscale.plugins.form.js"]').length > 0) {
			if($('head script[src*="goscale.plugins.pictures.grid.js"][rel="ready"]').length > 0) {
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
	
	plugins.goscalePluginsPicturesGrid = function() {
		$('.goscale-plugins-pictures.grid').goscalePluginsPicturesGrid();
	};
	
	plugins.goscalePluginsPicturesGrid();
})(jQuery);