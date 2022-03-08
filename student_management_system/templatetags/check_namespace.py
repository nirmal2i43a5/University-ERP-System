from django import urls
from django import template

register = template.Library()

@register.filter(name='has_namespace')
def has_namespace(request_url): 
    # request_url get the current ur from template and chec with respective namespace
    my_namespace = urls.resolve(request_url).namespace
    url_resolver = urls.get_resolver(urls.get_urlconf())
    all_namespace_list = url_resolver.namespace_dict.keys()
    return True if my_namespace in list(all_namespace_list) else False
