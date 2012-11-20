site = {
    processing: false,

    /**
     * Clean site after a submit.
     */
    reset: function() {
	$('#processing').hide();
	$('#go').show();
	$('#errors').hide();
	$('#errors ul').html('');
	site.processing = false;
    },

    /**
     * Parse the response from a call to server's parse method.
     */
    parse: function (data) {
	site.reset();
	if (data.status) {
	    /**
	     * Draw objects on canvas. Expects a json array with
	     * [ [arg0, arg1, ... argN, funcName], <more actions...> ]
	     */
	    var actions = data.data.actions;
	    sentence = $('<li />').hide().html(data.data.sentence);
	    $('#history ul').prepend(sentence);
	    sentence.slideDown();
	    for (var i in actions) {
		var action = data.data.actions[i];
		var figure = action.pop()
		var actionMap = {
		    'circle': lp.circle,
		    'rectangle': lp.rectangle,
		    'line': lp.line,
		};
		actionMap[figure].apply(this, action);
	    }
	}
	else {
	    for (var error in data.errors) {
		$('#errors ul').append('<li>'+data.errors[error]+'</li>');
	    }
	    $('#errors').show();
	}
    },

    /**
     * Clean waiting state if backend requeest errors out.
     */
    error: function (jqXHR, textStatus, errorThrown) {
	site.reset();
    },

    /**
     * Change state while waiting for response.
     */
    submit: function (evt) {
	// Disable re-submit
	if (site.processing) {
	    return false;
	}
	site.reset();
	site.processing = true
	$('#processing').show();
	$('#go').hide();
	var target = $(evt.target)
	// Get form values
	var values = target.serializeArray();
	var url = '/ajax' + target.attr('action');
	// Parse the response
	$.ajax(url, {
	    data: values,
	    type: 'POST',
	    success: site.parse,
	    error: site.error,
	});
	return false;
    },
}

/**
 * Collapse / expand expandable elements.
 */
$('.expandable .expander').click( function(evt) {
    $(evt.target).siblings('.expands').first().toggleClass('hidden');
});


/**
 * Setup ajax.
 */
$('#command form').submit(site.submit);

