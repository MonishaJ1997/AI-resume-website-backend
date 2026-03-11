from django.contrib import admin
from .models import LandingImage


@admin.register(LandingImage)
class LandingImageAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")



from django.contrib import admin
from .models import Job, JobApplication

admin.site.register(Job)
admin.site.register(JobApplication)


from django.contrib import admin
from .models import Blog

admin.site.register(Blog)

from django.contrib import admin
from .models import Template

admin.site.register(Template)



from django.contrib import admin
from .models import Logo

admin.site.register(Logo)

from django.contrib import admin
from .models import FeatureIcon

admin.site.register(FeatureIcon)    