from api_auth import models

def check_basic_credentials(self, api, request):
    if not 'HTTP_AUTHORIZATION' in request.META:
        return False
    header = request.META['HTTP_AUTHORIZATION'].split()[1]
    provided_credentials = base64.b64decode(header)\
        .decode('utf-8').split(':')
    username = provided_credentials[0]
    password = provided_credentials[1]
    credentials = models.BasicAuthCredentials.objects.filter(
        api=api, username=username, password=password
    )
    return credentials

def check_key_credentials(api, request):
    credentials_set = models.KeyCredentials.objects.filter(api=api)
    accepted_params = models.AcceptedKeyParameter.objects.filter(api=api)

    for credentials in credentials_set:
        for param in accepted_params:
            param_dict = None
            if param.param_type == models.AcceptedKeyParameter.HEADER:
                param.name = 'HTTP_' + param.name.upper()
                param_dict = request.META
            if param.param_type == models.AcceptedKeyParameter.QUERY:
                param_dict = request.query_params
            if param_dict.get(param.name, None) == credentials.key:
                return credentials
    return None

def check_credentials(api, request, auth_method):
    if auth_method.auth_type == 'basic':
        return check_basic_credentials(api, request)
    elif auth_method.auth_type == 'key':
        return check_key_credentials(api, request)
    else:
        return None

def authenticate(api, request, auth_methods):
    credentials = None
    for auth_method in auth_methods:
        credentials = check_credentials(api, request, auth_method)
        if credentials:
            break

    if not credentials:
        return None
    else:
        return credentials.consumer
