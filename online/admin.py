from django.contrib import admin
import models
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')
class FolderAdmin(admin.ModelAdmin):
    list_display = ('folder_name', 'create_time')
class FileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file_size')
@admin.register(models.Userinfo)
class UserinfoAdmin(admin.ModelAdmin):
    list_display = ('User', 'email')


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Folder, FolderAdmin)
admin.site.register(models.File, FileAdmin)

