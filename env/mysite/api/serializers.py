from rest_framework import serializers
from .models import Price, Class, HistoryPredictions, Predictions

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('id', 'value_min', 'value_max')

class ClassSerializer(serializers.ModelSerializer):
    price = PriceSerializer()  # Nested PriceSerializer

    class Meta:
        model = Class
        fields = ('id', 'name', 'example_image', 'extra_value', 'description', 'price')

class HistoryPredictionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryPredictions
        fields = ('id', 'image', 'total_min', 'total_max', 'timestamp')

class PredictionsSerializer(serializers.ModelSerializer):
    history_predictions = HistoryPredictionsSerializer()  # Nested HistoryPredictionsSerializer
    class_name = ClassSerializer()  # Nested ClassSerializer

    class Meta:
        model = Predictions
        fields = ('id', 'history_predictions', 'class_name')
