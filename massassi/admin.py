from django.contrib import admin


class MassassiModelAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        add_fields = ('created_at', 'created_by', 'last_modified_at', 'last_modified_by')
        if(self.fields):
            return self.fields + add_fields
        else:
            return add_fields

    # These fields should be shown on the form, but should be readonly
    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('created_at', 'created_by', 'last_modified_at', 'last_modified_by')

    # On save, set the created_by/last_modified_by as appropriate
    def save_model(self, request, obj, form, change):
        # some user-editable tables also have a `user` field; if it's present
        # populate from the request
        for field in obj._meta.get_fields():
            if field.name == 'user':
                obj.user = request.user

        if change:
            obj.last_modified_by = request.user
        else:
            obj.created_by = request.user
            obj.last_modified_by = request.user

        obj.save()

class MassassiModelWithUserAdmin(MassassiModelAdmin):
    """
    TODO: implement this class with a `user` field that gets populated with
    currently-logged-in user by default
    """
    pass
