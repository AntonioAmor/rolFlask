$('.toggle').click(function(){
    $('.formulario').animate({
        height: "toggle",
        'padding-top': 'toggle',
        'padding-bottom': 'toggle',
        opacity: 'toggle'
    }, "slow");

    let text = $(".logButt").text() == "Log in" ? "Crear Cuenta": "Log in"
    $(".logButt").text(text);
});
