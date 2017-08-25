from crm import models


class BasicAdmin(object):
    # 表中显示的字段列表
    list_display = []
    # 右侧的过滤功能的字段
    list_filter = []
    # 表上面的搜索功能的字段
    search_fields = []
    # 每页显示的记录数
    list_per_page = 20
    # 默认排序字段
    ordering =None
    
class CustomerAdmin(BasicAdmin):
    list_display = ['id', 'qq', 'name', 'source', 'consultant', 'consult_course', 'date', 'status']
    list_filters = ['source', 'consultant', 'consult_course', 'status', 'date']
    search_fields = ['qq', 'name', 'consultant__name']
    list_per_page = 5
    ordering = 'qq'
    
class CustomerFollowUpAdmin(BasicAdmin):
    list_display = ['customer', 'consultant', 'date']
    

enable_admins = {}
def register(model_class, admin_class=None):
    # app_label能拿到应用名
    if model_class._meta.app_label not in enable_admins:
        enable_admins[model_class._meta.app_label] = {}

    admin_class.model = model_class
    # model_name能拿到模型类的名字
    enable_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class
    
register(models.Customer, CustomerAdmin)
register(models.CustomerFollowUp, CustomerFollowUpAdmin)