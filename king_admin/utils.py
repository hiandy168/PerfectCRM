def table_filter(request, admin_class):
    # 过滤get请求传过来的参数，在数据库中查询出查询集

    filter_conditions = {}
    keywords = ['page']
    for k,v in request.GET.items():
        if k in keywords:
            continue
        if v:
            filter_conditions[k]=v
    print(filter_conditions)
    return admin_class.model.objects.filter(**filter_conditions), filter_conditions