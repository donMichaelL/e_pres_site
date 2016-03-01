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
