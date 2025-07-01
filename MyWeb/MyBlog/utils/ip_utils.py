from django.http import HttpRequest

def get_client_ip(request:HttpRequest):

    x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forward_for:
        ip = x_forward_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR','0.0.0.0')
        
    print(f"成功获取：{ip}")

    return ip