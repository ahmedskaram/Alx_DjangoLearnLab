# notifications/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user, read=False).order_by('-timestamp')
    notifications_data = [
        {
            'actor': notification.actor.username,
            'verb': notification.verb,
            'target': str(notification.target),
            'timestamp': notification.timestamp,
            'read': notification.read
        }
        for notification in notifications
    ]
    return Response(notifications_data)
