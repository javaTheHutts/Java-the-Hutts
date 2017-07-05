/*
Author(s): Nicolai van Niekerk, Justin van Tonder
*/

/* global $ */
$(document).ready(function() {

  //Materialize component initialization
  $('select').material_select();
  $('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 200 // Creates a dropdown of 15 years to control year
  });

  // Change caret symbol when expanding collapsibles
  $('.collapsible-header').on('click', function() {
    $(this).hasClass('active')?
    $(this).children('.carets').text('►'):
    $(this).children('.carets').text('▼');
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
