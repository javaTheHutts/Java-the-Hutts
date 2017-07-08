/*
Author(s): Nicolai van Niekerk, Justin van Tonder
*/

/* global $ */
$(document).ready(function() {
  
  // Initialise all modals
  $('div.modal').modal();
  
  // Initialise slider
  $('.slider').slider();

  // Materialise component initialization
  $('select').material_select();
  $('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 200 // Creates a dropdown of 15 years to control year
  });

  // Change caret symbol when expanding collapsibles
  $('.collapsible-header').on('click', function() {
    $(this).hasClass('active')?
    $(this).children('.carets').text('expand_more'):
    $(this).children('.carets').text('chevron_right');
  });
  
  // Click event to scroll to top
	$('.scroll-top').on('click', function() {
		$('html, body').animate({scrollTop: 0}, 800);
		return false;
	});
	
	// Click event to scroll to bottom
	$('.scroll-bottom').on('click', function() {
		$('html, body').animate({scrollTop: $('body').height()}, 800);
		return false;
	});
  
  // Result modal initialisation
  $('#compare-result').modal({
    ready: function(modal, trigger) {
      $('.odometer').html(96);
    }
  });
  
  // Modal trigger
  $('#compareBtn').on('click', function() {
    $('#compare-result').modal('open');
    return false;
  });
  
});

// Show ID Image preview
function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $('#id_image').attr('src', e.target.result);
    };

    reader.readAsDataURL(input.files[0]);
  }
}
