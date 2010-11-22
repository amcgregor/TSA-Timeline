$(function(){
    $.plugins({
            plugins: [
                    {
                        id: 'timeago',
                        js: '/js/jquery.timeago.js',
                        fn: 'timeago',
                        ext: 'timeago',
                        sel: 'time'
                    },
                ]
        });
    
    // Find all absolute links and make them open in a new window.
    $('a[href^=http]').attr('target', '_blank');
});