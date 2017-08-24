from crm import models


class BasicAdmin(object):
    list_display = []
    list_filter = []
    list_per_page = 20
    
class CustomerAdmin(BasicAdmin):
    list_display = ['qq', 'name', 'source', 'consultant', 'consult_course', 'date', 'status']
    list_filters = ['source', 'consultant', 'consult_course', 'status']
    list_per_page = 2
    
class CustomerFollowUpAdmin(BasicAdmin):
    list_display = ['customer', 'consultant', 'date']
    

enable_admins = {}
def register(model_class, admin_class=None):
    if model_class._meta.app_label not in enable_admins:
        enable_admins[model_class._meta.app_label] = {}

    admin_class.model = model_class
    enable_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class
    
register(models.Customer, CustomerAdmin)
register(models.CustomerFollowUp, CustomerFollowUpAdmin)