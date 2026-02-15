import uuid
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

# Models & Serializers
from .models import Project, ProjectImage, Category, Feedback, User 
from .serializers import ProjectSerializer, FeedbackSerializer

# ------------------ HELPER FUNCTIONS ------------------
def is_admin_user(user):
    """Check if user is superuser, staff, or has admin role."""
    return user.is_superuser or user.is_staff or getattr(user, 'role', '').lower() == "admin"

# ------------------ PUBLIC GET VIEWS ------------------
@api_view(['GET'])
def projects_api(request):
    projects = Project.objects.all().order_by('-id') 
    serializer = ProjectSerializer(projects, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def project_detail_api(request, id):
    project = get_object_or_404(Project, id=id)
    serializer = ProjectSerializer(project, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def categories_list(request):
    categories = Category.objects.all()
    data = [{"id": c.id, "name": c.name} for c in categories]
    return Response(data)

# ------------------ FEEDBACK ACTIONS ------------------
@api_view(['GET', 'POST'])
def add_feedback_api(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'GET':
        feedbacks = Feedback.objects.filter(project=project).order_by('-date')
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)

    if not request.user.is_authenticated:
        return Response({"error": "Authentication required"}, status=401)

    message = request.data.get('message', '').strip()
    if not message:
        return Response({"error": "Message cannot be empty"}, status=400)

    Feedback.objects.create(project=project, user=request.user, message=message)
    return Response({"success": "Feedback submitted successfully"}, status=201)

# ------------------ ADMIN: ADD PROJECT (FAST VERSION) ------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_project_api(request):
    if not is_admin_user(request.user):
        return Response({"error": "Admin access required"}, status=403)
    
    try:
        data = request.data
        # Frontend ab 'image_urls' (List) bhej raha hai
        image_urls = data.get("image_urls", []) 
        contact=data.get("contact_number")
        # 1. Main Project Create karein
        project = Project.objects.create(
            title=data.get("title"),
            description=data.get("description"),
            plot_size=data.get("plot_size"),
            design_loc=data.get("design_loc"),
           
            contact_number=contact if contact else None,
            whatsapp_number=data.get("whatsapp_number"),
            design_type=data.get("design_type"),
            interior_or_exterior=data.get("interior_or_exterior"),
            # Pehla image main image ban jayega
            image=image_urls[0] if image_urls else None 
        )

        # 2. Categories handle karein
        category_ids = data.get("categories", [])
        if category_ids:
            project.categories.set(category_ids)

        # 3. Multiple Images (ProjectImage Model)
        for url in image_urls:
            ProjectImage.objects.create(project=project, image=url)

        return Response({"message": "Project created successfully", "id": project.id}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

# ------------------ ADMIN: UPDATE PROJECT ------------------
@api_view(['PATCH', 'POST'])
@permission_classes([IsAuthenticated])
def update_project_api(request, pk):
    if not is_admin_user(request.user):
        return Response({"error": "Admin access required"}, status=403)

    try:
        project = get_object_or_404(Project, pk=pk)
        data = request.data
        
        # Update fields
        project.title = data.get("title", project.title)
        project.description = data.get("description", project.description)
        project.plot_size = data.get("plot_size", project.plot_size)
        project.design_loc = data.get("design_loc", project.design_loc)
        project.contact_number = data.get("contact_number", project.contact_number)
        project.whatsapp_number = data.get("whatsapp_number", project.whatsapp_number)
        project.design_type = data.get("design_type", project.design_type)
        project.interior_or_exterior = data.get("interior_or_exterior", project.interior_or_exterior)
        
        # Agar nayi images aayi hain (Cloudinary URLs)
        new_image_urls = data.get("new_image_urls", [])
        if new_image_urls:
            if not project.image: # Agar pehle se main image nahi hai
                project.image = new_image_urls[0]
            for url in new_image_urls:
                ProjectImage.objects.create(project=project, image=url)
        
        project.save()

        # Categories update
        category_ids = data.get("categories")
        if category_ids is not None:
            project.categories.set(category_ids)

        return Response({"message": "Project updated successfully"})
    except Exception as e:
        return Response({"error": str(e)}, status=400)

# ------------------ ADMIN: DELETE ACTIONS ------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_project_api(request, pk):
    if not is_admin_user(request.user):
        return Response({"error": "Unauthorized"}, status=403)

    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return Response({"success": "Project deleted"}, status=200)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_feedback_api(request, pk):
    if not is_admin_user(request.user):
        return Response({"error": "Unauthorized"}, status=403)
    
    feedback = get_object_or_404(Feedback, pk=pk)
    feedback.delete()
    return Response({"success": "Feedback deleted"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_image_api(request, pk):
    if not is_admin_user(request.user):
        return Response({"error": "Unauthorized"}, status=403)
    
    img = get_object_or_404(ProjectImage, pk=pk)
    img.delete()
    return Response({"success": "Image removed"})

# ------------------ AUTHENTICATION ------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    role = request.data.get('role', 'user')

    if not username:
        return Response({"error": "Username is required"}, status=400)

    # Google Login logic: Check if email exists
    if email and User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key, 
            "username": user.username, 
            "role": getattr(user, 'role', 'user')
        }, status=200)

    if not password:
        password = str(uuid.uuid4())[:12]

    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email if email else "",
            role=role
        )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "username": user.username,
            "role": user.role
        }, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        user_role = "admin" if (user.is_superuser or user.is_staff) else getattr(user, 'role', 'user')
        return Response({
            "token": token.key,
            "username": user.username,
            "role": user_role
        })
    return Response({"error": "Invalid credentials"}, status=401)

@api_view(['POST'])
@permission_classes([AllowAny])
def google_check(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=400)
    try:
        user = User.objects.get(email=email)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'exists': True,
            'token': token.key,
            'username': user.username,
            'role': getattr(user, 'role', 'user')
        })
    except User.DoesNotExist:
        return Response({'exists': False})

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_api(request):
    email = request.data.get('email', '').strip()
    new_password = request.data.get('new_password')

    if not email or not new_password:
        return Response({"error": "Email and New Password are required"}, status=400)

    try:
        user = User.objects.get(email__iexact=email)
        user.set_password(new_password)
        user.save()
        return Response({"success": "Password updated successfully!"})
    except User.DoesNotExist:
        return Response({"error": "Email not found"}, status=404)