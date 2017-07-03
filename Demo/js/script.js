/*
Author(s): Nicolai van Niekerk, Justin van Tonder
*/

/* global $ */
$(document).ready(function() {
  
  // Change caret symbol when expanding collapsibles
  $('.collapsible-header').on('click', function(){
    $(this).hasClass('active')?
    $(this).children('.carets').text('▼'):
    $(this).children('.carets').text('►');
  });
  
});