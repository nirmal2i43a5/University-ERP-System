from django import urls
from django import template

register = template.Library()

@register.filter(name='has_namespace')
def has_namespace(request_url,args): 
    
    # request_url get the current ur from template and check with respective namespace
    request_url_namespace = urls.resolve(request_url).namespace
    # print(":::Inside templatetags:::")
    # print(request_url,request_url_namespace)
    if len(args.split(',')) == 2:
        module_home_url,my_namespace =  args.split(',')#args content multi variables
        print(module_home_url)
        module_home_namespace = urls.resolve(module_home_url).namespace
        print(module_home_url)
    else:#this is for some app that do not have namespace(i.e for schedule app or others)
        module_home_url = args
    
    # print(request_url_namespace,module_home_namespace)
    if request_url_namespace == module_home_namespace:# and request_url_keyword == module_url_keyword:
        return True
    else:
        return False
    
    
    # url_resolver = urls.get_resolver(urls.get_urlconf())
    # all_namespace_list = url_resolver.namespace_dict.keys()
    # return True if request_url_namespace in list(all_namespace_list) else False


