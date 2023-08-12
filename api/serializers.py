from django.conf import settings
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from profiles.models import User
from posts.models import Post


class CustomPagination(PageNumberPagination):
    page_size = settings.TOTAL_POST_PAGE_API


class UserBaseSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_url(self, obj):
        return obj.get_api_url()


class UserListSerializer(UserBaseSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'full_name', 'image', 'url']


class PostListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'url', 'created']

    def get_url(self, obj):
        return obj.get_api_url()


class UserDetailSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'image', 'date_of_birth', 'city', 'posts']

    def get_posts(self, obj):
        posts = Post.objects.filter(user=obj)

        paginator = CustomPagination()
        paginated_posts = paginator.paginate_queryset(posts, self.context['request'])

        serializer = PostListSerializer(paginated_posts, many=True)
        return serializer.data


class UserPostDetailSerializer(UserBaseSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'url']


class PostDetailSerializer(serializers.ModelSerializer):
    user = UserPostDetailSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'user', 'content', 'created', 'updated']
