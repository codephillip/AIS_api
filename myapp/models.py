from django.db import models


class Crop(models.Model):
    name = models.CharField(max_length=250)
    optimal_water_level = models.FloatField()
    crop_type = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=400)
    phoneNumber = models.IntegerField()
    password = models.CharField(max_length=40)
    address = models.CharField(max_length=250)
    crop = models.ForeignKey(Crop)

    def __str__(self):
        return self.name


class Metric(models.Model):
    water_volume = models.FloatField()
    isIrrigating = models.BooleanField()
    user = models.ForeignKey(User)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.water_volume)


class Trigger(models.Model):
    water_volume = models.FloatField()
    duration = models.CharField(max_length=10)
    user = models.ForeignKey(User)
    irrigation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.water_volume)


class Feedback(models.Model):
    title = models.TextField()
    content = models.TextField()
    user = models.ForeignKey(User)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
