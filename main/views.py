from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Project, ProjectImage, Category, Feedback, User
from .serializers import ProjectSerializer


# ------------------ GET ALL PROJECTS ------------------
@api_view(['GET'])
def projects_api(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True, context={'request': request})
    return Response(serializer.data)


# ------------------ GET PROJECT DETAIL ------------------
@api_view(['GET'])
def project_detail_api(request, id):
    project = get_object_or_404(Project, id=id)
    serializer = ProjectSerializer(project, context={'request': request})
    return Response(serializer.data)


# ------------------ GET CATEGORIES ------------------
@api_view(['GET'])
def categories_list(request):
    categories = Category.objects.all()
    data = [{"id": c.id, "name": c.name} for c in categories]
    return Response(data)


# ------------------ ADD FEEDBACK ------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_feedback_api(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    message = request.data.get('message', '').strip()

    if not message:
        return Response({"error": "Message cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

    Feedback.objects.create(
        project=project,
        user=request.user,
        message=message
    )

    return Response({"success": "Feedback submitted successfully!"})


# ------------------ ADD PROJECT (ADMIN) ------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_project_api(request):
    if request.user.role != "admin":
        return Response({"error": "Only admin can add project"}, status=status.HTTP_403_FORBIDDEN)

    data = request.data
    category = get_object_or_404(Category, id=data.get("category"))

    project = Project.objects.create(
        title=data.get("title"),
        description=data.get("description"),
        category=category,
        design_type=data.get("design_type"),
        interior_or_exterior=data.get("interior_or_exterior"),
        plot_size=data.get("plot_size"),
        contact_number=data.get("contact_number"),
        whatsapp_number=data.get("whatsapp_number"),
        image=request.FILES.get("image")
    )

    images = request.FILES.getlist("images")
    for img in images:
        ProjectImage.objects.create(project=project, image=img)

    serializer = ProjectSerializer(project, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# ------------------ DELETE PROJECT (ADMIN) ------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_project_api(request, pk):
    if request.user.role != "admin":
        return Response({"error": "Only admin can delete project"}, status=status.HTTP_403_FORBIDDEN)

    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return Response({"success": "Project deleted"})


# ------------------ REGISTER ------------------
@api_view(['POST'])
def register_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    role = request.data.get('role')

    if not username or not password or not role:
        return Response({"error": "All fields required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    User.objects.create_user(
        username=username,
        password=password,
        role=role
    )

    return Response({"message": "User created successfully"})


# ------------------ LOGIN ------------------
@api_view(['POST'])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "message": "Login success",
            "token": token.key,
            "username": user.username,
            "role": user.role
        })
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
