from django.contrib import admin

from .models import Case, Evidence, Incident


admin.site.register(Case)
admin.site.register(Incident)
admin.site.register(Evidence)
