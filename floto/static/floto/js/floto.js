var floto = {

	photoListURL: "/get-photo-list/",
	triggerPhotoListRefreshURL: "/trigger-photo-list-refresh/",
	photoList: [],
	nextPhotoIndex: null,
	displayTime: 15000,
	transitionTime: 2000, // the time that our CSS transition takes
	refreshListTime: 1000 * 60 * 60, // 1 hour
	$frame: null,

	init: function(){
		floto.$frame = $("#frame");
		floto.getPhotoList();
		floto.$frame.find("img").load(floto.fixTransformedDimensions);
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

	setFirstPhoto: function(){
		floto.log("setFirstPhoto called");
		if(floto.$frame.find("img.current").attr("src")){
			floto.log("First photo already set.");
		}else{
			floto.nextPhotoIndex = -1; // because putNextPhotoInPlace puts the NEXT photo in place
			floto.putNextPhotoInPlace();
		}
	},

	putNextPhotoInPlace: function(){
		floto.log("putNextPhotoInPlace called");
		if(floto.nextPhotoIndex >= floto.photoList.length){
			floto.nextPhotoIndex = -1;
		}
		// It's important that we re-use the same <img> tag because browser's keep old elements
		// in memory (as oldChild), so if we create a new <img> each time we slowly eat up all
		// the memory and the computer grinds to a halt.
		photo = floto.photoList[floto.nextPhotoIndex + 1];
		floto.$frame.find("img.upnext")
			.attr("src", photo.serving_url)
			.attr("class", "upnext") //remove all the rotationX classes
			//.load(floto.fixTransformedDimensions) // assume this is already done
	},

	changePhoto: function(){
		floto.log("changePhoto called");
		// Get both images before we change the class, otherwise which image is which will change
		var $upnext = floto.$frame.find("img.upnext");
		var $current =  floto.$frame.find("img.current");
		// trigger the CSS transitions
		$upnext.removeClass("upnext").addClass("current");
		$current.removeClass("current").addClass("upnext");
		// put the next photo into place once the transitions have finished
		setTimeout(floto.putNextPhotoInPlace, floto.transitionTime);
		floto.nextPhotoIndex ++;
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
