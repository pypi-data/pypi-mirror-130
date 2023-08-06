from django.contrib import admin

from .models import DigRule


class DigRuleAdmin(admin.ModelAdmin):
    pass

admin.site.register(DigRule, DigRuleAdmin)

