from django.db import models

class Price(models.Model):
    id = models.AutoField(primary_key=True)
    value_min = models.FloatField()
    value_max = models.FloatField()

    def __str__(self):
        return f"Price from {self.value_min} to {self.value_max}"

class Class(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    example_image = models.TextField()        # Base64-encoded image data
    extra_value = models.FloatField()
    description = models.TextField()
    price = models.ForeignKey(
        Price,
        on_delete=models.CASCADE,
        related_name='classes'
    )

    def __str__(self):
        return self.name

class HistoryPredictions(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.TextField()                # Base64-encoded image data
    total_min = models.FloatField()
    total_max = models.FloatField()
    timestamp = models.DateTimeField()        # DateTime field for timestamp

    def __str__(self):
        return f"HistoryPrediction {self.id} at {self.timestamp}"

class Predictions(models.Model):
    history_predictions = models.ForeignKey(
        HistoryPredictions,
        on_delete=models.CASCADE,
        related_name='predictions'
    )
    class_name = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='predictions'
    )

    def __str__(self):
        return f"Prediction for {self.class_name.name} in HistoryPrediction {self.history_predictions.id}"
