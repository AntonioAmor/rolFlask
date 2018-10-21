$(document).ready(function() {
        $(".joinButton").click(function() {

            var game_id = $(this).attr("value");
            if (game_id == $("#joinId").attr("placeholder")){
              $("#joinDiv").toggle();
            }else{
              $("joinDiv").show();
            }

            var desc= $(this).closest("div").attr("title");
            $("#joinId").attr("placeholder", game_id);
            $("#joinDesc").text(desc)
        });
    });

$(document).ready(function() {
        $("#createGames").click(function() {

            $("#createDiv").toggle()
        });
    });
