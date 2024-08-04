from django.shortcuts import render
from .serializers import TaskSerializer
from .models import Task
from rest_framework import generics, permissions  # New
...
class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    # Only an authenticated user can access this API endpoint
    permission_classes = [permissions.IsAuthenticated]
    # return Response(queryset.data)

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer