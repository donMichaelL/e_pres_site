var $grid = $('.grid').imagesLoaded( function() {
  // init Masonry after all images have loaded
  $grid.masonry({
    itemSelector: '.grid-item',
    gutter: 10,
  });
});

$(".alert-success").fadeTo(2000, 500).slideUp(500, function(){
    $(".alert-success").alert('close');
});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function notification_message(message) {
    $("body").append("<div class='alert alert-success text-center alert-dismissible container-alert-flash '> \
    <button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button> \
    	<p class='lead' style='font-size:14px;'><strong>"+ message +"</strong></p> \
    </div>\
    ");

    $(".alert-success").fadeTo(2000, 500).slideUp(500, function(){
        $(".alert-success").alert('close');
    });

}

$(document).ready(function(){
  $('.lang').click(function(event){
    var language = event.target.id;
    $.ajax({
      type: "POST",
      url: '/language-selector/',
      data: {
        language: language,
        csrfmiddlewaretoken:  getCookie('csrftoken')
      },
    success: function(){
      console.log('ok');
      }
    });
    location.reload();

  });
});
