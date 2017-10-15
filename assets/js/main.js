$(document).ready(function() {
  /* ======= Fixed header when scrolled ======= */
  $(window).bind('scroll', function() {
    if ($(window).scrollTop() > 60) {
      $('#header').addClass('header-scrolled');
    } else {
      $('#header').removeClass('header-scrolled');
    }
  });
  
  /* ======= Scrollspy ======= */
  $('body').scrollspy({ target: '#header', offset: 100});
  
  /* ======= ScrollTo ======= */
  $('a.scrollto').on('click', function(e){
    //store hash
    var target = this.hash;
    e.preventDefault();
		$('body').scrollTo(target, 800, {offset: -50, 'axis':'y'});
    //Collapse mobile menu after clicking
		if ($('.navbar-collapse').hasClass('in')){
			$('.navbar-collapse').removeClass('in').addClass('collapse');
		}
  });
  
  /* ===== Hero section sizing ===== */
  function setHeroSize() {
    $('.hero-section').css({
      'min-height': $(window).innerHeight()
    });
  }
  setHeroSize();
  $(window).resize(function() {
      setHeroSize();
  });

  $('.left.carousel-control').hide();
  $('.carousel-control').on('click', function() {
    if ($('.carousel-inner .active h3').text() == 'Extraction') {
      $('.right.carousel-control').hide();
      $('.left.carousel-control').show();
    } else {
      $('.left.carousel-control').hide();
      $('.right.carousel-control').show();
    }
  });

  $('.service').on('click', function() {
    if (!$(this).hasClass('service-selected')) {
      $('.service-selected').removeClass('service-selected');
      $(this).addClass('service-selected');
    }
  });
});