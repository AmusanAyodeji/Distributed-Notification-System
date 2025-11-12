from fastapi import APIRouter, Header
from schema.notification import NotificationRequest
from services.queue import send_to_queue 

router = APIRouter()

notifstatus = {}

@router.post("/api/v1/notifications/")
def create_notification(notifrequest: NotificationRequest):
    queue_name = "email.queue" if notifrequest.notification_type == "email" else "push.queue"
    send_to_queue(queue_name, notifrequest.model_dump())
    notifstatus[notifrequest.request_id] = "pending"
    return {
        "success": True,
        "message": "Notification dispatched",
        "data": notifrequest.model_dump(),
        "meta": {}
    }
    #store the notification status in a local cache and general storage share

# @router.post("/api/v1/{notification_preference}/status/")
# def check_notification_status(notification_id: str,  status: NotificationStatus,  timestamp: Optional[datetime],  error: Optional[str]):

    #updates the status of the email when it has sent to queue