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
		$(function() {
			$('.goscale-plugins-videos').goscalePluginsVideos(); // check for the specific class to run the jquery plugin
		});
	})(jQuery);


2.3. Ajaxlinks
-----------------

In order to make the ajaxlinks plugin work with the goscale's plugins, you'll need to add a "data-callback" attribute to the javascript files in your plugin's template containing the name of the function you need to call each time a page containing your plugin is loaded. Example: ::

	<script type="text/javascript" src="{{ STATIC_URL }}goscale/js/goscale.plugins.videos.js" data-callback="plugins.goscalePluginsVideos"></script>