from django.contrib import admin
from tkm.models import *

# Register your models here.
@admin.register(Post)
class StudenAdim(admin.ModelAdmin):
 list_display = ['id','title']