(function($) {
    $.fn.goscalePluginsPictures = function() {
		var $picturesContainer = $(this),
			autoplay = $picturesContainer.data('autoplay') == 'True' ? true : false;
		
		switch($picturesContainer.data('type')) {
			case 'grid':
				var $container 	= $picturesContainer.find('.am-container'),
					$imgs		= $container.find('img').hide(),
					totalImgs	= $imgs.length,
					cnt			= 0;
				
				$imgs.each(function(i) {
					var $img	= $(this);
					$('<img/>').load(function() {
						++cnt;
						if( cnt === totalImgs ) {
							$container.removeClass('loading');
							$imgs.show();
							$container.montage({
								liquid : true,
								margin : 2,
								minw: 90,
								fillLastRow : false,
								alternateHeight	: true,
								alternateHeightRange : {
									min	: 90,
									max	: 288
								}
							});
						}
					}).attr('src',$img.attr('src'));
				});	
				
				$picturesContainer.find("a[rel^='prettyPhoto']").prettyPhoto({
					show_title: false, /* true/false */
					default_width: 500,
					default_height: 344,
					counter_separator_label: '/', /* The separator for the gallery counter 1 "of" 2 */
					theme: 'dark_rounded', /* light_rounded / dark_rounded / light_square / dark_square / facebook */
					horizontal_padding: 20, /* The padding on each side of the picture */
					deeplinking: true, /* Allow prettyPhoto to update the url to enable deeplinking. */
					overlay_gallery: true, /* If set to true, a gallery will overlay the fullscreen image on mouse over */
					keyboard_shortcuts: true, /* Set to false if you open forms inside prettyPhoto */
					changepicturecallback: function(){}, /* Called everytime an item is shown/changed */
					callback: function(){}, /* Called when prettyPhoto is closed */
					ie6_fallback: true,
					social_tools: false
				});
			break;
			case 'slideshow':
				if($picturesContainer.data('width')) {
					$picturesContainer.find(".slides_container").css('width', $picturesContainer.data('width'));
					$picturesContainer.find(".slides_container img").css('width', $picturesContainer.data('width') - 22);
				}
				if($picturesContainer.data('height')) {
					$picturesContainer.find(".slides_container").css('height', $picturesContainer.data('height'));
					$picturesContainer.find(".slides_container img").css('height', $picturesContainer.data('height') - 22);
				}
				$picturesContainer.find(".slides").slides({
					preload: true,
					preloadImage: $picturesContainer.find('.loader img').attr('src'),
					play: autoplay ? 4000 : 0,
					hoverPause: true
				});
			break;
			case 'thumbnails':
				var $gallery = $picturesContainer.find('.gallery');
				$gallery.galleryView({
					panel_width: $picturesContainer.data('width') ? $picturesContainer.data('width') : undefined,
					panel_height: $picturesContainer.data('height') ? $picturesContainer.data('height') : undefined,
					frame_width: $picturesContainer.data('thumbnailWidth') ? $picturesContainer.data('thumbnailWidth') : undefined,
					frame_height: $picturesContainer.data('thumbnailHeight') ? $picturesContainer.data('thumbnailHeight') : undefined,
					autoplay: autoplay
				});
			break;
			case 'mini':
				if($picturesContainer.data('width')) {
					$('#msg_slideshow').css('width', $picturesContainer.data('width'));
					$('#msg_wrapper').css('width', $picturesContainer.data('width'));
				}
				if($picturesContainer.data('height')) {
					$('#msg_slideshow').css('height', $picturesContainer.data('height'));
					$('#msg_wrapper').css('height', $picturesContainer.data('height'));
				}
				
				$(function() {
					/**
					* interval : time between the display of images
					* playtime : the timeout for the setInterval function
					* current  : number to control the current image
					* current_thumb : the index of the current thumbs wrapper
					* nmb_thumb_wrappers : total number	of thumbs wrappers
					* nmb_images_wrapper : the number of images inside of each wrapper
					*/
					var interval			= 4000;
					var playtime;
					var current 			= 0;
					var current_thumb 		= 0;
					var nmb_thumb_wrappers	= $('#msg_thumbs .msg_thumb_wrapper').length;
					var nmb_images_wrapper  = 6;
					/**
					* start the slideshow
					*/
					
					play();
					
					if(!autoplay) {
						pause();
					}
					
					/**
					* show the controls when 
					* mouseover the main container
					*/
					slideshowMouseEvent();
					function slideshowMouseEvent(){
						$('#msg_slideshow').unbind('mouseenter')
										   .bind('mouseenter',showControls)
										   .andSelf()
										   .unbind('mouseleave')
										   .bind('mouseleave',hideControls);
						}
					
					/**
					* clicking the grid icon,
					* shows the thumbs view, pauses the slideshow, and hides the controls
					*/
					$('#msg_grid').bind('click',function(e){
						hideControls();
						$('#msg_slideshow').unbind('mouseenter').unbind('mouseleave');
						pause();
						$('#msg_thumbs').stop().animate({'top':'0px'},500);
						e.preventDefault();
					});
					
					/**
					* closing the thumbs view,
					* shows the controls
					*/
					$('#msg_thumb_close').bind('click',function(e){
						showControls();
						slideshowMouseEvent();
						$('#msg_thumbs').stop().animate({'top':'-230px'},500);
						e.preventDefault();
					});
					
					/**
					* pause or play icons
					*/
					$('#msg_pause_play').bind('click',function(e){
						var $this = $(this);
						if($this.hasClass('msg_play'))
							play();
						else
							pause();
						e.preventDefault();	
					});
					
					/**
					* click controls next or prev,
					* pauses the slideshow, 
					* and displays the next or prevoius image
					*/
					$('#msg_next').bind('click',function(e){
						pause();
						next();
						e.preventDefault();
					});
					$('#msg_prev').bind('click',function(e){
						pause();
						prev();
						e.preventDefault();
					});
					
					/**
					* show and hide controls functions
					*/
					function showControls(){
						$('#msg_controls').stop().animate({'right':'15px'},500);
					}
					function hideControls(){
						$('#msg_controls').stop().animate({'right':'-110px'},500);
					}
					
					/**
					* start the slideshow
					*/
					function play(){
						next();
						$('#msg_pause_play').addClass('msg_pause').removeClass('msg_play');
						playtime = setInterval(next,interval)
					}
					
					/**
					* stops the slideshow
					*/
					function pause(){
						$('#msg_pause_play').addClass('msg_play').removeClass('msg_pause');
						clearTimeout(playtime);
					}
					
					/**
					* show the next image
					*/
					function next(){
						++current;
						showImage('r');
					}
					
					/**
					* shows the previous image
					*/
					function prev(){
						--current;
						showImage('l');
					}
					
					/**
					* shows an image
					* dir : right or left
					*/
					function showImage(dir){
						/**
						* the thumbs wrapper being shown, is always 
						* the one containing the current image
						*/
						alternateThumbs();
						
						/**
						* the thumb that will be displayed in full mode
						*/
						var $thumb = $('#msg_thumbs .msg_thumb_wrapper:nth-child('+current_thumb+')')
									.find('a:nth-child('+ parseInt(current - nmb_images_wrapper*(current_thumb -1)) +')')
									.find('img');
						if($thumb.length){
							var source = $thumb.attr('alt');
							var $currentImage = $('#msg_wrapper').find('img');
							if($currentImage.length){
								$currentImage.fadeOut(function(){
									$(this).remove();
									$('<img />').load(function(){
										var $image = $(this);
										resize($image);
										$image.hide();
										$('#msg_wrapper').empty().append($image.fadeIn());
									}).attr('src',source);
								});
							}
							else{
								$('<img />').load(function(){
										var $image = $(this);
										resize($image);
										$image.hide();
										$('#msg_wrapper').empty().append($image.fadeIn());
								}).attr('src',source);
							}
									
						}
						else{ //this is actually not necessary since we have a circular slideshow
							if(dir == 'r')
								--current;
							else if(dir == 'l')
								++current;	
							alternateThumbs();
							return;
						}
					}
					
					/**
					* the thumbs wrapper being shown, is always 
					* the one containing the current image
					*/
					function alternateThumbs(){
						$('#msg_thumbs').find('.msg_thumb_wrapper:nth-child('+current_thumb+')')
										.hide();
						current_thumb = Math.ceil(current/nmb_images_wrapper);
						/**
						* if we reach the end, start from the beggining
						*/
						if(current_thumb > nmb_thumb_wrappers){
							current_thumb 	= 1;
							current 		= 1;
						}	
						/**
						* if we are at the beggining, go to the end
						*/					
						else if(current_thumb == 0){
							current_thumb 	= nmb_thumb_wrappers;
							current 		= current_thumb*nmb_images_wrapper;
						}
						
						$('#msg_thumbs').find('.msg_thumb_wrapper:nth-child('+current_thumb+')')
										.show();	
					}
					
					/**
					* click next or previous on the thumbs wrapper
					*/
					$('#msg_thumb_next').bind('click',function(e){
						next_thumb();
						e.preventDefault();
					});
					$('#msg_thumb_prev').bind('click',function(e){
						prev_thumb();
						e.preventDefault();
					});
					function next_thumb(){
						var $next_wrapper = $('#msg_thumbs').find('.msg_thumb_wrapper:nth-child('+parseInt(current_thumb+1)+')');
						if($next_wrapper.length){
							$('#msg_thumbs').find('.msg_thumb_wrapper:nth-child('+current_thumb+')')
											.fadeOut(function(){
												++current_thumb;
												$next_wrapper.fadeIn();									
											});
						}
					}
					function prev_thumb(){
						var $prev_wrapper = $('#msg_thumbs').find('.msg_thumb_wrapper:nth-child('+parseInt(current_thumb-1)+')');
						if($prev_wrapper.length){
							$('#msg_thumbs').find('.msg_thumb_wrapper:nth-child('+current_thumb+')')
											.fadeOut(function(){
												--current_thumb;
												$prev_wrapper.fadeIn();									
											});
						}				
					}
					
					/**
					* clicking on a thumb, displays the image (alt attribute of the thumb)
					*/
					$('#msg_thumbs .msg_thumb_wrapper > a').bind('click',function(e){
						var $this 		= $(this);
						$('#msg_thumb_close').trigger('click');
						var idx			= $this.index();
						var p_idx		= $this.parent().index();
						current			= parseInt(p_idx*nmb_images_wrapper + idx + 1);
						showImage();
						e.preventDefault();
					}).bind('mouseenter',function(){
						var $this 		= $(this);
						$this.stop().animate({'opacity':1});
					}).bind('mouseleave',function(){
						var $this 		= $(this);	
						$this.stop().animate({'opacity':0.5});
					});
					
					/**
					* resize the image to fit in the container (400 x 400)
					*/
					function resize($image){
						var theImage 	= new Image();
						theImage.src 	= $image.attr("src");
						var imgwidth 	= theImage.width;
						var imgheight 	= theImage.height;
						
						var containerwidth  = 180;
						var containerheight = 180;
					
						if(imgwidth	> containerwidth){
							var newwidth = containerwidth;
							var ratio = imgwidth / containerwidth;
							var newheight = imgheight / ratio;
							if(newheight > containerheight){
								var newnewheight = containerheight;
								var newratio = newheight/containerheight;
								var newnewwidth =newwidth/newratio;
								theImage.width = newnewwidth;
								theImage.height= newnewheight;
							}
							else{
								theImage.width = newwidth;
								theImage.height= newheight;
							}
						}
						else if(imgheight > containerheight){
							var newheight = containerheight;
							var ratio = imgheight / containerheight;
							var newwidth = imgwidth / ratio;
							if(newwidth > containerwidth){
								var newnewwidth = containerwidth;
								var newratio = newwidth/containerwidth;
								var newnewheight =newheight/newratio;
								theImage.height = newnewheight;
								theImage.width= newnewwidth;
							}
							else{
								theImage.width = newwidth;
								theImage.height= newheight;
							}
						}
						$image.css({
							'width'	:theImage.width,
							'height':theImage.height
						});
					}
				});
			break;
			case 'carousel':
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
					$('#carousel').append(['<img class="Image Image', i, '" id="image', i, '" src="', $(carouselItems[i]).attr('src'), '" alt="" />'].join(''));
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
					$('.Image1').animate({width:'90px', top:'60px', left:'10px'}, s).removeClass('Image1').addClass('Image0');
					$('.Image2').animate({width:'150px', top:'25px', left:'30px'}, s).removeClass('Image2').addClass('Image1');
					$('.Image3').animate({width:'190px', top:'0', left:'90px'}, s).removeClass('Image3').addClass('Image2');
					$('.Image4').animate({width:'150px', top:'25px', left:'190px'}, s).removeClass('Image4').addClass('Image3');
					$('#carousel').append(['<img class="Image Image4" id="image', carouselLast, '" src="', $(carouselItems[carouselLast]).attr('src'), '" alt="" />'].join(''));
					showTitle();
				}

				function scrollRight() {
					s = speed;
					if(carouselFirst == 0) carouselFirst = carouselItems.length-1;
					else carouselFirst--;
					if(carouselLast == 0) carouselLast = carouselItems.length-1;
					else carouselLast--;	
					$('.Image4').css('z-index', '0').fadeOut(s, removeItself);
					$('.Image3').animate({width:'90px', top:'60px', left:'275px'}, s).removeClass('Image3').addClass('Image4');
					$('.Image2').animate({width:'150px', top:'25px', left:'190px'}, s).removeClass('Image2').addClass('Image3');
					$('.Image1').animate({width:'190px', top:'0', left:'90px'}, s).removeClass('Image1').addClass('Image2');
					$('.Image0').animate({width:'150px', top:'25px', left:'30px'}, s).removeClass('Image0').addClass('Image1');
					$('#carousel').append(['<img class="Image Image0" id="image', carouselFirst, '" src="', $(carouselItems[carouselFirst]).attr('src'), '" alt="" />'].join(''));
					showTitle();
				}

				function removeItself() {
					$(this).remove();
				}

				function showTitle() {
					carouselCur = parseInt($('.Image2')[0].id.replace('image', ''));
					$('#imageTitle').html(['<a href="', $(carouselItems[carouselCur]).data('link'), '">', $(carouselItems[carouselCur]).data('title'), '</a>'].join(''));
					$('#imageTitle a').fancybox();
				}

				function openWebsite() {
					$('#imageTitle a').click();
				}
			break;
		}
	};
	$('.goscale-plugins-pictures').goscalePluginsPictures();
})(jQuery);