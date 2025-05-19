from django.urls import path

from askme import views

urlpatterns = [
    path('', views.index, name="index"),
    path('hot/', views.hot, name="hot"),
    path('tag/<str:tag_name>/', views.tag, name="tag"),
    path('question/<int:question_id>/', views.question, name="question"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('ask/', views.ask, name="ask"),

]