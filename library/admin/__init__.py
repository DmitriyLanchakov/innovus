from django.contrib import admin
from .persons import PersonAdmin
from .resources import ResourceAdmin, CategoryAdmin

from library.models import Category, Person, Video, Audio, Document, Picture

admin.site.register(Video, ResourceAdmin)
admin.site.register(Audio, ResourceAdmin)
admin.site.register(Document, ResourceAdmin)
admin.site.register(Picture,  ResourceAdmin)


admin.site.register(Person, PersonAdmin)
admin.site.register(Category, CategoryAdmin)

