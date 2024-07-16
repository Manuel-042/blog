from .serializers import LikesSerializer, UserSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from . models import CustomUser, Blog, Category, Comment, Likes
from . serializers import BlogSerializer, CategorySerializer, CommentSerializer, UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import mixins, generics

from account import serializers


# Create your views here.
@api_view(['GET'])
def read_user(request,pk):
    if request.method == 'GET':
        user = CustomUser.objects.get(id=pk)
        serializer = UserSerializer(user)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST',])
def register(request):
    if request.method == "POST":
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST',])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = None
        
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass
            
        if not user:
            user = authenticate(username=username, password=password)
            
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        
    return Response({'Error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class BlogListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        all_blogs = Blog.objects.all()
        serializer = BlogSerializer(all_blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = BlogSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
        
class SingleUserBlogsListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        blogs = Blog.objects.filter(author=pk)
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SingleUserBlogLikesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        author_id = CustomUser.objects.get(id=pk)
        
        likes = Likes.objects.filter(author=author_id)
        serializer = LikesSerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class SingleBlogDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        blog = Blog.objects.get(id=pk)
        serializer = BlogSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        blog = Blog.objects.get(id=pk)
        serializer = BlogSerializer(blog, data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        blog = Blog.objects.get(id=pk)
        blog.delete()
        
        return Response(status=status.HTTP_200_OK) 
    

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        #pk = post_id
        user = request.user
        try:
            post = Blog.objects.get(id=pk)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog Post not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the like already exists
        if Likes.objects.filter(author=user, post=post).exists():
            return Response({'message': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the like
        like = Likes(author=user, post=post)
        like.save()
        
        serializer = LikesSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        #pk = post_id
        user = request.user
        try:
            post = Blog.objects.get(id=pk)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog Post not found'}, status=status.HTTP_404_NOT_FOUND)

        
        # Create the comment
        comment = request.data.get('comment')  # Assuming 'content' is the comment field name
        if not comment:
            return Response({'error': 'Missing required comment'}, status=status.HTTP_400_BAD_REQUEST)
        
        parent_id = request.data.get('parent')
        if parent_id:
            try:
                parent = Comment.objects.get(pk=parent_id)
            except Comment.DoesNotExist:
                return Response({'error': 'Parent comment not found'}, status=status.HTTP_404_NOT_FOUND)
            
        if not parent:
            parent = None
    
        comment = Comment(author=user, post=post, comment=comment, parent=parent)
        comment.save()
        
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        