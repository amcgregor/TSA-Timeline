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
});