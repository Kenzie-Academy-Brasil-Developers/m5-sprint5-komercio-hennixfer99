from django.urls import path


from .views import LoginView,AccountDetailView,AccountView,AccountUpdate,UpdateStatus
 
urlpatterns = [
    path('accounts/', AccountView.as_view()),
    path('accounts/newest/<int:num>/', AccountDetailView.as_view()),
    path('accounts/<pk>/', AccountUpdate.as_view()),
    path('accounts/<pk>/management/', UpdateStatus.as_view()),
    path('login/', LoginView.as_view()),
]  