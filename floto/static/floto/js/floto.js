var floto = {

	photoListURL: "/get-photo-list/",
	triggerPhotoListRefreshURL: "/trigger-photo-list-refresh/",
	triggerAlbumInfoRefreshURL: "/trigger-album-info-refresh/",
	photoList: [],
	nextPhotoIndex: null,
	displayTime: 15000,
	infoDisplayTime: 5000,
	transitionTime: 2000, // the time that our CSS transition takes
	refreshListTime: 1000 * 60 * 60, // 1 hour
	refreshAlbumInfoTime: 1000 * 60 * 97, // 97 minutes, deliberately offset from the list refresh interval
	hideMouseTime: 5000,
	mouseHideTimeoutlID: null,
	$frame: null,

	init: function(){
		floto.$frame = $("#frame");
		floto.getPhotoList();
		floto.$frame.find("img").load(floto.fixTransformedDimensions);
		setInterval(floto.changePhoto, floto.displayTime);
		setInterval(floto.triggerPhotoListRefresh, floto.refreshListTime);
		setInterval(floto.triggerAlbumInfoRefresh, floto.refreshAlbumInfoTime);
		floto.tryEnterFullScreen();
		floto.resetMouseHide();
		$(document).on("mousemove", floto.resetMouseHide);
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

	triggerAlbumInfoRefresh: function(){
		// Calls a URL on the server which triggers it to go and refresh the album info for existing photos
		floto.log("Triggering album info refresh (server side)");
		$.get(floto.triggerAlbumInfoRefreshURL);
	},

	setFirstPhoto: function(){
		floto.log("setFirstPhoto called");
		if(floto.$frame.find("img.current").attr("src")){
			floto.log("First photo already set.");
		}else{
			floto.nextPhotoIndex = -1; // because putNextPhotoInPlace puts the NEXT photo in place
			floto.putNextPhotoInPlace();
			floto.changePhoto();
		}
	},

	putNextPhotoInPlace: function(){
		floto.log("putNextPhotoInPlace called");
		if(floto.nextPhotoIndex >= floto.photoList.length){
			floto.nextPhotoIndex = -1;
		}
		// It's important that we re-use the same <img> tag because browsers keep old elements
		// in memory (as oldChild), so if we create a new <img> each time we slowly eat up all
		// the memory and the computer grinds to a halt.
		photo = floto.photoList[floto.nextPhotoIndex + 1];
		floto.$frame.find("img.upnext")
			.attr("style", "") // remove the old max-height/-width that were added by fixTransformedDimensions
			.attr("src", photo.serving_url) // this triggers fixTransformedDimensions, hence it's second
			.attr("class", "upnext") //remove all the rotationX classes
			.addClass("rotation" + photo.rotation);
			//.load(floto.fixTransformedDimensions) // assume this is already done
		var $items = $(".info.upnext .item");
		var has_info = false;
		$items.text(""); // wipe current info
		$.each(
			['title', 'album', 'location', 'date_taken'],
			function(index, item){
				var $item = $items.filter("." + item);
				if(photo[item]){
					$item.text(photo[item]).removeClass("empty");
					has_info = true;
				}else{
					$item.addClass("empty");
				}
			}
		);
		// Set a class so that showPhotoInfo knows whether to show the info bar or not
		if(has_info){
			$(".info.upnext").addClass("hasinfo");
		}else{
			$(".info.upnext").removeClass("hasinfo");
		}
	},

	changePhoto: function(){
		floto.log("changePhoto called");
		// Get all elements before we change the classes, otherwise which is which will change
		var $upnexts = $(".upnext");  // Both image and info
		var $currents =  $(".current");
		// trigger the CSS transitions
		$upnexts.removeClass("upnext").addClass("current");
		$currents.removeClass("current visible").addClass("upnext");
		// Put the next photo into place once the transitions have finished.
		// We want the info about the current photo to be displayed for the last few seconds before
		// we show the next one, so schedule it to be shown <infoDisplayTime> before the photo changes
		setTimeout(floto.showPhotoInfo, floto.displayTime - floto.infoDisplayTime);
		setTimeout(floto.putNextPhotoInPlace, floto.transitionTime);
		floto.nextPhotoIndex ++;
	},

	showPhotoInfo: function(){
		floto.log("showPhotoInfo called");
		floto.log($(".info.current.hasinfo").length ? "There is info to show" : "There is no info to show");
		// Slide the info bar up into view, assuming it's got something in it to show
		$(".info.current.hasinfo").addClass("visible");
	},

	fixTransformedDimensions: function(){
		// We rotate photos using CSS transform: rotate.  The problem is that the photo still
		// effectively has its original dimensions, so the width is the height and the height is
		// the width, which screws up other CSS.  This attempts to fix that.
		floto.log("fixTransformedDimensions called");
		var $img = $(this);
		if($img.hasClass('rotation90') || $img.hasClass('rotation-90') || $img.hasClass('rotation270')){
			floto.log("rotated photo");
			var new_max_height = Math.min(floto.$frame.width(), $img.width());
			var new_max_width = Math.min(floto.$frame.height(), $img.height());
			$img.css({'max-height': new_max_height + "px", 'max-width': new_max_width + "px"});
			// $img.css({width: $img.height() + "px", height: $img.width() + "px"});
		}
	},

	tryEnterFullScreen: function(){
		// Most browsers don't allow fullscreen unless it's triggered by a user action, but
		// if that restriction is disabled we can do it directly
		floto.enterFullScreen(); // This doesn't actually throw an error
		// And there's no way to check if full screen is activated
		$(document).on("click", "img", floto.enterFullScreen); // So we have to do this anyway
	},

	enterFullScreen: function(){
		try{
			floto.$frame[0].mozRequestFullScreen();
		}catch(e){
			floto.log("Could not enter fullscreen: " + String(e));
		}

	},

	hideMouse: function(){
		$("body").addClass("hidemouse");
	},

	showMouse: function(){
		$("body").removeClass("hidemouse");
	},

	resetMouseHide: function(){
		clearInterval(floto.mouseHideIntervalID);
		floto.showMouse();
		floto.mouseHideTimeoutlID = setTimeout(floto.hideMouse, floto.hideMouseTime);
	}
};

floto.init();
