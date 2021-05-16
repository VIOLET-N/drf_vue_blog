
from rest_framework import generics
# from rest_framework.permissions import IsAdminUser

from article.models import Article

# Create your views here.
from article.serializer import ArticleDetailSerializer
from article.serializer import ArticleListSerializer
from article.permissions import IsAdminUserOrReadOnly


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    """文章详情视图"""
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
