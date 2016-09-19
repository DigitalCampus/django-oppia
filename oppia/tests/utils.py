from tastypie.models import ApiKey


def getApiKey(user):
    """
    Returs the ApiKey for a user object. If it does not exist yet, is generated
    """

    try:
        api_key = ApiKey.objects.get(user=user)
    except ApiKey.DoesNotExist:
        #if the user doesn't have an apiKey yet, generate it
        api_key = ApiKey.objects.create(user=user)
    return api_key