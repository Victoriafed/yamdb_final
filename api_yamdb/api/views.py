from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TittleFilter
from .mixins import CustomMixinSet
from .permissions import (AdminSuperUserPermission,
                          IsAdminModeratorOwnerOrReadOnly, OnlyAdmin)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          SignupUserSerializer, SimpleUser,
                          TitleModifySerializer, TitleReadSerializer,
                          TokenSerializer, UsersSerializer)
from .utils import send_email


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, OnlyAdmin]
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method in (
                "PATCH", "POST") and self.request.user.is_admin:
            return UsersSerializer
        return SimpleUser

    @action(
        detail=False, methods=('get', 'patch', 'post',),
        url_path='me', url_name='me',
        permission_classes=[permissions.IsAuthenticated]
    )
    def get_user_me(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class GenreViewSet(CustomMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminSuperUserPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CustomMixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminSuperUserPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    )
    permission_classes = (AdminSuperUserPermission,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TittleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleReadSerializer
        return TitleModifySerializer


class APIToken(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        token = RefreshToken.for_user(user).access_token
        return Response(
            {'token': str(token)},
            status=status.HTTP_201_CREATED
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup_with_email(request):
    if request.method == 'POST':
        serializer = SignupUserSerializer(data=request.data)
        if request.user.is_authenticated and serializer.is_valid():
            user = User.objects.get_or_create(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email']
            )
            return Response(serializer.data)
        if serializer.is_valid():
            user = serializer.save()
            send_email(user)
            return Response(serializer.data)
        try:
            user = User.objects.get(
                username=request.data.get('username'),
                email=request.data.get('email')
            )
            send_email(user)
        except User.DoesNotExist:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
