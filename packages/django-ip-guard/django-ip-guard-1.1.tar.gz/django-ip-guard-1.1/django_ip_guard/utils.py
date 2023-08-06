def get_client_ip(request):
    client_ip = request.META.get('REMOTE_ADDR', '')
    return client_ip

