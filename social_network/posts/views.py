from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment, Like, PostImage
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, PostImageSerializer

class PostListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all()

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            return Response({"ошибка": "Вы не можете редактировать..."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            return Response({"ошибка": "Выне можете это удалить..."}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()

class CommentListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        serializer.save(author=self.request.user, post_id=post_id)

class LikeCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def post(self, request, post_id):
        if Like.objects.filter(post=post_id, user=request.user).exists():
            return Response({"ошибка": "Вы уже поставили реакцию..."}, status=status.HTTP_400_BAD_REQUEST)
        Like.objects.create(post_id=post_id, user=request.user)
        return Response({"Уведомление": "Вы поставили реакцию :)"}, status=status.HTTP_201_CREATED)

class PostImageListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostImageSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return PostImage.objects.filter(post=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        serializer.save(post_id=post_id)