from django.shortcuts import render
from king_admin.utils import table_filter
# Create your views here.
from king_admin import king_admin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def index(request):
    # print(king_admin.enable_admins['crm']['customer'].model)
    return render(request, 'king_admin/table_index.html', {'table_list':king_admin.enable_admins})

def display_table_objs(request, app_name, table_name):
    admin_class = king_admin.enable_admins[app_name][table_name]
    object_list,filter_condtions = table_filter(request, admin_class)
    paginator = Paginator(object_list, admin_class.list_per_page)
    
    page = request.GET.get('page')
    print(page,'==============')
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        query_sets = paginator.page(1)
    except EmptyPage:
        query_sets = paginator.page(paginator.num_pages)
        
    return render(request, 'king_admin/table_objs.html', {'admin_class':admin_class,
                                                          'query_sets':query_sets,
                                                          'filter_condtions':filter_condtions})
    
    