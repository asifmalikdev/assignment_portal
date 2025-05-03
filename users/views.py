
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({'message': f'Hello {request.user.username}, you are authenticated!'})


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({
                'message': 'user created successfully',
                'access_token': access_token,
                'refresh_token': str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'details':'username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'message': 'Login Successfull',
            'access_token':access_token,
            'refresh_token':str(refresh)
        }, status= status.HTTP_200_OK)
    return Response({'detail': 'invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def teacher_only_view(request):
    if request.user.role != 'teacher':
        return Response({'error': 'only teacher can access this'}, status=status.HTTP_403_FORBIDDEN)
    return Response({'message': f'wellcome Teacher {request.user.username}!'})

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def student_only_view(request):
    if request.user.role != 'student':
        return Response({'error':'only student can access'}, status=status.HTTP_403_FORBIDDEN)
    return Response({'message':f'wellcome students {request.user.username}!'})



from .models import UserProfile, TeacherProfile, StudentProfile
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)

    if profile.role == 'admin':
        return Response({"message": f"Welcome Admin {user.username}. You can manage the platform."})

    elif profile.role == 'teacher':
        teacher = TeacherProfile.objects.get(user=user)
        return Response({
            "message": f"Welcome Teacher {user.username}",
            "school": teacher.school.name if teacher.school else None,
            "subjects": [sub.name for sub in teacher.subjects.all()],
            "classes": [cls.name for cls in teacher.classes.all()]
        })

    elif profile.role == 'student':
        student = StudentProfile.objects.get(user=user)
        return Response({
            "message": f"Welcome Student {user.username}",
            "class": student.classroom.name if student.classroom else None
        })

    return Response({"message": "Role not recognized"})




