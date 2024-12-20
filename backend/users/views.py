from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User

@api_view(['GET'])
def user_counts(request):
    total_users = User.objects.count()
    total_admins = User.objects.filter(is_superuser=True).count()
    return Response({
        'total_users': total_users,
        'total_admins': total_admins,
    })