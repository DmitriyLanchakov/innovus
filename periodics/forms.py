# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _
from periodics.models import *

# --------------------------------------------------------------------------- #

class PostAdminForm(forms.ModelForm):
    published = forms.BooleanField(required=False, help_text=_('Post will be saved as draft if not checked'))

    def __init__(self, *args, **kwargs):
        super(PostAdminForm, self).__init__(*args, **kwargs)
        select = self.fields['category'].widget

        # Customize category field
        self.fields['category'].widget = forms.CheckboxSelectMultiple()
        self.fields['category'].widget.choices = select.choices
        self.fields['category'].help_text = ''

        # Customize 'publish when saving' state
        self.fields['published'].initial = self.instance.publisher_public is not None


    class Meta:
        model = Post
        exclude = ('created_by', 'modified_by', )


# --------------------------------------------------------------------------- #
class CommentForm(forms.ModelForm):
    post = forms.IntegerField(widget=forms.HiddenInput)
    type = forms.CharField(widget=forms.HiddenInput)
    content = forms.CharField(widget=forms.Textarea, label=_('Message'))

    class Meta:
        model = Comment
        exclude = (
            'ip_address', 'created_by', 'modified_by','created_at',
            '_commentable_object_id', '_commentable_content_type',
            'is_approved', 'parent', 'user', 'author_name', 'author_email',
        )
    

# --------------------------------------------------------------------------- #

class GuestCommentForm(CommentForm):
    author_name  = forms.CharField(label=_('Name'), max_length=255, required=True)
    author_email = forms.EmailField(label=_('E-mail ').strip(), required=True)

    class Meta:
        model = Comment
        exclude = (
            'ip_address', 'created_by', 'modified_by','created_at',
            '_commentable_object_id', '_commentable_content_type',
            'is_approved', 'parent', 'user', 
        )

# --------------------------------------------------------------------------- #

class CategoryAdminForm(forms.ModelForm):
    per_page = forms.IntegerField(initial=10)

    class Meta:
        model = Category
        exclude = ('created_by', 'modified_by', 'sort_order', )

# --------------------------------------------------------------------------- #

def get_form(request):
    """
    Comment form factory
    """
    return CommentForm if request.user.is_authenticated() else GuestCommentForm
