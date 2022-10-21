from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
User = get_user_model()
from listing.extras import delete_realtors_listing_data

class UserAccountAdmin(admin.ModelAdmin):
    using = 'users'
    list_display = ('id', 'email', 'name', 'is_realtor')
    list_display_links = ('id', 'email', 'name', 'is_realtor')
    list_filter = ('email', 'is_realtor')
    search_fields = ('email', 'name',)
    list_per_page = 25
    
    

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        email = obj.email
        print('Delete Model Email: ')
        print(email)
        obj.delete(using=self.using)
        print('Calling Delete Realtor Function...')
        delete_realtors_listing_data(email)
        print('Finished Delete Realtor Function')

    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


admin.site.register(User, UserAccountAdmin)
    