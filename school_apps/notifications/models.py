from django.db import models
import json
from student_management_app.models import CustomUser as User

# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer


class Notification(models.Model):
    NOTIFICATION_TYPES = ((1, "Added"), (2, "Updated"), (3, "Assignment"))

    post = models.CharField(max_length=200, null=True)
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    is_seen = models.BooleanField(default=False)
    type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        # channel_layer=get_channel_layer()
        notification_obj = Notification.objects.all().count()
        data = {
            "count": notification_obj,
            "current_notification": self.post,
            "notification_type": self.notification_type,
        }

        # async_to_sync(channel_layer.group_send)(
        # 'test_notification_group',{
        # 	'type':'send_notification',
        # 	'value':json.dumps(data)
        # }
        # )
        super(Notification, self).save(*args, **kwargs)
