====================
Plugins front-end
====================

All the plugins are located in the goscalecms app "goscale" folder, then in "plugins". There is also a second subfolder, "static" containing the media files used by these plugins (js, css and images).

Templates
--------------------

The "plugins" folder contains all the plugins (each plugin having its own folder at its name).
In their "templates" sub folders are their templates, each one corresponding to a specific view, that you can choose in the "template" dropdown of a plugin in the admin.
 
In all these templates you have access to 2 main variables :

* {{ title }} : a string containing the title of the page, set in the "title" field of a plugin in the admin
* {{ posts }} : a dictionary containig the content to display on the page (videos, rss feeds, pictures, ...)

Then, each plugin has it's own specific secondary variables to display additional information or choose a specific layout. You can check all the variables available and their content at any time by adding this line to a template: ::
 
	<textarea>{{ debug }}</textarea>
 
For each new plugin, always use the same structure as the other plugin's templates (to include the base css and js files). To include plugin's specific js and css files (used by dependencies like jquery plugins), use these URLs: ::
 
	{{ STATIC_URL }}goscale/css/your.css.file.css
	{{ STATIC_URL }}goscale/js/your.js.file.js
 
Also, if your plugin needs you to add specific css to make its default style and/or specific js to make it run, use these URLs: ::
 
	{{ STATIC_URL }}goscale/css/goscale.plugins.pluginname.css
	{{ STATIC_URL }}goscale/js/goscale.plugins.pluginname.js
 
In these URLs, replace pluginname by the name of your plugin.
 
 
Media files
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