from django import urls
from django import template

register = template.Library()

@register.filter(name='has_namespace')
def has_namespace(request_url,args): 
    print("-----------------------I am inside Namespace-----------------------***Do this using session concept*******")
    
    request_url_namespace = urls.resolve(request_url).namespace
    if len(args.split(',')) == 2:
        module_home_url,my_namespace =  args.split(',')#args content multi variables
    else:#this is for some app that do not have namespace(i.e for schedule app or others)
        module_home_url = args
        
    module_home_namespace = urls.resolve(module_home_url).namespace
    if request_url_namespace == module_home_namespace:
        return True
    else:
        return False
    
    
    # url_resolver = urls.get_resolver(urls.get_urlconf())
    # all_namespace_list = url_resolver.namespace_dict.keys()
    # return True if request_url_namespace in list(all_namespace_list) else False


