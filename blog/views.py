from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, update_session_auth_hash
from blog.delta import convert_delta_to_html
from blog.forms import BlogCreateForm, CreateUserForm, LoginForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie, requires_csrf_token
from django.contrib.auth.models import auth, User
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import ListView, CreateView, DetailView, FormView, View
from account.models import Blog, CustomUser, Likes, Comment, LikesComment
from account.serializers import BlogSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import logging
import datetime
import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json

logger = logging.getLogger(__name__)


# Create your views here.

def home(request):
    return render(request, 'blog/blogpage.html')

def RegisterView(request):
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('login')
            
    context = {'form': form}
    
    return render(request, 'registration/register.html', context=context)

def login(request):
    form = LoginForm()
    
    if request.method == "POST":
        form = LoginForm(request, data = request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth.login(request, user)
                
                # token, _ = Token.objects.get_or_create(user=user)
                messages.success(request, "You have been Successfully logged in")
                # context = {'token': token.key}
                response = redirect('home')
                # response.set_cookie('auth_token', token.key, httponly=True, secure=True)
                return response
            else:
                messages.error(request, "Invalid username or password")
                return render(request, 'registration/login.html', {'error': 'Invalid credentials.'})
        else:
            messages.error(request, "No user found with these Credentials")
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'registration/login.html', context)

# class LoginView(View):
#     form_class = LoginForm
#     initial = {"key": "value"}
#     template_name = "'blog/login.html"

#     def post(self, request, *args, **kwargs):
#         form = self.form_class()
#         if form.is_valid():     

#             user = authenticate(
#                 username=form.cleaned_data['username'],
#                 password=form.cleaned_data['password'],
#             )
            
#             if user is not None:
#                 auth.login(request, user)
                
#                 token, _ = Token.objects.get_or_create(user=user)

#                 context = {'token': token.key}
#                 response = redirect('home')
#                 response.set_cookie('auth_token', token.key, httponly=True, secure=True)
#                 return response
#             else:
#                 return render(request, 'blog/login.html', {'error': 'Invalid credentials.'})
#         context = {'form': form}
#         return render(request, 'blog/login.html', context)

@login_required()
def logout(request):
    if request.user.is_authenticated:   
        auth.logout(request)
        messages.success(request, "Logout Successful")
        response = redirect('login')
        # response.delete_cookie('auth_token')
        return response

    return redirect('login')

@login_required()
def password_change(request):
    if not request.user.is_authenticated:
        return render(request, "pages/404error.html")
    
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('login')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'registration/password_change.html', {'form': form})
    

# class BlogListView(LoginRequiredMixin, ListView):
#     login_url = 'login/'
#     model = Blog
#     serializer = BlogSerializer
#     template_name = 'blog/bloglistpage.html'
    
#     def get(self, request, *args, **kwargs):
#         all_blogs = Blog.objects.all()
#         serializer = self.serializer(all_blogs, many=True)
#         logger.warning('BlogListView was accessed at '+str(datetime.datetime.now())+' hours!')
        
#         for blog in all_blogs:
#             blog.likes_count = blog.likes.count()
            
#         context = {"blogs": serializer.data}
#         return render(request, self.template_name, context)

class BlogListView(LoginRequiredMixin, ListView):
    login_url = 'login/'
    model = Blog
    template_name = 'blog/bloglistpage.html'
    context_object_name = 'blogs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_blogs = Blog.objects.all()

        for blog in all_blogs:
            blog.likes_count = blog.likes.count()
            blog.user_has_liked = blog.likes.filter(author=self.request.user).exists()
            blog.comment_count = blog.comments.count()

        context['blogs'] = all_blogs
        logger.warning('BlogListView was accessed at ' + str(datetime.datetime.now()) + ' hours!')
        return context
    
# class BlogCreateView(LoginRequiredMixin, CreateView):
#     login_url = 'login'
#     model = Blog
#     form_class = BlogCreateForm
#     template_name = 'blog/blogcreatepage.html'
#     redirect_field_name = 'home'
    
#     def form_valid(self, form):
#         logger.warning('Blog was accessed at '+str(datetime.datetime.now())+' hours!')
#         form.instance.author = self.request.user  # Set the author of the blog post
#         form.instance.blogpost = convert_delta_to_html(form.cleaned_data['blogpost'])
#         messages.success(self.request, "Blog Created Successfully.")
#         return super().form_valid(form)
    
    
#     def get_success_url(self):
#         return reverse('home') 
@login_required()
def createBlog(request):
    if not request.user.is_authenticated:
        return render(request, "pages/404error.html")
    
    if request.method == "POST":
        form = BlogCreateForm(request.POST, request.FILES)
        # print(form)
        if form.is_valid():
            form.instance.author = request.user  # Set the author of the blog post
            #form.instance.blogpost = convert_delta_to_html(form.cleaned_data['blogpost'])
            messages.success(request, "Blog Created Successfully.")
            form.save()
            return redirect('home')
        else:
            logger.error('form is invalid!')
            print(form.errors)
    else:
        form = BlogCreateForm()
    
    return render(request, 'blog/blogcreatepage.html', {'form': form})

class BlogDetailView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    template_name = 'blog/blogdetailpage.html'
    redirect_field_name = 'home'
    model = Blog 
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')  # Use self.kwargs['pk']
        blog = Blog.objects.get(pk=pk)
        context["blog"] = blog
        context["likes_count"] = blog.likes.count()
        context["user_has_liked"] = blog.likes.filter(author=self.request.user).exists()
        comments= blog.comments.filter(parent=None).order_by('-created_at')
        context["comments"] = comments
        context["comment_count"] = blog.comments.count()
        
        # userHasLikedComment = []
        # totalLikeCount = []
        commentInfoList = []
        for comment in comments:
            user_has_liked_comment = LikesComment.objects.filter(comment=comment, author=self.request.user).exists()
            total_comment_likes = LikesComment.objects.filter(comment=comment).count()
            print(user_has_liked_comment)
            print(total_comment_likes)
            
            # userHasLikedComment.append(user_has_liked_comment)
            # totalLikeCount.append(total_comment_likes)
            
            comment_info = {
                'user_has_liked_comment': user_has_liked_comment,
                'total_comment_likes': total_comment_likes
            }
            
            commentInfoList.append(comment_info)
            
            
            #context["user_has_liked_comment"] = user_has_liked_comment
            # context["userHasLikedComment"] = userHasLikedComment
            # context["totalLikeCount"] = totalLikeCount
            context["comment_info"] = commentInfoList
            
        return context

@requires_csrf_token
def uploadImageFile(request):
    if request.method == 'POST':
        file = request.FILES.get('image')
        if not file:
            return JsonResponse({"success": 0, "error": "No file provided"}, status=400)

        response = cloudinary.uploader.upload(file)
        return JsonResponse({"success": 1, "file": {"url": response['secure_url']}})
    else:
        return JsonResponse({"success": 0, "error": "Invalid request method"}, status=405)
    
@requires_csrf_token
def uploadImageUrl(request):
    if request.method == 'POST':
        url = request.POST.get('url') 
        if not url:
            return JsonResponse({"success": 0, "error": "No URL provided"}, status=400)
        
        response = cloudinary.uploader.upload(url)
        return JsonResponse({"success": 1, "file": {"url": response['secure_url']}})
    else:
        return JsonResponse({"success": 0, "error": "Invalid request method"}, status=405)
    
# template_name = 'registration/password_reset_form.html',
# html_email_template_name = 'registration/password_reset_email.html'
# subject_template_name = 'registration/password_reset_subject'

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import get_object_or_404

def password_reset_request(request):
    if request.method == "POST":
        password_form = PasswordResetForm(request.POST)
        
        if password_form.is_valid():
            data = password_form.cleaned_data.get('email')
            user_email = CustomUser.objects.filter(Q(email=data))
            
            if user_email.exists():
                for user in user_email:
                    subject = "Password Reset Request"
                    email_template_name = "registration/password_reset_subject.txt"
                    params = {
                        'email': user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Divvy',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http'
                    }
                    email = render_to_string(email_template_name, params)
                    try:
                        send_mail(subject, email, '', [user.email], fail_silently=False)
                    except:
                        return HttpResponse("Invalid Header")
                    return redirect('password_reset_done')
    else:
        password_form = PasswordResetForm()
    context = {
        'form': password_form
    }
    
    return render(request, 'registration/password_reset_form.html', context )
    
class PasswordResetView(FormView):
    template_name = 'registration/password_reset_form.html'
    html_email_template_name = 'registration/password_reset_email.html'
    model = CustomUser
    form_class = PasswordResetForm
    success_url = "password_reset_done"
    
    def form_valid(self, form):
        my_subject = "Divvy Password Reset"
        #my_message = "This is an email sent from Divvy"
        my_recipient = form.cleaned_data['email']
        user = get_object_or_404(CustomUser, email=my_recipient)  # Fetch the user
        
        params = {
            'email': user.email,
            'domain': '127.0.0.1:8000',
            'site_name': 'Divvy',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'protocol': 'http'
        }
        my_message = render_to_string(self.html_email_template_name, params)
        
        send_mail(
            subject = my_subject,
            message = my_message,
            recipient_list = [my_recipient],
            from_email = None,
            fail_silently = False
        )
        
        
        return super().form_valid(form)

def LikePostView(request, post_id):
    if request.method == 'POST':
        user = request.user
        post = get_object_or_404(Blog, id=post_id)
        
        if Likes.objects.filter(author=user, post=post).exists():
            return JsonResponse({'message': 'Already liked', 'likes_count': post.likes.count()})
        
        like = Likes(author=user, post=post)
        like.save()
        
        likes_count = post.likes.count()
        
        return JsonResponse({'message': 'Liked', 'likes_count': likes_count})
    return JsonResponse({'error': 'Invalid Request' }, status=400)


class CommentLikeView(View):
    def post(self, request, post_id, comment_id):
        user = request.user
        post = get_object_or_404(Blog, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        
        print(user)
        print(post_id)
        print(comment_id)
        
        if LikesComment.objects.filter(author=user, comment=comment, post=post).exists():
            return JsonResponse({'message': 'Already liked', 'likes_count': comment.likes.count()})
        
        like = LikesComment(author=user, comment=comment, post=post)
        like.save()
        
        likes_count = comment.likes.count()
        
        return JsonResponse({'message': 'Liked', 'likes_count': likes_count})
    
    def get(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Invalid Request' }, status=400)



class CommentPostView(View):
    def post(self, request, post_id):
        user = request.user
        post = get_object_or_404(Blog, id=post_id)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            messages.error(request, "Invalid JSON")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Get the comment content
        comment_content = data.get('comment')  # Assuming 'comment' is the field name in your form
        if not comment_content:
            messages.error(request, "Missing required comment")
            return JsonResponse({'error': 'Missing required comment'}, status=400)
        
        # Get the parent comment ID, if any
        parent_id = data.get('parent')
        parent = None
        if parent_id:
            try:
                parent = Comment.objects.get(pk=parent_id)
            except Comment.DoesNotExist:
                messages.error(request, "Parent comment not found")
                return JsonResponse({'error': 'Parent comment not found'}, status=404)

        # Create the comment
        comment = Comment(author=user, post=post, comment=comment_content, parent=parent)
        comment.save()
        messages.success(request, "Comment created successfuly")
        
        response_data = {
            'success': True,
            'message': 'Comment Created',
            'comment_text': comment.comment,
            'comment_author': comment.author.username,
            'comment_date': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

        return JsonResponse(response_data, status=200)
    
    def get(self, request, *args, **kwargs):
        messages.error(request, "Invalid request")
        return JsonResponse({'error': 'Invalid Request' }, status=400)
        