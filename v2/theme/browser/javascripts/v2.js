var v2 = function() {
    var $;

    var addCornersToSelectedMenuItems = function() {
        $("ul.main-menu > li > a.selected").parent().addClass("selected");
    };

    return {
        init: function() {
            $ = jQuery;

            addCornersToSelectedMenuItems();
        }
    };
} ();

jQuery(document).ready(function(){
    v2.init();
});