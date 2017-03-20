from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from myapp.models import Metric, User, Feedback, Trigger, Crop
from myapp.serializers import MetricSerializer, UserSerializer, FeedbackSerializer, TriggerSerializer, CropSerializer


@api_view(['GET', 'POST'])
def metrics_route(request):
    return master_route(request, 'metrics', Metric, MetricSerializer)


@api_view(['GET', 'POST'])
def feedbacks_route(request):
    return master_route(request, 'feedbacks', Feedback, FeedbackSerializer)


@api_view(['GET', 'POST'])
def triggers_route(request):
    return master_route(request, 'triggers', Trigger, TriggerSerializer)


@api_view(['GET', 'POST'])
def crops_route(request):
    return master_route(request, 'crops', Crop, CropSerializer)


@api_view(['GET', 'POST'])
def users_route(request):
    # handles user sign-up and get all users
    return master_route(request, 'users', User, UserSerializer)


@api_view(['POST', 'PUT'])
def user_login(request, pk):

    if request.method == 'PUT':
        # only updates crop
        try:
            User.objects.filter(id=pk).update(crop=request.data['crop'])
            return Response({"status": "Successfully updated user information"}, status=status.HTTP_201_CREATED)
        except Exception:
            return Response({"status": "Failed updated user information"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        error_response = Response({"status": "Failed to login user"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            users = User.objects.filter(id=pk, phoneNumber=request.data['phoneNumber'])
            if users is not None and users[0].password == request.data['password']:
                return Response({"status": "Successfully logged in user"}, status=status.HTTP_202_ACCEPTED)
            else:
                return error_response
        except Exception:
            return error_response


def master_route(request, tableName, Table, TableSerializer):
    try:
        tables = Table.objects.all()
    except Table.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        return Response({tableName: TableSerializer(tables, many=True).data})

    if request.method == 'POST':
        serializer = TableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
