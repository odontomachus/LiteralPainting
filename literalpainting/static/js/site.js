/**
 * Collapse / expand expandable elements.
 */
$('.expandable .expander').click( function(evt) {
    $(evt.target).siblings('.expands').first().toggleClass('hidden');
});

/**
 * Submit form and parse response.
 */
$('#command form').submit(function (evt) {
    var target = $(evt.target)
    // Get form values
    var values = target.serializeArray();
    var url = '/ajax' + target.attr('action');
    $.post(url, values, function (data) {
	console.log(data);
    });

    return false;
});
