/*
Author(s): Nicolai van Niekerk, Justin van Tonder
*/

/* global $ */
var PATH_TO_PIPELINE = '/home/justin/Desktop/output/';

$(document).ready(function () {

	// Hide some content
	$('.initially-hidden').hide();

	// Initialize slide menu buttons
	$('.slide-btn').sideNav({
		menuWidth: 300,
		closeOnClick: true
	});

	// Hide existing side navs
	$('.slide-btn').on('click', function () {
		// Not the best fix... but workable
		if ($('#sidenav-overlay').css('opacity') == '1') {
			$('#sidenav-overlay').trigger('click');
		}
	});

	// Initialise all modals
	$('.modal').modal();

	// Materialise component initialization
	$('select').material_select();

	$('.datepicker').pickadate({
		selectMonths: true, // Creates a dropdown to control month
		selectYears: 110, // Creates a dropdown of 15 years to control year,
		format: 'dd/mm/yyyy',
		closeOnSelect: false // Close upon selecting a date,
	});

	// Image pipeline initialisation
	$('.pipeline').slick({
		slidesToShow: 3,
		slidesToScroll: 1,
		centerMode: false,
		infinite: false,
		focusOnSelect: true,
		responsive: [{
			breakpoint: 601,
			settings: {
				slidesToShow: 1,
				slidesToScroll: 1
			}
		}, {
			breakpoint: 993,
			settings: {
				slidesToShow: 2,
				slidesToScroll: 1
			}
		}]
	});

	// Initialise collapsibles
	$('.collapsible').collapsible({
		onOpen: function () {
			// Change caret symbol when expanding collapsibles
			$('.collapsible-header').each(function (el) {
				$(this).hasClass('active') ?
				$(this).children('.carets').text('chevron_right') :
				$(this).children('.carets').text('expand_more');
				// Refresh slick carousels
				$('.pipeline').slick('setPosition');
			});
		},
		onClose: function () {
			// Change caret symbol when expanding collapsibles
			$('.collapsible-header').each(function (el) {
				$(this).hasClass('active') ?
				$(this).children('.carets').text('chevron_right') :
				$(this).children('.carets').text('expand_more');
			});
		}
	});

	// Click event to scroll to top
	$('.scroll-top').on('click', function () {
		$('html, body').animate({ scrollTop: 0 }, 800);
		return false;
	});

	// Click event to scroll to bottom
	$('.scroll-bottom').on('click', function () {
		$('html, body').animate({ scrollTop: $('body').height() }, 800);
		return false;
	});

	// Result modal initialisation
	$('.verify-result').modal({
		endingTop: '20%',
	});

	// Modal trigger
	$('#verify-btn').on('click', function (e) {
		e.preventDefault();
		var formData = new FormData();
		var idPhoto = document.getElementById('id-photo-verify').files[0];
		var userImage = document.getElementById('profile-photo').files[0];
		var names = $('#names-verify').val();
		var surname = $('#surname-verify').val();
		var idNumber = $('#identity_number-verify').val();
		var nationality = $('#nationality-verify').val();
		var cob = $('#country_of_birth-verify').val();
		var status = $('#status-verify').val();
		var gender = $('#sex-verify').val();
		var dob = $('#date_of_birth-verify').val();

		formData.append('id_img', idPhoto);
		formData.append('face_img', userImage);
		formData.append('names', names);
		formData.append('surname', surname);
		formData.append('idNumber', idNumber);
		formData.append('nationality', nationality);
		formData.append('cob', cob);
		formData.append('status', status);
		formData.append('gender', gender);
		formData.append('dob', dob);

		// Ensure that the pre-loader spinner is visible
		$('.circle-result').html('');
		$('#verify-result .modal-content .spinner').show();

		$.ajax({
			type: "POST",
			url: "http://localhost:5000/verifyID",
			data: formData,
			processData: false,
			contentType: false,
			success: function (data) {
				$('.result-total').data('percentage', data.total_match);
				$('.result-text').data('percentage', data.text_match);
				$('.result-profile').data('percentage', data.face_match);

				// Results circliful
				$('.result-total').circliful({
					percent: $('.result-total').data('percentage'),
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

				$('.result-text').circliful({
					percent: $('.result-text').data('percentage'),
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

				$('.result-profile').circliful({
					percent: $('.result-profile').data('percentage'),
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

				$('#verify-result .modal-content .spinner').hide();
				$('.circle-results-wrapper, #verify-result.modal .modal-footer')
				.show(500);

				// Populate and unhide pipeline
				populatePipeline(true, 8);
				populatePipeline(false, 6);
				$('#text-pipeline').show(600);
				$('#profile-pipeline').show(600);
			}
		});

		// Testing -- Remove
		$('.test-circle').circliful({
			percent: 88.8,
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

		// Open up result modal
		$('#verify-result.modal .modal-footer').hide();
		$('#verify-result').modal('open');
	});

	// View detailed results click
	$('#verify-result.modal .modal-footer').on('click', function () {
		$('.collapsible-main').collapsible('close', 1);
		$('.collapsible-main').collapsible('open', 4);
		$('body').scrollTo($('#detailed-results > .collapsiblebody'), 1000);
	});

	// Hover compare cards on compare button hover
	$('#verify-btn, .extraction-options button').hover(function () {
		$('.duo-card').addClass('duo-card-hover');
	}, function () {
		$('.duo-card').removeClass('duo-card-hover');
	});

	// Extract text
	$('#extract-text-btn').on('click', function (e) {
		e.preventDefault();

		// Display a pre-loader while waiting
		$('.loader-overlay .spinner').css({
			position:'absolute',
			left: ($(window).width() - $(this).outerWidth()) / 2,
			top: ($(window).height() - $(this).outerHeight()) / 2
		});
		$('.loader-overlay').show(600);

		var formData = new FormData();
		var blurTechnique = $('#blur_technique').val();
		var thresholdTechnique = $('#threshold_technique').val();
		var profileSwitch = $('#profile_switch').is(':checked');
		var barcodeSwitch = $('#barcode_switch').is(':checked');
		var extractRed = $('#extract_red').is(':checked');
		var extractGreen = $('#extract_green').is(':checked');
		var extractBlue = $('#extract_blue').is(':checked');
		var idPhoto = document.getElementById('id-photo-extract').files[0];

		formData.append('idPhoto', idPhoto);

		// Send preferences if auto settings is off
		if (!$('#auto_settings').is(':checked')) {
			formData.append('blur_technique', blurTechnique);
			formData.append('threshold_technique', thresholdTechnique);
			formData.append('remove_face', profileSwitch);
			formData.append('remove_barcode', barcodeSwitch);

			if (extractBlue)
				formData.append('color', "blue");
			else if (extractGreen)
				formData.append('color', "green");
			else if (extractRed)
				formData.append('color', "red");
		}

		$.ajax({
			type: "POST",
			url: "http://localhost:5000/extractText",
			data: formData,
			processData: false,
			contentType: false,
			success: function (data) {
				// Hide pre-loader
				$('.loader-overlay').hide(600);

				// Handle the case involving a UP card, if a UP card
				// was used as an input image
				if (data['up_card']) {
					handleUPCard(data);
					return;
				}

				$("input[id$=extract]").each(function () {
					var id = $(this).attr("id").replace("-extract", "");
					if (id != "id-photo") {
						$(this).focus();
						$(this).val(data[id]);
						$(this).blur();
					}
				});
				// Populate and unhide pipeline
				populatePipeline(true, 8);
				$('#text-pipeline').show(600);
			},
			error: function() {
				// Hide pre-loader
				$('.loader-overlay').hide(600);
			}
		});
	});

	// Extract profile
	$('#extract-photo-btn').on('click', function (e) {
		// Display a pre-loader while waiting
		$('.loader-overlay .spinner').css({
			position:'absolute',
			left: ($(window).width() - $(this).outerWidth()) / 2,
			top: ($(window).height() - $(this).outerHeight()) / 2
		});
		$('.loader-overlay').show(600);

		var formData = new FormData();
		var idPhoto = document.getElementById('id-photo-extract').files[0];
		formData.append('idPhoto', idPhoto);

		$.ajax({
			type: "POST",
			url: "http://localhost:5000/extractFace",
			data: formData,
			processData: false,
			contentType: false,
			success: function (data) {
				// Hide pre-loader
				$('.loader-overlay').hide(600);

				var face = jQuery.parseJSON(data)
				document.getElementById("face-preview-extract").src = face.extracted_face;
				// Populate and unhide pipeline
				populatePipeline(false, 6);
				$('#profile-pipeline').show(600);
			},
			error: function() {
				// Hide pre-loader
				$('.loader-overlay').hide(600);
			}
		});
	});

	// Extract all
	$('#extract-all-btn').on('click', function (e) {
		// Display a pre-loader while waiting
		$('.loader-overlay .spinner').css({
			position:'absolute',
			left: ($(window).width() - $(this).outerWidth()) / 2,
			top: ($(window).height() - $(this).outerHeight()) / 2
		});
		$('.loader-overlay').show(600);

		var formData = new FormData();
		var idPhoto = document.getElementById('id-photo-extract').files[0];
		formData.append('idPhoto', idPhoto);

		$.ajax({
			type: "POST",
			url: "http://localhost:5000/extractAll",
			data: formData,
			processData: false,
			contentType: false,
			success: function (data) {
				// Hide pre-loader
				$('.loader-overlay').hide(600);

				// Handle the case involving a UP card, if a UP card
				// was used as an input image
				if (data['up_card']) {
					handleUPCard(data);
					return;
				}

				// Populate text fields
				var cardComponents = jQuery.parseJSON(data);
				$("input[id$=extract]").each(function () {
					var id = $(this).attr("id").replace("-extract", "");
					if (id != "id-photo") {
						$(this).focus();
						$(this).val(cardComponents.text_extract_result[id]);
						$(this).blur();
					}
				});

				// Show face
				document.getElementById("face-preview-extract").src = cardComponents.extracted_face;

				// Populate and unhide pipeline
				populatePipeline(true, 8);
				populatePipeline(false, 6);
				$('#text-pipeline').show(600);
				$('#profile-pipeline').show(600);
			},
			error: function() {
				// Hide pre-loader
				$('.loader-overlay').hide(600);
			}
		});
	});

	// Make sure you can only extract one channel
	$(".channel_extractors").change(function () {
		var currentID = $(this).attr('id');
		$(".channel_extractors").each(function (index) {
			if ($(this).attr('id') != currentID)
				$(this).prop('checked', false);
		});
	});

	// Enable and Disable Auto Settings
	$('#auto_settings').change(function () {
		if ($(this).is(':checked')) {
			$('.text-switch').prop('checked', false);
			$('.text-extract-settings').prop('disabled', true);
		}
		else
			$('.text-extract-settings').prop('disabled', false);
		$('select').material_select();
	});
});

// Show ID Image preview
function readURL(input) {
	if (input.files && input.files[0]) {
		var reader = new FileReader();
		reader.onload = function (e) {
			$('#id-preview-verify').attr('src', e.target.result);
			$('#id-preview-extract').attr('src', e.target.result);
		};
		reader.readAsDataURL(input.files[0]);
	}
}

// Populate slides for pipeline carousel
function populatePipeline(isTextPipeline, numImages) {
	var attachTo = isTextPipeline ? $('#text-pipe') : $('#profile-pipe');
	var imagePrepend = isTextPipeline ? '' : 'f';
	// Clear existing pipeline slides
	attachTo.slick('removeSlide', null, null, true);
	for (var i = 1; i <= numImages; i++) {
		// Get file path
		var imagePath = PATH_TO_PIPELINE + imagePrepend + i + '.png';
		// Determine if image exists
		imageExists(imagePath, false, function (image) {
			var nonCachedImage = image + '?t=' + new Date().getTime();
			// Create anchor
			var anchor = $('<a>', {
				'href': nonCachedImage,
				'data-lightbox': isTextPipeline ? 'text-pipelet' : 'profile-pipelet'
			});
			// Attach to the anchor
			$('<div>', {
				'class': 'pipe-slide',
				'style': 'background-image: url(' + nonCachedImage + ');'
			}).appendTo(anchor);
			// Finally, add the anchor as a slide to slick carousel
			attachTo.slick('slickAdd', anchor)
		});
	}
}

// Check if a given file exists
function imageExists(image, remote, callback) {
	if (!remote) {
		var img = new Image();
		img.src = image;
		img.onload = function () {
			// Image exists, therefore, proceed
			callback(image);
		}
	} else {
		var url = 'http://localhost:5000' + image;
		$.ajax({
			url: '',
			type: 'HEAD',
			success: function () {
				// Image exists, therefore, proceed
				callback(file);
			}
		});
	}
}

// Handle the extracted information from a UP card
function handleUPCard(data) {
	// The regex used to find the student/staff number
	// used mostly to sift through the garbage and find 
	// what we actually want
	var re = /[0-9]{6,10}/
	// Split text_dump on newline
	var textDump = data['text_dump'].split('\n');
	// Sift through the noise
	for (var i = 0; i < textDump.length; i++) {
		if (re.test(textDump[i])) {
			// Get student/staff number
			var upNumber = data['barcode_dump']? data['barcode_dump']: textDump[i];
			$('#identity_number-extract').focus();
			$('#identity_number-extract').val(upNumber);
			$('#identity_number-extract').blur();
			// Get initials and surname if possible
			if (i - 1 > 0) {
				var nameLine = textDump[i - 1].split(' ');
				nameLine.shift();
				$('#names-extract').focus();
				$('#names-extract').val(nameLine[0]);
				$('#names-extract').blur();
				nameLine.shift();
				nameLine = nameLine.join(' ');
				$('#surname-extract').focus();
				$('#surname-extract').val(nameLine);
				$('#surname-extract').blur();
			}
		}
	}

	// $('#identity_number-extract').text(text_dump[]);
}
