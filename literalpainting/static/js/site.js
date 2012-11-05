site = {
    processing: false,

    clean: function() {
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
	site.clean();
	if (data.status) {
	    var actions = data.data.actions;
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
	site.clean();
    },

    /**
     * Change state while waiting for response.
     */
    submit: function (evt) {
	// Disable re-submit
	if (site.processing) {
	    return false;
	}
	site.clean();
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

