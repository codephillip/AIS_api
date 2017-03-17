from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from myapp.models import Metric
from myapp.serializers import MetricSerializer


@api_view(['GET'])
def get_metrics(request):
    try:
        metrics = Metric.objects.all()
        print("metrics#")
        print(metrics)
    except Metric.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MetricSerializer(metrics, many=True)
        return Response({'metrics': serializer.data})