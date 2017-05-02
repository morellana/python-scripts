var system = require('system');

if (system.args.length < 2){
	console.log("Se necesita parametro URL");
	phantom.exit();
}

var url = system.args[1];
var page = require('webpage').create();

// error handler
page.onError = function(msg, trace) {
}

page.open(url, function (status) {
	if (status == 'success') {
		var download_link = page.evaluate(function(){
			return document.getElementById('dlbutton').href
		})

		console.log(download_link);
	}
	phantom.exit();
});
	   
