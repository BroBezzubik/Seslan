$(document).ready(function(){
    $('#left-side-bar-collapse').on('click', function(){
        $('#left-side-bar').toggleClass('active');
        $('#left-side-bar-collapse').toggleClass('active')
        
        
    })

    $('#right-side-bar-collapse').on('click', function(){
        $('#right-side-bar').toggleClass('active');
        $('#right-side-bar-collapse').toggleClass('active');
    })
})