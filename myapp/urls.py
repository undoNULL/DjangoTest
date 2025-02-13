from django.urls import path
from .views import CreatePostAPIView, GetAllPostAPIView, GetPostByIdAPIView, GetPostByTitleAPIView, LoginAPIView, SetNameAPIView, UserRegisterAPIView, hello

urlpatterns = [
    path('', hello),
    path('regist/', UserRegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('set_name/', SetNameAPIView.as_view()),
    path('create_post/', CreatePostAPIView.as_view()),
    path('get_all_post/', GetAllPostAPIView.as_view()),
    path('get_post_by_title/', GetPostByTitleAPIView.as_view()),
    path('get_post_by_id/', GetPostByIdAPIView.as_view()),
]
