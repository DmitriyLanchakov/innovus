/* adds a parameter to an url */
function insert_into_url(url, name, value){
	if(url.substr(url.length-1, url.length)== "&"){
		url = url.substr(0, url.length-1);
	}
	dash_splits = url.split("#");
	url = dash_splits[0];
	var splits = url.split(name + "=");
	if (splits.length == 1){
		splits = url.split(name);
	}
	var get_args = false;
	if(url.split("?").length>1){
		get_args = true;
	}
	if(splits.length > 1){
		var after = "";
		if (splits[1].split("&").length > 1){
			after = splits[1].split("&")[1];
		}
		url = splits[0] + name;
		if (value){
			url += "=" + value
		}
		url += "&" + after;
	}else{
		if(get_args){
			url = url + "&" + name;
		}else{
			url = url + "?" + name;
		}
		if(value){
			url += "=" + value;
		}
	}
	if(dash_splits.length>1){
		url += dash_splits[1];
	}
	if(url.substr(url.length-1, url.length)== "&"){
		url = url.substr(0, url.length-1);
	}
	return url;
}

/* removes a parameter from an url */
function remove_from_url(url, name){
	var dash_splits = url.split("#");
	url = dash_splits[0];
	var splits = url.split(name + "=");
	if(splits.length == 1){
		splits = url.split(name);
	}
	if(splits.length > 1){
		var after = "";
		if (splits[1].split("&").length > 1){
			after = splits[1].split("&")[1];
		}
		if (splits[0].substr(splits[0].length-2, splits[0]-length-1)=="?" || !after){
			url = splits[0] + after;
		}else{
			url = splits[0] + "&" + after;
		}
	}
	if(url.substr(url.length-1,1) == "?"){
		url = url.substr(0, url.length-1);
	}
	if(dash_splits.length > 1 && dash_splits[1]){
		url += "#" + dash_splits[1];
	}
	return url;
}

var django = {
    "jQuery": jQuery.noConflict(true)
};
window.$ = django.jQuery;
window.jQuery = django.jQuery;

(function($){
    $('html').ajaxSend(function(event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });
})(jQuery);
