from rest_framework import generics
from .models import Price, Class, HistoryPredictions, Predictions
from .serializers import PriceSerializer, ClassSerializer, HistoryPredictionsSerializer, PredictionsSerializer

class PriceListCreate(generics.ListCreateAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer

class PriceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer

class ClassListCreate(generics.ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

class ClassDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

class HistoryPredictionsListCreate(generics.ListCreateAPIView):
    queryset = HistoryPredictions.objects.all()
    serializer_class = HistoryPredictionsSerializer

class HistoryPredictionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistoryPredictions.objects.all()
    serializer_class = HistoryPredictionsSerializer

class PredictionsListCreate(generics.ListCreateAPIView):
    queryset = Predictions.objects.all()
    serializer_class = PredictionsSerializer

class PredictionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Predictions.objects.all()
    serializer_class = PredictionsSerializer
