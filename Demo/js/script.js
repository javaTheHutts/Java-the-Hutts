/*
Author(s): Nicolai van Niekerk, Justin van Tonder
*/

/* global $ */
$(document).ready(function() {
  
  // Initialise all modals
  $('.modal').modal();

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
    $('.pipeline').slick('slickGoTo', 0);
    $('.pipelet').slick('slickGoTo', 0);
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
    endingTop: '22%',
    ready: function(modal, trigger) {
      console.log($('#result').data('percentage'));
      // Results circliful
      $('#result-total').circliful({
        percent: $('#result-total').data('percentage'),
        text: 'Total',
        textBelow: true,
        decimals: 2,
        alwaysDecimals: true,
        foregroundColor: '#80cbc4',
        backgroundColor: 'none',
        fillColor: '#eee',
        foregroundBorderWidth: 4,
        iconColor: '#80cbc4',
        icon: 'f2c3',
        iconSize: '30',
        iconPosition: 'middle'
      });
      
      $('#result-text').circliful({
        percent: $('#result-text').data('percentage'),
        text: 'Text',
        textBelow: true,
        decimals: 2,
        alwaysDecimals: true,
        foregroundColor: '#80cbc4',
        backgroundColor: 'none',
        fillColor: '#eee',
        foregroundBorderWidth: 4,
        iconColor: '#80cbc4',
        icon: 'f022',
        iconSize: '30',
        iconPosition: 'middle'
      });
      
      $('#result-profile').circliful({
        percent: $('#result-profile').data('percentage'),
        text: 'Profile',
        textBelow: true,
        decimals: 2,
        alwaysDecimals: true,
        foregroundColor: '#80cbc4',
        backgroundColor: 'none',
        fillColor: '#eee',
        foregroundBorderWidth: 4,
        iconColor: '#80cbc4',
        icon: 'f007',
        iconSize: '30',
        iconPosition: 'middle'
      });
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
    
    // Move up once working
    $('#result-total').html('');
    $('#result-total').data('percentage', 86.55);
    $('#result-text').html('');
    $('#result-text').data('percentage', 84);
    $('#result-profile').html('');
    $('#result-profile').data('percentage', 88.99);
    $('#compare-result').modal('open');
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
    responsive: [{
      breakpoint: 600,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 2
      }
    }]
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
