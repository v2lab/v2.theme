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
            var container = document.querySelectorAll('.masonry-holder');
            var msnry;
            if(container){
            	imagesLoaded( container, function() {
                    $(".masonry-holder").masonry({
                        itemSelector: '.masonry-item',
                        "gutter": 30
                    });
				// msnry = new Masonry( container, {
				// 	itemSelector: '.masonry-item',
				// 	"gutter": 30
				// });
	            });
            }

            // $("body").css("background-color","#ccc");
            var s = Snap(document.getElementById('v2-logo'));
            var scaleValue = Math.random()/2 + 1.3;
            var rotateValue = (Math.random() - 0.5) * 90;
            var skewValue = (Math.random() - 0.5) * 60;
            var myMatrix = new Snap.Matrix();

            myMatrix.scale(scaleValue,scaleValue,80,59);        // play with scaling before and after the rotate 
            myMatrix.translate(0,0);      // this translate will not be applied to the rotation
            myMatrix.rotate(rotateValue, 228, 59);        // rotate
            // var c = s.rect(0, 0, 455, 118);
            // c.attr({fill: "#cccccc"});
            var colorArr = ["#000000","#FFFFFF","#2BFF3A","#32FF9C","#FFFF2D","#B373FF","#00FFFF","#FF434E","#5FBEFF"];
            var randColor = colorArr[Math.floor(Math.random() * colorArr.length)];

            Snap.load("../++resource++v2.theme.images/v2_logo.svg", function (f) {
                var main = f.select("#main");
                // main.transform("r18 0 0");
                // main.transform(myMatrix);
                main.transform("scale("+scaleValue+") rotate("+rotateValue+", 180, 59) skewX("+skewValue+")");
                main.selectAll("path").attr({
                    fill: randColor
                });
                s.append(main);
            });


        }
    };
} ();

jQuery(document).ready(function(){
    v2.init();
});