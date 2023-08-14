const labelItems = document.querySelectorAll('.label-item');  // Get all label items
  
 // Add event listener for each label item
 labelItems.forEach(label => {
   label.addEventListener('click', () => {
     // Toggle the "selected" class on click
     label.classList.toggle('selected');
   });
 });

 $(function() {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	$(".toggle-password").click(function() {

	  $(this).toggleClass("fa-eye fa-eye-slash");
	  var input = $($(this).attr("toggle"));
	  if (input.attr("type") == "password") {
	    input.attr("type", "text");
	  } else {
	    input.attr("type", "password");
	  }
	});

});

// function to toggle the mobile drawer on click of the humburger button
// document.addEventListener("DOMContentLoaded", function() {
// 	const mobileMenuIcon = document.querySelector(".mobile-menu-icon");
// 	const mobileNavPanel = document.querySelector(".mobile-nav-panel");
// 	// const overlay = document.querySelector(".overlay");

// 	mobileMenuIcon.addEventListener("click", function() {
// 		mobileNavPanel.classList.toggle("show");
// 		mobileMenuIcon.classList.toggle("open"); // Toggle the "open" class
// 	});

// 	// overlay.addEventListener("click", function() {
// 	// 	mobileNavPanel.classList.remove("show");
// 	// 	mobileMenuIcon.classList.remove("open"); // Remove the "open" class
// 	// });
// });


