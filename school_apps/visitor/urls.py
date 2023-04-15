from django.urls import path
from . import views

app_name = 'visitor'

urlpatterns = [
    path('form/', views.visitorform, name='visitorform'),
    path('list/', views.VisitorListView.as_view(), name='visitor_list'),
    path('detail/<int:pk>', views.VisitorDetailView.as_view(), name='visitor_detail'),
    path('printform/<int:pk>', views.printform, name='printform'),
]

