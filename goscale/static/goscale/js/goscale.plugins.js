var plugins = {};

plugins.parseScript = function(strcode) {
	var scripts = new Array();         // Array which will store the script's code
	
	console.log('ok');
	// Strip out tags
	while(strcode.indexOf("<script") > -1 || strcode.indexOf("</script") > -1) {
		var s = strcode.indexOf("<script");
		var s_e = strcode.indexOf(">", s);
		var e = strcode.indexOf("</script", s);
		var e_e = strcode.indexOf(">", e);

		// Add to scripts array
		scripts.push(strcode.substring(s_e+1, e));
		// Strip from strcode
		strcode = strcode.substring(0, s) + strcode.substring(e_e+1);
	}

	// Loop through every script collected and eval it
	for(var i = 0, ln = scripts.length; i < ln; i++) {
		try {
			console.log(scripts[i]);
			eval(scripts[i]);
		}
		catch(ex) {
			console.log('error');// do what you want here when a script fails
		}
	}
};