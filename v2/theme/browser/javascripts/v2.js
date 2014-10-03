var v2 = function() {
    var $;

    var addCornersToSelectedMenuItems = function() {
        $("ul.main-menu > li > a.selected").parent().addClass("selected");
    };

    return {
        init: function() {
            $ = jQuery;

            addCornersToSelectedMenuItems();


            // Initializing Masonry
            var container = document.querySelector('.masonry-holder');
            var msnry;
            if(container){
            	imagesLoaded( container, function() {
				msnry = new Masonry( container, {
					itemSelector: '.masonry-item',
					"gutter": 30
				});
	            });
            }


        }
    };
} ();

jQuery(document).ready(function(){
    v2.init();
});