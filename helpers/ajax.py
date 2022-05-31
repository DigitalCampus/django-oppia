

def is_ajax(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return True
    else:
        return False
