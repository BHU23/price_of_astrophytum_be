from django.utils import timezone
from rest_framework import generics, serializers
from rest_framework.response import Response
from .models import HistoryPredictions, Predictions, Class, Price
from .serializers import PriceSerializer, ClassSerializer, HistoryPredictionsSerializer, PredictionsSerializer
from .utils import process_image
import logging

logger = logging.getLogger('mylogger')

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

    def perform_create(self, serializer):
        logger.info("perform_create called")
        image = self.request.data.get('image')
        if not image:
            raise serializers.ValidationError({"image": "This field is required."})
        
        # logger.info(image)
        predictions = self.process_image(image)
        logger.info(f"Predictions: {predictions}")
        total_min = 0
        total_max = 0
        if predictions:
            total_min, total_max = self.calculate_total_price(predictions)

        history_prediction = serializer.save(
            total_min=total_min,
            total_max=total_max,
            timestamp=timezone.now()
        )
        if predictions:
            self.create_predictions(predictions, history_prediction)

    def process_image(self, image_data):
      
        return process_image(image_data)
        # return [1]
    
    def calculate_total_price(self, class_ids):
        total_min = 0
        total_max = 0
        for class_id in class_ids:
            try:
                class_obj = Class.objects.get(id=class_id)
                price = class_obj.price
                total_min += price.value_min
                total_max += price.value_max
            except Class.DoesNotExist:
                logger.warning(f"Class not found for class_id: {class_id}")
                continue
        return total_min, total_max

    def create_predictions(self, class_ids, history_prediction):
        for class_id in class_ids:
            try:
                class_obj = Class.objects.get(id=class_id)
                Predictions.objects.create(
                    history_predictions=history_prediction,
                    class_name=class_obj
                )
            except Class.DoesNotExist:
                logger.warning(f"Class not found for class_id: {class_id}")
                continue

class HistoryPredictionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistoryPredictions.objects.all()
    serializer_class = HistoryPredictionsSerializer

class PredictionsListCreate(generics.ListCreateAPIView):
    queryset = Predictions.objects.all()
    serializer_class = PredictionsSerializer

class PredictionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Predictions.objects.all()
    serializer_class = PredictionsSerializer
