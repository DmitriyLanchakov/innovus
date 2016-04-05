/**
 * jQuery Maxlength plugin
 * @version        $Id: jquery.maxlength.js 18 2009-05-16 15:37:08Z emil@anon-design.se $
 * @package        jQuery maxlength 1.0.5
 * @copyright    Copyright (C) 2009 Emil Stjerneman / http://www.anon-design.se
 * @license        GNU/GPL, see LICENSE.txt
 */

(function($)
{
    $.fn.maxlength = function(options)
    {
        var settings = jQuery.extend(
        {
            events:        [],   // Array of events to be triggered
            callbacks:     [],   // Array of callbacks
            maxCharacters: 10    // Characters limit
        }, options);

        // Add the default event
        $.merge(settings.events, ['keyup','change']);

        return this.each(function()
        {
            var item = $(this);
            var charactersLength = item.val().length;

            var getCharsLeft = function()
            {
                return Math.max(settings.maxCharacters - charactersLength, 0);
            }

            var checkChars = function()
            {
                var exceed = charactersLength >= settings.maxCharacters;
                
                for (var i = 0; i < settings.callbacks.length; i++) {
                    settings.callbacks[i](item, getCharsLeft(), exceed);
                }

                if (exceed) {
                    item.val(item.val().substr(0, settings.maxCharacters));
                }
            }

            var validateElement = function()
            {
                var ret = false;

                if (item.is('textarea')) {
                    ret = true;
                } else if(item.filter("input[type=text]")) {
                    ret = true;
                } else if(item.filter("input[type=password]")) {
                    ret = true;
                }
                return ret;
            }

            if (validateElement()) {
                $.each(settings.events, function (i, n) {
                    item.bind(n, function(e) {
                        charactersLength = item.val().length;
                        checkChars();
                    });
                });
                checkChars();
            }
        });
    };
})(jQuery);