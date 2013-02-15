$(function(){
	if($.fn.ajaxlinks) {
		var defaultConfig = {
    		load_to: '#content',
			load_from: '#content',
			loader: '<span class="ajax-loader"></span>',
			use_sammy: true,
			goto_top: true,
			add_scripts: true,
			ajaxify_content: true
    	};
		var newConfig = ajaxConfig || {};
		var config = $.extend(defaultConfig, newConfig);
		$('a').filter(":not('.no-al a, a.no-al')").ajaxlinks(config);
	}
});