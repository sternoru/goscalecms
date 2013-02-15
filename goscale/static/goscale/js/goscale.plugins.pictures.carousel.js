var plugins = plugins || {};

(function($) {
    $.fn.goscalePluginsPicturesCarousel = function() {
		if(navigator.appName == 'Microsoft Internet Explorer') {
			$('body').addClass('ie');
		}
		var $picturesContainer = $(this),
			autoplay = $picturesContainer.data('autoplay') == 'True' ? true : false;
			
		// set useful variables
		var carouselItems, carouselFirst, carouselLast, carouselCur;
		var speed = 150;
		var browserAppName;
		browserAppName = navigator.appName;
		carouselItems = $('#carousel-images img');
		carouselFirst = 0;
		carouselLast = 4;
		
		// add listeners
		$('#arrowLeft').bind('click', scrollRight);
		$('#arrowRight').bind('click', scrollLeft);
		$('#carousel').bind('mousewheel', mouseWheelMoved);
		$('.Image2').live('click', openWebsite);
		
		for(i = 0, ln = carouselItems.length; i < ln; i++) {
			if(i > 4) break;
			$('#carousel').append(['<div class="Image Image', i, '" id="image', i, '"><img src="', $(carouselItems[i]).attr('src'), '" alt="" /></div>'].join(''));
		}
		showTitle();
		
		function mouseWheelMoved(event, delta) {
			if (browserAppName == 'Opera') delta=-delta;
			if(delta > 0) scrollRight();
			else scrollLeft();
			return false;
		}

		function scrollLeft() {
			s = speed;
			if(carouselFirst == carouselItems.length-1) carouselFirst = 0;
			else carouselFirst++;
			if(carouselLast == carouselItems.length-1) carouselLast = 0;
			else carouselLast++;	
			$('.Image0').css('z-index', '0').fadeOut(s, removeItself);
			$('.Image1').animate({width:'90px', top:'60px', left:'10px', maxHeight: '68px'}, s).removeClass('Image1').addClass('Image0');
			$('.Image2').animate({width:'150px', top:'25px', left:'30px', maxHeight: '113px'}, s).removeClass('Image2').addClass('Image1');
			$('.Image3').animate({width:'190px', top:'0', left:'90px', maxHeight: '143px'}, s).removeClass('Image3').addClass('Image2');
			$('.Image4').animate({width:'150px', top:'25px', left:'190px', maxHeight: '113px'}, s).removeClass('Image4').addClass('Image3');
			$('#carousel').append(['<div class="Image Image4" id="image', carouselLast, '"><img src="', $(carouselItems[carouselLast]).attr('src'), '" alt="" /></div>'].join(''));
			showTitle();
		}

		function scrollRight() {
			s = speed;
			if(carouselFirst == 0) carouselFirst = carouselItems.length-1;
			else carouselFirst--;
			if(carouselLast == 0) carouselLast = carouselItems.length-1;
			else carouselLast--;	
			$('.Image4').css('z-index', '0').fadeOut(s, removeItself);
			$('.Image3').animate({width:'90px', top:'60px', left:'275px', maxHeight: '68px'}, s).removeClass('Image3').addClass('Image4');
			$('.Image2').animate({width:'150px', top:'25px', left:'190px', maxHeight: '113px'}, s).removeClass('Image2').addClass('Image3');
			$('.Image1').animate({width:'190px', top:'0', left:'90px', maxHeight: '143px'}, s).removeClass('Image1').addClass('Image2');
			$('.Image0').animate({width:'150px', top:'25px', left:'30px', maxHeight: '113px'}, s).removeClass('Image0').addClass('Image1');
			$('#carousel').append(['<div class="Image Image0" id="image', carouselFirst, '"><img src="', $(carouselItems[carouselFirst]).attr('src'), '" alt="" /></div>'].join(''));
			showTitle();
		}

		function removeItself() {
			$(this).remove();
		}

		function showTitle() {
			carouselCur = parseInt($('.Image2')[0].id.replace('image', ''));
			$('#carousel-image-link').html(['<a href="', $(carouselItems[carouselCur]).data('link'), '">', $(carouselItems[carouselCur]).data('imageTitle'), '</a>'].join(''));
			$('#imageTitle').html($(carouselItems[carouselCur]).data('title'));
			$('#carousel-image-link a').fancybox();
		}

		function openWebsite() {
			$('#carousel-image-link a').click();
		}
	};
	
	plugins.goscalePluginsPicturesCarousel = function() {
		if($('.goscale-plugins-pictures.carousel').length > 0) {
			$('.goscale-plugins-pictures.carousel').goscalePluginsPicturesCarousel();
		}
	}
	
	$(function() {
		plugins.goscalePluginsPicturesCarousel();
	});
})(jQuery);