

from django.shortcuts import render

# @permission_required("authentication.view_user_log", raise_exception=True)
def user_log_list(request):
    context = {
        "title": "User Log",
        "active_menu": "authentication",
    }
    return render(request, "userlog/userlog.html", context=context)


