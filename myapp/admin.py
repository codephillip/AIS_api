from django.contrib import admin
from myapp.models import Crop, User, Metric, Feedback, Trigger

admin.site.register(Crop)
admin.site.register(User)
admin.site.register(Metric)
admin.site.register(Trigger)
admin.site.register(Feedback)
