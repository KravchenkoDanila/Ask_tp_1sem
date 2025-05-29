from django.urls import path, re_path
from askme import views

urlpatterns = [
    path('', views.index, name="index"),
    path('hot/', views.hot, name="hot"),
    path('tag/<str:tag_name>/', views.tag, name="tag"),
    path('question/<int:question_id>/', views.question, name="question"),
    path('login/', views.log_in, name="login"),
    path('signup/', views.signup, name="signup"),
    path('ask/', views.ask, name="ask"),
    path('logout/', views.logout, name='logout'),

    re_path(r'^settings', views.settings, name="settings"),

]