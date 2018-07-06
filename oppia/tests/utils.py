from django.urls import reverse
from tastypie.models import ApiKey


def get_api_key(user):
    """
    Returs the ApiKey for a user object. If it does not exist yet, is generated
    """

    try:
        api_key = ApiKey.objects.get(user=user)
    except ApiKey.DoesNotExist:
        #if the user doesn't have an apiKey yet, generate it
        api_key = ApiKey.objects.create(user=user)
    return api_key


def get_api_url(resource_name, resource_id=None):
    """
    Returs the ApiKey for a user object. If it does not exist yet, is generated
    """
    view_name = 'api_dispatch_list' if resource_id is None else 'api_dispatch_detail'
    kwargs = {'resource_name': resource_name, 'api_name': 'v1'}
    if resource_id is not None:
        kwargs['pk'] = resource_id
    return reverse(view_name, kwargs=kwargs)
