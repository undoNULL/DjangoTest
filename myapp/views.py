#from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

from myapp.models import PostModel, User
from myapp.service import create_account, account_compare, create_post, get_all_post, get_post_by_id, get_post_by_title

#def hello(request):
#    return JsonResponse({"msg":"world"})

def hello(request):
    version = request.GET.get('v', 'world')
    return JsonResponse({"msg": version})



class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' #['id', 'pw', 'name']

class UserSerializer(serializers.Serializer):
    id = serializers.CharField()
    pw = serializers.CharField()
    name = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    id = serializers.CharField()
    pw = serializers.CharField()

class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            #user = User.objects.create(id=serializer.data['id'], pw=serializer.data['pw'])
            user = create_account(serializer.data['id'], serializer.data['pw'])
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK, data=UserSerializer(user).data)
    
    
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = account_compare(serializer.data['id'], serializer.data['pw'])
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK, data=UserSerializer(user).data)
        
class SetNameAPIView(APIView):
    class SetNameSerializer(UserSerializer):
        name = serializers.CharField(allow_blank=True)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            #user = User.objects.get(id=serializer.data['id'], pw=serializer.data['pw'])
            user = account_compare(serializer.data['id'], serializer.data['pw'])
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.name = serializer.data['name']
        user.save()
        return Response(status=status.HTTP_200_OK, data=self.SetNameSerializer(user).data)
    

class PostSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    title = serializers.CharField()
    author_id = serializers.CharField()
    content = serializers.CharField()


class CreatePostAPIView(APIView):
    class CreatePostSerializer(serializers.Serializer):
        title = serializers.CharField()
        id = serializers.CharField()
        content = serializers.CharField()

    def post(self, request):
        serializer = self.CreatePostSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            post = create_post(serializer.data['title'], serializer.data['id'], serializer.data['content'])
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK, data=PostSerializer(post).data)
    

"""
class GetAllPostAPIView(APIView):
    class InitPostSerializer(serializers.Serializer):
        id = serializers.CharField()

    def post(self, request):
        serializer = self.InitPostSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            posts = get_all_post()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK, data=PostSerializer(posts).data)   
"""

class GetAllPostAPIView(APIView):
    def post(self, request):
        try:
            posts = get_all_post()
            post_list = PostSerializer(posts, many=True).data
            return Response(
                status=status.HTTP_200_OK,
                data={"post_list": post_list}
            )
        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": str(e)}
            )
        

class GetPostByTitleAPIView(APIView):
    class TitleFilterSerializer(serializers.Serializer):
        title = serializers.CharField()

    def post(self, request):
        serializer = self.TitleFilterSerializer(data=request.data)
        
        # 요청 데이터가 유효하지 않으면 400 응답
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Invalid request data"}
            )

        try:
            title = serializer.validated_data["title"]
            posts = get_post_by_title(title)

            # 검색 결과가 없는 경우
            if not posts.exists():
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data={"error": "No posts found with the given title"}
                )

            # 검색 결과 반환
            post_list = PostSerializer(posts, many=True).data
            return Response(
                status=status.HTTP_200_OK,
                data={"post_list": post_list}
            )
        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": str(e)}
            )
        
class GetPostByIdAPIView(APIView):
    class IdFilterSerializer(serializers.Serializer):
        id = serializers.CharField()

    def post(self, request):
        serializer = self.IdFilterSerializer(data=request.data)
        
        # 요청 데이터가 유효하지 않으면 400 응답
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Invalid request data"}
            )

        try:
            id = serializer.validated_data["id"]
            posts = get_post_by_id(id)

            # 검색 결과가 없는 경우
            if not posts.exists():
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data={"error": "No posts found with the given id"}
                )

            # 검색 결과 반환
            post_list = PostSerializer(posts, many=True).data
            return Response(
                status=status.HTTP_200_OK,
                data={"post_list": post_list}
            )
        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": str(e)}
            )