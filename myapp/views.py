from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from myapp.models import Metric, User, Feedback
from myapp.serializers import MetricSerializer, UserSerializer, FeedbackSerializer


@api_view(['GET', 'POST'])
def metrics_route(request):
    return master_route(request, 'metrics', Metric, MetricSerializer)


@api_view(['GET', 'POST'])
def feedbacks_route(request):
    return master_route(request, 'feedbacks', Feedback, FeedbackSerializer)


def master_route(request, tableName, Table, TableSerializer):
    try:
        tables = Table.objects.all()
    except Table.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        return Response({tableName: TableSerializer(tables, many=True).data})

    if request.method == 'POST':
        print("posting#")
        print(request.data)
        serializer = TableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
