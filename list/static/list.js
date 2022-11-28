window.Superlist = {}
window.Superlist.initialize = function() {
    $('input[name="text"]').on('keypress', function() {
        $('.has-error').hide();
    });
};