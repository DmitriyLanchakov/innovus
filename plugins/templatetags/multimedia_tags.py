# -*- coding: utf-8 -*-

from re import compile
from django import template

# --------------------------------------------------------------------------- #

register = template.Library()

PLAYER_SRC  = '/media/static/flash/player.swf'
SETTINGS_SRC = '/media/static/css/video-ru-full.txt'

# --------------------------------------------------------------------------- #

class VideoPlayerNode(template.Node):
    def __init__(self, file, width, height, title, settings):
        self.file     = template.Variable(file)
        self.title    = template.Variable(title)
        self.width    = width
        self.height   = height
        self.settings = settings

    def render(self, context):
        return template.loader.render_to_string('plugins/videoplayer.html',
            dict(
                width  = self.width,
                height = self.height,
                file         = self.file.resolve(context),
                title        = self.title.resolve(context),
                settings_src = self.settings,
                player_src   = PLAYER_SRC,
            ),
            context_instance=template.RequestContext(context['request']),
        )

# --------------------------------------------------------------------------- #

@register.tag
def videoplayer(parser, token):
    """
    Usage:
    
    {% videoplayer "file.flv" 640x480 %}
    {% videoplayer "file.flv" 640x480 "Movie title" %}
    {% videoplayer "file.flv" 640x480 "Movie title" "uppod.txt" %}

    """
    bits = token.split_contents()

    if len(bits) < 4:
        raise template.TemplateSyntaxError(
            'Tag %s accepts at least 3 arguments' % bits[0]
        )

    if not compile('^(\d+)x(\d+)$').match(bits[2]): 
        raise template.TemplateSyntaxError(
            '%s size must be specified in [width]x[height] format' % bits[0]
        )

    width, height = bits[2].split('x', 2) 

    return VideoPlayerNode(
        file     = bits[1],
        title    = bits[3] if len(bits) > 3 else '',
        settings = bits[4].strip('"') if len(bits) > 4 else SETTINGS_SRC,
        width    = width,
        height   = height,
    )
    
