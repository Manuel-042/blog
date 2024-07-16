from dataclasses import fields
from rest_framework import serializers
from .models import Blog, Category, Comment, CustomUser, Likes
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email"]

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
    required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
            {"password": "Password fields didn't match."})
        return attrs
        
    def create(self, validated_data):
        user = CustomUser(
            username = validated_data['username'],
            email = validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField()
    
    class Meta:
        model = Category
        exclude = ['id']
        
        
class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    reading_duration = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = '__all__'
        
    def get_reading_duration(self, object):
        return object.reading_duration()

        
        
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    post = BlogSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = '__all__'
        
class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'
        