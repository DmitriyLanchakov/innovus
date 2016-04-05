# -*- coding: utf-8 -*-

from mimetypes import guess_type
from django.template import Node, Variable, Library, TemplateSyntaxError, loader, RequestContext

# --------------------------------------------------------------------------- #

register = Library()

# --------------------------------------------------------------------------- #

class MediaBaseNode(Node):
    def __init__(self, object, varname):
        self.object = Variable(object)
        self.varname = varname

    def render(self, context):
        object = self.object.resolve(context)
        files, matched  = object.attachments.all(), []

        for f in files:
            if self.match(f):
                matched.append(f)

        context[self.varname] = matched
        return unicode('')

    def match(self, filename):
        raise NotImplementedError('Please implement this in child class')

# --------------------------------------------------------------------------- #

class GalleryNode(MediaBaseNode):
    def match(self, file):
#        mime = guess_type(file.file.path)[0]
        return file.file.path.endswith('gif')  or \
               file.file.path.endswith('jpeg') or \
               file.file.path.endswith('jpg') or \
               file.file.path.endswith('png')

# --------------------------------------------------------------------------- #

class VideoNode(MediaBaseNode):
    def match(self, file):
        return file.file.path.endswith('flv') #'video/x-flv' in guess_type(file.file.path)

# --------------------------------------------------------------------------- #

def tag_factory(parser, token, NodeClass):
    bits = token.split_contents()

    if len(bits) != 5 or bits[1] != 'for' or bits[3]  != 'as':
        raise TemplateSyntaxError(
            'Wrong syntax for %(tag)s. Valid is {% %(tag)s ' +
            'for [object] as [var] %}' % dict(tag=bits[0])
        )
    return NodeClass(object=bits[2], varname=bits[4])

# --------------------------------------------------------------------------- #

def inclusion_tag_factory(parser, token, template):
    class InclusionNode(Node):
        def __init__(self, object, template):
            self.object = Variable(object)
            self.template = template


        def render(self, context):
            return loader.render_to_string(
                self.template,
                dict(object=self.object.resolve(context)),
                context_instance=RequestContext(context['request']),
            )

    # ----

    bits = token.split_contents()

    if len(bits) != 3 or bits[1] != 'for':
        raise TemplateSyntaxError(
            'Wrong syntax for %(tag)s. Valid is {% %(tag)s ' +
            'for [object] %}' % dict(tag=bits[0])
        )

    return InclusionNode(object=bits[2], template=template)

# --------------------------------------------------------------------------- #

@register.tag
def make_gallery(parser, token):
    return tag_factory(parser, token, GalleryNode)

@register.tag
def render_gallery(parser, token):
    return inclusion_tag_factory(
        parser, token, 'periodics/templatetags/gallery.html'
    )

# --------------------------------------------------------------------------- #

@register.tag
def make_video(parser, token):
    return tag_factory(parser, token, VideoNode)

@register.tag
def render_video_full(parser, token):
    return inclusion_tag_factory(
        parser, token, 'periodics/templatetags/video_full.html'
    )

@register.tag
def render_video_preview(parser, token):
    return inclusion_tag_factory(
        parser, token, 'periodics/templatetags/video_preview.html'
    )


@register.tag
def multimedia(parser, token):
    templates = dict(
        video = 'periodics/content/video.html',
        image = 'periodics/content/image.html',
        error = 'periodics/content/error.html',
    )

    bits = token.split_contents()
    if bits[0] != "multimedia" or bits[1] != "for":
        raise TemplateSyntaxError(
            'Wrong syntax for %(tag)s. Valid is {% %(tag)s ' +
            'for [object] %}' % dict(tag=bits[0])
        )
    if len(bits) == 5:
        templates = bits[4]


    return MultimediaNode(post=bits[2], templates=templates)


class MultimediaNode(Node):

    def __init__(self, post, templates):
        self.post = Variable(post)

        if not isinstance(templates, dict):
            self.templates = Variable(templates)
        else:
            self.templates = templates


    def render(self, context):
        post = self.post.resolve(context)

        if not isinstance(self.templates, dict):
            self.templates = self.templates.resolve(context)

        if post.attachments.public().count():

            for item in post.attachments.public():

                if item.file.path.endswith('flv'):
                    return loader.render_to_string(
                        self.templates['video'],
                        { 'item': item },
                    context_instance=RequestContext(context['request']))

        elif post.picture_src and post.picture_show:
            return loader.render_to_string(
                self.templates['image'],
                { 'item': post.picture_src, 'post': post },
                context_instance=RequestContext(context['request'])
            )

        else:
            return loader.render_to_string(
                self.templates['error'],
                context,
                context_instance=RequestContext(context['request'])
            )

