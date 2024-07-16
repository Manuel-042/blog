from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('home', views.home, name="home"),
    
    path('register/', views.RegisterView, name="register"),

    path('login/', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('password_change/', views.password_change, name="password_change"),
    
    path('password_reset/',views.PasswordResetView.as_view(), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ), name='password_reset_confirm'),
    
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ), name='password_reset_complete'),
    
    
    path('bloglist/', views.BlogListView.as_view(), name="bloglist"),
    path('blogcreate/', views.createBlog, name='blogcreate'),
    path('blogdetail/<int:pk>', views.BlogDetailView.as_view(), name='blogdetail'),
    
    path('uploadImageFile/', csrf_exempt(views.uploadImageFile), name="uploadImageFile"),
    path('uploadImageUrl/', csrf_exempt(views.uploadImageUrl), name="uploadImageUrl"),
    
    path('likepost/<int:post_id>', views.LikePostView, name="post-likes"),
    path('commentpost/<int:post_id>', views.CommentPostView.as_view(), name="post-comments"),
    path('likecomment/<int:post_id>/<int:comment_id>', views.CommentLikeView.as_view(), name="comments-likes"),
]

