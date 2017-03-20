from rest_framework import serializers

from myapp.models import Crop, User, Metric, Feedback, Trigger


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = ('id', 'name', 'optimal_water_level', 'crop_type')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name', 'phoneNumber', 'password', 'address', 'crop')


class MetricSerializer(serializers.ModelSerializer):

    class Meta:
        model = Metric
        fields = ('id', 'water_volume', 'isIrrigating', 'user', 'time_stamp')


class TriggerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trigger
        fields = ('id', 'water_volume', 'duration', 'user', 'irrigation_time')


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ('id', 'title', 'content', 'time_stamp', 'user')
