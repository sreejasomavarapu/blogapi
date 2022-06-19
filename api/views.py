from email import message
#bfrom jmespath import search
from rest_framework import generics , viewsets
from rest_framework.response import Response
from . models import Post
from . serializers import PostSerializer, PostSerializerWithImage
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions, BasePermission, SAFE_METHODS, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.views import APIView        
from rest_framework.parsers import FormParser, MultiPartParser
# Create your views here.


    


# class PostListViewSet(viewsets.ViewSet):
#      queryset = Post.postobjects.all()
#      permission_classes =[DjangoModelPermissions]
#      def list(self, request):
#         queryset = Post.postobjects.all()
#         serializer = PostSerializer(queryset, many=True)
#         return Response(serializer.data)

#      def retrieve(self, request, pk=None):
#         queryset = Post.postobjects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = PostSerializer(user)
#         return Response(serializer.data)


        # def list(self, request):
        #     pass

        # def create(self, request):
        #     pass

        # def retrieve(self, request, pk=None):
        #     pass

        # def update(self, request, pk=None):
        #     pass

        # def partial_update(self, request, pk=None):
        #     pass

        # def destroy(self, request, pk=None):
        #     pass

class POstUserWritePermission(BasePermission):
    message= 'Editing posts is restricted to author only'
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            # Check permissions for read-only request
            return True
        else:
            # Check permissions for write request   
            return obj.author == request.user
            
# class PostListViewSet(viewsets.ModelViewSet):
#     permission_classes=[POstUserWritePermission]
#     serializer_class=PostSerializer
#     queryset = Post.postobjects.all()

#     def get_object(self,queryset=None,**kwargs):
#         item=self.kwargs.get('pk')
#         return get_object_or_404(Post,title=item)

        #return super().get_object()


class PostList(generics.ListCreateAPIView):
    permission_classes =[DjangoModelPermissions]
    #permission_classes =[IsAdminUser]
    queryset = Post.postobjects.all()
    serializer_class= PostSerializer

    def get_queryset(self):
        user = self.request.user
        # note that we are using objects not postobjects
        return Post.objects.filter(author=user) 

class PostDetail(generics.RetrieveUpdateAPIView, POstUserWritePermission): # or RetrieveUpdateDestroyAPIView
    permission_classes=[POstUserWritePermission]
    queryset=Post.objects.all()
    serializer_class=PostSerializer


class PostCreateImage(APIView):
    permission_classes=[IsAuthenticated]
    parser_classes=[MultiPartParser, FormParser]

    def post(self,request, format=None):
        print(request.data)
        serializer = PostSerializerWithImage(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListSearch(generics.ListCreateAPIView):

    queryset = Post.postobjects.all()
    serializer_class= PostSerializer
    filter_backends=[filters.SearchFilter]
    search_fields =['^title']
