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
		// setInterval(floto.changePhoto, floto.displayTime);
		setInterval(floto.triggerPhotoListRefresh, floto.refreshListTime);
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
		if(floto.$frame.find("img").length){
			floto.log("First photo already set.");
		}else{
			floto.nextPhotoIndex = 0;
			photo = floto.photoList[floto.nextPhotoIndex];
			$('<img/>')
				.attr('src', photo.serving_url)
				.addClass('current')
				.addClass('rotation' + String(photo.rotation))
				.appendTo(floto.$frame);
			floto.putNextPhotoInPlace();
		}
	},

	putNextPhotoInPlace: function(){
		if(floto.nextPhotoIndex >= floto.photoList.length){
			floto.nextPhotoIndex = -1;
		}
		photo = floto.photoList[floto.nextPhotoIndex + 1];
		$('<img/>')
			.attr('src', photo.serving_url)
			.addClass('upnext')
			.addClass('rotation' + String(photo.rotation))
			.appendTo(floto.$frame);
	},

	changePhoto: function(){
		floto.log("changePhoto called");
		floto.$frame.find("img.upnext").animate({"opacity":1}, 400);
		floto.$frame.find("img.current").animate(
			{"opacity": 0}, 400, "swing",
			function(){
				$(this).remove();
				floto.$frame.find("img.upnext").removeClass("upnext").addClass("current");
				floto.nextPhotoIndex ++;
				floto.putNextPhotoInPlace();
			}
		);
	}
};

floto.init();
