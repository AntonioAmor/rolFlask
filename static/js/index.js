$(document).ready(function() {
        $(".joinButton").click(function() {

            var game_id = $(this).attr("value");
            var val = $("#joinId").attr("value")
            if ( val == game_id || val ==null){
              $("#joinDiv").toggle();
            }else{
              $("joinDiv").show();
            }

            var desc= $(this).closest("div").attr("title");
            $("#joinId").attr("value", game_id);
            $("#joinDesc").text(desc)
        });
    });

$(document).ready(function() {
        $("#createGames").click(function() {

            $("#createDiv").toggle()
        });
    });
