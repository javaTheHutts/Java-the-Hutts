/*
Author(s): Nicolai van Niekerk, Justin van Tonder
*/

/* global $ */
$(document).ready(function() {
  
  // Initialise all modals
  $('div.modal').modal();

  // Materialise component initialization
  $('select').material_select();
  $('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 200 // Creates a dropdown of 200 years to control year
  });

  // Change caret symbol when expanding collapsibles
  $('.collapsible-header').on('click', function() {
    $(this).hasClass('active')?
    $(this).children('.carets').text('expand_more'):
    $(this).children('.carets').text('chevron_right');
    // Trigger slick carousel events to re-init sizes
    $('.pipeline').slick('slickNext');
    $('.pipelet').slick('slickNext');
    $('.pipeline').slick('slickPrev');
    $('.pipelet').slick('slickPrev');
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
      // Stuff here
    }
  });
  
  // Modal trigger
  $('#compareBtn').on('click', function(e) {
    e.preventDefault();
    var formData = new FormData();
    var idPhoto = document.getElementById('idPhoto').files[0];
    var userImage = document.getElementById('userImage').files[0];
    var names = $('#names').val();
    var surname = $('#surname').val();
    var idNumber = $('#idNumber').val();
    var nationality = $('#nationality').val();
    var cob = $('#cob').val();
    var status = $('#status').val();
    var gender = $('#gender').val();
    var dob = $('#dob').val();

    formData.append('idPhoto', idPhoto);
    formData.append('userImage', userImage);
    formData.append('names', names);
    formData.append('surname', surname);
    formData.append('idNumber', idNumber);
    formData.append('nationality', nationality);
    formData.append('cob', cob);
    formData.append('status', status);
    formData.append('gender', gender);
    formData.append('dob', dob);

    $.ajax({
        type: "POST",
        url: "http://localhost:5000/verifyID",
        data: formData,
        processData: false,
        contentType: false,
        success: function(data){
            alert("Match: " + data.PercentageMatch + "%");
        }
    });
  });
  
  // Image sliders initialisation
  $('.pipelet').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: false,
    fade: true,
    asNavFor: '.pipeline'
  });
  
  $('.pipeline').slick({
    slidesToShow: 3,
    slidesToScroll: 1,
    asNavFor: '.pipelet',
    centerMode: true,
    focusOnSelect: true,
  });
  
});

// Show ID Image preview
function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $('#idPreview').attr('src', e.target.result);
    };

    reader.readAsDataURL(input.files[0]);
  }
}
