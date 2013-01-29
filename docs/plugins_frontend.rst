2. Plugins front-end
====================

All the plugins are located in the goscalecms app "goscale" folder, then in "plugins". There is also a second subfolder, "static" containing the media files used by these plugins (js, css and images).

2.1. Templates
--------------------

The "plugins" folder contains all the plugins (each plugin having its own folder at its name).
In their "templates" sub folders are their templates, each one corresponding to a specific view, that you can choose in the "template" dropdown of a plugin in the admin.
 
In all these templates you have access to 2 main variables :

* {{ title }} : a string containing the title of the page, set in the "title" field of a plugin in the admin
* {{ posts }} : a dictionary containig the content to display on the page (videos, rss feeds, pictures, ...)

Then, each plugin has it's own specific secondary variables to display additional information or choose a specific layout.
 
For each new plugin, always use the same structure as the other plugin's templates (to include the base css and js files). To include plugin's specific js and css files (used by dependencies like jquery plugins), use these URLs: ::
 
	{{ STATIC_URL }}goscale/css/your.css.file.css
	{{ STATIC_URL }}goscale/js/your.js.file.js
 
Also, if your plugin needs you to add specific css to make its default style and/or specific js to make it run, use these URLs: ::
 
	{{ STATIC_URL }}goscale/css/goscale.plugins.pluginname.css
	{{ STATIC_URL }}goscale/js/goscale.plugins.pluginname.js
 
In these URLs, replace pluginname by the name of your plugin.
 
 
2.2. Static files
--------------------
 
They should all be in the "static" subfolder, in "js" for the javascript files, "css" for the css files and "img" for the images.
 
In the specific js file, you should create a jquery plugin that's called only if a certain class is found on the page, example: ::
 
	(function($) {
	    $.fn.goscalePluginsVideos = function() { // jquery plugin creation
			// your plugin's js here
		};
		$('.goscale-plugins-videos').goscalePluginsVideos(); // check for the specific class to run the jquery plugin
	})(jQuery);
 
Eventually, always include at the end of the css block a css file located in the themes's folder of the "django_cms_template" project that can be used to override the style of the plugin for each theme to make it fit to it's design using this exact URL: ::
 
	{{ STATIC_THEME_URL }}css/plugins-override.css


2.3. Ajaxlinks
-----------------

In order to make the ajalinks plugin work with the goscale's plugins, you'll need to add this piece of code in ajaxlink's callback: ::

	var $plugin = $(content).find('[data-pluginjs]');

	if($plugin.length > 0) {
		var file = $plugin.eq(0).data('pluginjs'),
			callback = $plugin.eq(0).data('plugincb');
		
		if($(['head script[src*="', file, '"]'].join('')).length > 0) {
			plugins[callback]();
		}
		else {
			head.js(file);
		}
	}

Please make sure that you're using the javascript plugin "head.js".

Then, your goscale plugin's template should have a "data-pluginjs" and a "data-plugincb" data attribute on any of it's html element containing the plugin's main javascript file and the function to call it, example: ::

	<div class="goscale-plugins-videos" data-pluginjs="{{ STATIC_URL }}goscale/js/goscale.plugins.videos.js" data-plugincb="goscalePluginsVideos">

According to this example, your main js file is "goscale.plugins.videos.js" and it should initialize the "plugins" namespace (if it doesn't exist), and add a "plugins.goscalePluginsVideos" function that will be called by ajaxlinks' callback and initiate the goscale's plugin. All the needed js files should be removed from the template and put in the plugin's main js file. To continue on the videos plugin example, it's main js will then be: ::

	var plugins = plugins || {}; // initiates/uses the plugins namespace
	
	(function($) {
		$.fn.goscalePluginsVideos = function() { // your jquery plugin
			//your plugin's needed variables here
			var loadJSFiles = function() { // function to call to load the needed js files, that were in the plugin's template before
				var src = [$('head script[src*="goscale.plugins.videos.js"]').attr('src').split('goscale/js/')[0], 'goscale/js/'].join(''),
					scripts = [
						[src, 'swfobject.js'].join(''), // ------------------
						[src, 'jquery.mousewheel.js'].join(''), // ----------
						[src, 'tools.scrollable-1.0.5.min.js'].join(''), // --> the names of the js files taken from the template
						[src, 'jquery.fancybox-1.3.4.pack.js'].join(''), // -
						[src, 'jquery.easing.1.3.js'].join('') // -----------
					],
					callback = function() { // callback called after the last js file is loaded
						$('head script[src*="goscale.plugins.videos.js"]').attr('rel', 'ready'); // this js file's name
						initPlugin(); // calling you plugin's code
					},
					checkFiles = function() { // function to check which js file to load (if they aren't already loaded by any other plugin)
						var tmp = [];
						for(var i = 0, ln = scripts.length; i < ln; i++) {
							if($(['head script[src*="', scripts[i], '"]'].join('')).length == 0) {
								tmp.push(scripts[i]);
							}
						}
						scripts = tmp;
					},
					loadJSFile = function(filename, last) { // function to load the remaining needed js files
						var fileref = document.createElement('script');
						fileref.type = 'text/javascript';
						fileref.src = filename;
						if(last) {
							fileref.onload = callback;
						}
						document.getElementsByTagName("head")[0].appendChild(fileref);
					};
				
				checkFiles(); // checking which js files to load
				if(scripts.length == 0) { // if no files to load, calling your plugin's code
					callback();
				}
				else { // else loading all the needed js files
					for(var i = 0, ln = scripts.length; i < ln; i++) {
						loadJSFile(scripts[i], (i == (ln - 1)));
					}
				}
			},
			initPlugin = function() { // function to call if/when the needed js files are loaded
				// your plugin's code here
			}; // end of your code
		
			if($('head script[src*="goscale.plugins.form.js"]').length > 0) { // if the main js files are there
				if($('head script[src*="goscale.plugins.videos.js"][rel="ready"]').length > 0) { // and the videos plugin's js files too
					initPlugin(); // run your plugin's code
				}
				else {
					loadJSFiles(); // else load the plugin's needed js files
				}
			}
			else {
				head.ready('goscale.plugins.form.js', function() { // else we're waiting for them to then load the plugin's js files
					loadJSFiles();
				});
			}
		}; // end of your jquery plugin
		
		plugins.goscalePluginsVideos = function() { // the needed "plugins" namespace function to run your plugin's code from ajaxlinks' callback
			$('.goscale-plugins-videos').goscalePluginsVideos(); // your plugin's call
		};
		
		plugins.goscalePluginsVideos(); // runs the first time this file is loaded (or each time it's loaded if ajaxlinks isn't used)
	})(jQuery); // end of file

And the plugin's template js section should look like this (in videos.html for example): ::

	{% goscale_addtoblock "js" %} // goscale's sekizai tag
		<script type="text/javascript">
			head.ready('scripts', function() { // where scripts is the head.js label of the last of your local main js files, to be sure that they are ready before the plugin is called
				head.js('{{ STATIC_URL }}goscale/js/goscale.plugins.videos.js'); // your plugin's main js file
			});
		</script>
	{% endaddtoblock %}