from rest_framework import serializers

from myapp.models import Crop, User, Metric, Feedback


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = ('id', 'name', 'optimal_water_level', 'crop_type')


class UserSerializer(serializers.ModelSerializer):
    crop = CropSerializer()

    class Meta:
        model = User
        fields = ('id', 'name', 'phoneNumber', 'address', 'crop')


class MetricSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Metric
        fields = ('id', 'water_volume', 'isIrrigating', 'user', 'time_stamp')


class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Feedback
        fields = ('id', 'title', 'content', 'time_stamp', 'user')
