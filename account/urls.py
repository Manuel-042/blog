from django.urls import path
from . views import read_user, register, user_login, user_logout
from . import views

urlpatterns = [
    path("user/<int:pk>", read_user, name="user"),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="user"),
    
    #Blogs
    path("bloglist/", views.BlogListView.as_view(), name="all_blogs"),
    path('blogdetail/<int:pk>', views.SingleBlogDetailView.as_view(), name="blog_detail"),
    path('blogcategory', views.CategoryListView.as_view(), name="all_categories"),
    path('userbloglist/<int:pk>', views.SingleUserBlogsListView.as_view(), name="user_blog_list"),
    path('userbloglikes/<int:pk>', views.SingleUserBlogLikesView.as_view(), name="user_blog_likes"),
    path('likepost/<int:pk>', views.LikePostView.as_view(), name="liked_post"),
    path('commentpost/<int:pk>', views.CommentPostView.as_view(), name="comment_post"),
]

