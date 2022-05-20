from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer
from rest_framework.response import Response
from .models import Post


# class PublicPostListAPIView(generics.ListAPIView):
#     queryset = Post.objects.filter(is_public=True)
#     serializer_class = PostSerializer

# generic을 안쓰고 직접 APIView를 통해 생성
# class PublicPostListAPIView(APIView):
#     def get(self, request):
#         qs = Post.objects.filter(is_public=True)
#         serializer = PostSerializer(qs, many=True)
#         return Response(serializer.data)
#
#
# public_post_list = PublicPostListAPIView.as_view()

# 함수 기반 뷰를 사용하여
@api_view(['GET'])
def public_post_list(request):
    qs = Post.objects.filter(is_public=True)
    serializer = PostSerializer(qs, many=True)
    return Response(serializer.data)

class PostViewSet(ModelViewSet):  # 아래에 뷰 두 가지를 한 번에 지원해서 5개의 분기 모두 지원
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def dispatch(self, request, *args, **kwargs):  # 실제 요청이 올때마다 호출되는 함수
        print("request.body:", request.body)  # print 비추 logger 추천
        print("request.POST:", request.POST)
        return super().dispatch(request, *args, **kwargs)


# def post_list(requst):
#     # 2개 분기
#     pass
#
# def post_detail(request, pk):
#     # request, method => 3개 분기
#     pass

# @csrf_exempt
# def post_list(reuqest):
#     pass

# 파이썬에 장식자 문법, 리액트에서는 고차 컴포넌트(Higher Order Component)
# post_list = csrf_exempt(post_list)

class PostListAPIView(APIView):
    def get(self, request):
        qs = Post.objects.all()
        serializer = PostSerializer(qs, many=True)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PostDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
