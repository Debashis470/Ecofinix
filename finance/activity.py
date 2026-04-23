from .models import UserActivity

def log_activity(request, action_text):
    if request.user.is_authenticated:
        UserActivity.objects.create(
            user=request.user,
            action=action_text
        )