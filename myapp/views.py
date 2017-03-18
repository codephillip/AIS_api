from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from myapp.models import Metric, User
from myapp.serializers import MetricSerializer, UserSerializer


@api_view(['GET', 'POST'])
def metrics_route(request):
    try:
        metrics = Metric.objects.all()
        print("metrics#")
        print(metrics)
    except Metric.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MetricSerializer(metrics, many=True)
        return Response({'metrics': get_metrics(metrics).data})

    if request.method == 'POST':
        save_metric(request)


def get_metrics(metrics):
    serializer = MetricSerializer(metrics, many=True)
    return serializer


@api_view(['POST'])
def save_metric(request):
    print("posting#")
    # checking sent data directly from request
    print(request.data)
    # print(request.data['content'])
    try:
        user = User.objects.get(id=request.data['user_id'])
        print(user)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    request.data['user'] = request.data['user_id']
    print(request.data)
    serializer = MetricSerializer(data=request.data)
    if serializer.is_valid():
        # checking sent data after serialization
        # print(serializer.validated_data['title'])
        print("Is valid")
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
