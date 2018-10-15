$(document).ready(function() {
        $(".joinButton").click(function() {
            $("#joinDiv").toggle();
            var game_id = $(this).attr("value");
            $("#joinId").attr("placeholder", game_id)
        });
    });
