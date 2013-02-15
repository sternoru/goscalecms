var plugins = plugins || {};

plugins.goscalePluginsFeeds = function() {
	if(navigator.appName == 'Microsoft Internet Explorer') {
		$('body').addClass('ie');
	}
};

$(function() {
	plugins.goscalePluginsFeeds();
});