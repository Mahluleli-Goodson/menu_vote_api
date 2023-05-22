from django.http import JsonResponse, HttpResponse


def liveness_check_view(request):
    # Check if the request expects JSON response
    if 'application/json' in request.headers.get('Accept', ''):
        return JsonResponse({'message': 'working'})
    else:
        return HttpResponse('working')
