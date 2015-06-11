/** jQuery fadeQueue - v0.5 - 25/2/2011
* Copyright (c) 2011 Palle Zingmark <www.palleman.nu>
* Dual licensed under the MIT and GPL licenses.
*/
(function ($) {
	/**
	* This plugin creates a queue containing all children inside the provided parent element, 
	* then the plugin steps thru the queue and fades in the element, one after another. You 
	* can also choose to start the queue at any direct children inside the provided parent.
	*
	* @demo http://jquery.palleman.nu/fadequeue/
	* @fiddle http://jsfiddle.net/pallezingmark/D46fS/
	*
	* @param {number|object|function} These parameters can be provided:
	*
	*  @param {number} Provide the duration (miliseconds) for the queued item to fade in.
	*   @default: 200
	*   @example: 
	*    $('#mydiv').fadeQueue(500);
	*
	*  @param duration [number] {object} Provide the duration (miliseconds) for the queued item to fade in.
	*   @default: 200
	*   @example: 
	*    $('#mydiv').fadeQueue({ 
	*     duration: 500 
	*    });
	*
	*  @param pause [number] {object} Provide a pause (miliseconds) between the fade in durations.
	*   @default: (duration / 2)
	*   @example: 
	*    $('#mydiv').fadeQueue({ 
	*     pause: 100 
	*    });
	*
	*  @param startAt [node] {object} Provide a node where the animation will force a start.
	*   @default: first-child
	*   @example: 
	*    $('#mydiv').fadeQueue({ 
	*     startAt: $('#mydiv :nth-child(3)') 
	*    });
	*
	*  @param {function} Provide a callback function that will be called when queue is empty.
	*   @example: 
	*    $('#mydiv').fadeQueue(function(){ 
	*     alert('Queue is empty') 
	*    });
	*
	*/
	$.fn.fadeQueue = function (args) {

		//# Variables used
		var parent = $(this),
			params = {},
			forceStart = null,
			duration = 200,
			pause = 0,
			callBack = null,
			fadeTimer = 0,
			pauseTimer = 0,
			start = parent.children(':first');

		if(typeof args !== 'undefined'){
			//# Loop thru arguments, if provided.
			for (var i = 0, n = arguments.length; i < n; i++) {
				var a = arguments[i];
				switch (typeof a) {
				case 'number':
					duration = a;
					break;
				case 'object':
					params = a;
					break;
				case 'function':
					callBack = a;
					break;
				}
			}

			//# Check if any parameters is provided.
			forceStart = (typeof params.startAt !== 'undefined') ? params.startAt : null;
			duration = (typeof params.duration !== 'undefined') ? params.duration : duration;
			pause = (typeof params.pause !== 'undefined') ? params.pause : pause;
		}

		//# If no pause is provided, set the default 
		//# pause at half the duration. (best effect?)
		if(pause === 0){
			pause = (duration / 2);
		}

		//# Check if we should force the animation to start 
		//# on another child instead of first-child.
		if (forceStart) {
			forceStart.next().nextAll().hide();
			start = forceStart;
		} else {
			$(this).children().hide();
		}

		//# Stop any allready ongoing animations 
		//# on the provided children.
		parent.children().stop(true,true);
		
		//# Begin to fade element
		var fadeElement = function (elm) {
			if (elm.length !== 0) {
				//# We still have elements in queue.
				fadeTimer = window.setTimeout(function () {
					elm.fadeIn(duration);
					pauseTimer = window.setTimeout(function () {
						fadeElement(elm.next());
					}, pause);
				}, pause / 2);
			} else {
				//# No more elements in queue.
				//# If a callback function was provided - return it.
				if (typeof callBack == 'function') {
					return new callBack();
				}
			}
		};

		//## Initiate function
		fadeElement(start);

	};
})(jQuery);