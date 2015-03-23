var floto = {

	photoListURL: "/get-photo-list/",
	triggerPhotoListRefreshURL: "/trigger-photo-list-refresh/",
	photoList: [],
	nextPhotoIndex: null,
	displayTime: 15000,
	refreshListTime: 1000 * 60 * 60, // 1 hour
	$frame: null,

	init: function(){
		floto.$frame = $("#frame");
		floto.getPhotoList();
		setInterval(floto.changePhoto, floto.displayTime);
		setInterval(floto.triggerPhotoListRefresh, floto.refreshListTime);
		floto.tryEnterFullScreen();
	},

	log: function(msg){
		if(typeof(console) != "undefined"){
			console.log(msg);
		}
	},

	getPhotoList: function(){
		$.get(floto.photoListURL, null, floto.getPhotoListSuccess);
	},

	getPhotoListSuccess: function(data){
		floto.log("getPhotoListSuccess called");
		if(typeof(data) == "object"){
			// Only replace our list of photos if the new data is different, otherwise we lose
			// where we got to in terms of which photos we have/haven't displayed
			if(floto.photoList.length != data.length){
				floto.photoList = data;
				floto.setFirstPhoto();
			}
		}else{
			floto.log("Photo list data is not an object");
			floto.log(String(typeof(data)));
			floto.log(data);
		}
	},

	triggerPhotoListRefresh: function(){
		// Calls a URL on the server which triggers it to go and refresh its list of photos from Flickr
		floto.log("Triggering photo list refresh (server side)");
		$.get(floto.triggerPhotoListRefreshURL, null, floto.getPhotoList);
	},

	insertImg: function(photo, classes){
		// Create a jQuery object of a <img> tag for the given photo object from the API
		floto.log("insertImg called");
		return $('<img/>')
			.attr('src', photo.serving_url)
			.addClass('rotation' + String(photo.rotation))
			.addClass(classes)
			.load(floto.fixTransformedDimensions)
			.appendTo(floto.$frame);
	},

	setFirstPhoto: function(){
		floto.log("setFirstPhoto called");
		if(floto.$frame.find("img").length){
			floto.log("First photo already set.");
		}else{
			floto.nextPhotoIndex = 0;
			photo = floto.photoList[floto.nextPhotoIndex];
			var $img = floto.insertImg(photo, 'current');
			floto.putNextPhotoInPlace();
		}
	},

	putNextPhotoInPlace: function(){
		floto.log("putNextPhotoInPlace called");
		if(floto.nextPhotoIndex >= floto.photoList.length){
			floto.nextPhotoIndex = -1;
		}
		photo = floto.photoList[floto.nextPhotoIndex + 1];
		var $img = floto.insertImg(photo, 'upnext');
	},

	changePhoto: function(){
		floto.log("changePhoto called");
		floto.$frame.find("img.upnext").animate({"opacity":1}, 400);
		floto.$frame.find("img.current").animate(
			{"opacity": 0}, 400, "swing",
			function(){
				floto.log("animation finished");
				$(this).remove();
				floto.$frame.find("img.upnext").removeClass("upnext").addClass("current");
				floto.nextPhotoIndex ++;
				floto.putNextPhotoInPlace();
			}
		);
	},

	fixTransformedDimensions: function(){
		// We rotate photos using CSS transform: rotate.  The problem is that the photo still
		// effectively has its original dimensions, so the width is the height and the height is
		// the width, which screws up other CSS.  This attempts to fix that.
		floto.log("fixTransformedDimensions called");
		var $img = $(this);
		if($img.hasClass('rotation90') || $img.hasClass('rotation90')){
			var new_max_height = Math.min(parseInt($img.css('max-width')), $img.width());
			var new_max_width = Math.min(parseInt($img.css('max-height')), $img.height());
			$img.css({'max-height': new_max_height + "px", 'max-width': new_max_width + "px"});
			// $img.css({width: $img.height() + "px", height: $img.width() + "px"});
		}
	},

	tryEnterFullScreen: function(){
		// Most browsers don't allow fullscreen unless it's triggered by a user action, but
		// if that restriction is disabled we can do it directly
		floto.enterFullScreen(); // This doesn't actually throw an error
		// And there's no way to check if full screen is activated
		$(document).on('click', floto.enterFullScreen); // So we have to do this anyway
	},

	enterFullScreen: function(){
		floto.$frame[0].mozRequestFullScreen();
	}
};

floto.init();
