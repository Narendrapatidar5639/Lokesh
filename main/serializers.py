from rest_framework import serializers
from .models import Project, ProjectImage, Category, Feedback, User
from django.contrib.auth import authenticate

# 1. Project Image Serializer
class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image']

# 2. Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# 3. Feedback Serializer
class FeedbackSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'user_name', 'message', 'date']

# 4. Project Serializer
class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)
    category_names = serializers.SerializerMethodField()
    
    # ✅ Sirf Contact Number ko custom logic se handle karenge
    contact_number = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'categories', 'description', 
            'plot_size', 'design_loc', 'contact_number', 'whatsapp_number', 
            'interior_or_exterior', 'design_type', 'image', 
            'images', 'category_names'
        ]

    def get_category_names(self, obj):
        return [c.name for c in obj.categories.all()]

    # ✅ Fixed Contact Number Logic (Cleans '('',)' and empty data)
    def get_contact_number(self, obj):
        val = obj.contact_number
        
        # Agar data tuple format mein hai ('...',), toh string nikaalo
        if isinstance(val, (list, tuple)):
            val = val[0] if val else ""
        
        # String mein convert karke check karo ki valid hai ya nahi
        clean_val = str(val).strip()
        
        if clean_val and clean_val != "('',)" and clean_val != "None":
            return clean_val
            
        # Agar database khali hai ya kachra hai, toh ye fixed number jayega
        return "+919109231207" # <--- Apna No. yahan daalein

# 5. User Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']