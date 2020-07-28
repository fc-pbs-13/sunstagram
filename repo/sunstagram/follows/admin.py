from django.contrib import admin

# Register your models here.
from follows.models import Child, Parent


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', )


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'parent', 'user')
    list_select_related = ('user', 'parent')
