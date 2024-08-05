from django.contrib import admin
from .models import Price, Class, HistoryPredictions, Predictions

# Register the models with the Django admin site
admin.site.register(Price)
admin.site.register(Class)
admin.site.register(HistoryPredictions)
admin.site.register(Predictions)
