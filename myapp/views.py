from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from myapp.models import Metric, User, Feedback, Trigger, Crop
from myapp.serializers import MetricSerializer, UserSerializer, FeedbackSerializer, TriggerSerializer, CropSerializer

import urllib.request
import uuid
import csv
import json
from django.contrib.staticfiles.templatetags.staticfiles import static

import pandas as pd
from sklearn import metrics
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC

percentage = 0.0
final_classifier = 1


def classifier1(X_train, X_test, y_train, y_test):
    global percentage
    global final_classifier
    print("LogisticRegression")
    # accuracy evaluation
    classifier = LogisticRegression()
    # fit the model to the training data (learn the coefficients)
    classifier.fit(X_train, y_train)
    # make predictions on the testing set
    y_pred = classifier.predict(X_test)
    print("y_test")
    print(y_test)
    print("y_pred")
    print(y_pred)
    temp_percentage = metrics.accuracy_score(y_test, y_pred)
    if temp_percentage > percentage:
        percentage = temp_percentage
        final_classifier = 1
    print("percentage: " + str(temp_percentage))
    return classifier


def classifier2(X_train, X_test, y_train, y_test):
    global percentage
    global final_classifier
    print("LinearSVC")
    # accuracy evaluation
    classifier = LinearSVC()
    # fit the model to the training data (learn the coefficients)
    classifier.fit(X_train, y_train)
    # make predictions on the testing set
    y_pred = classifier.predict(X_test)
    print("y_test")
    print(y_test)
    print("y_pred")
    print(y_pred)
    temp_percentage = metrics.accuracy_score(y_test, y_pred)
    if temp_percentage > percentage:
        percentage = temp_percentage
        final_classifier = 2
    print("percentage: " + str(temp_percentage))
    return classifier


def classifier3(X_train, X_test, y_train, y_test):
    global percentage
    global final_classifier
    print("RandomForestClassifier")
    # accuracy evaluation
    classifier = RandomForestClassifier(n_estimators=3, max_depth=2)
    # fit the model to the training data (learn the coefficients)
    classifier.fit(X_train, y_train)
    # make predictions on the testing set
    y_pred = classifier.predict(X_test)
    print("y_test")
    print(y_test)
    print("y_pred")
    print(y_pred)
    temp_percentage = metrics.accuracy_score(y_test, y_pred)
    if temp_percentage > percentage:
        percentage = temp_percentage
        final_classifier = 3
    print("percentage: " + str(temp_percentage))
    return classifier


def classifier4(X_train, X_test, y_train, y_test):
    global percentage
    global final_classifier
    print("KNeighborsClassifier")
    # accuracy evaluation
    classifier = KNeighborsClassifier(n_neighbors=1)
    # fit the model to the training data (learn the coefficients)
    classifier.fit(X_train, y_train)
    # make predictions on the testing set
    y_pred = classifier.predict(X_test)
    print("y_test")
    print(y_test)
    print("y_pred")
    print(y_pred)
    # compare the predicted values-y_pred, with the actual values-y_test
    temp_percentage = metrics.accuracy_score(y_test, y_pred)
    if temp_percentage > percentage:
        percentage = temp_percentage
        final_classifier = 4
    print("percentage: " + str(temp_percentage))
    return classifier


def get_byte():
    if int(str(uuid.uuid4().get_time())[0:3]) > 500:
        return 0
    else:
        return 1


def initialise():
    url = static('test.csv')
    csv_connection = open(url, "wb")
    f = csv.writer(csv_connection)
    # smv = soil moisture value. comes from the smv sensor on the hardware
    f.writerow(["pk", "dt", "name", "temp", "humidity", "smv", "trigger"])

    # production url
    # url = "http://api.openweathermap.org" + "/data/2.5/forecast?id=" + str(
    #     232422) + "&mode=json&units=metric&cnt=7&appid=1f846e7a0e00cf8c2f96dd5e768580fb"
    # development url
    url = "http://127.0.0.1:8080/weather1.json"
    print(url)
    # 'load'-for json document, 'loads'-for json string
    x = json.load(urllib.request.urlopen(url))
    print(x)
    city = x.get('city')

    count = 0
    for list_data in x.get('list'):
        f.writerow([count + 1, list_data["dt_txt"],
                    city["name"], list_data["main"]["temp"], list_data["main"]["humidity"],
                    str(uuid.uuid4().get_node())[0:3],
                    get_byte()])
        count += 1
    csv_connection.close()

    csv_url = "test.csv"
    data = pd.read_csv(csv_url, index_col=0)
    feature_cols = ['temp', 'humidity', 'smv']

    print("ACTUAL DATA")
    print(data)

    X = data[feature_cols]
    print(X.head())
    print(type(X))
    print(X.shape)

    y = data['trigger']
    print(y.head())
    print(type(y))
    print(y.shape)

    # MACHINE LEARNING
    # split the data into training and testing data
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    # default split is 75% for training and 25% for testing
    print("train test split shapes")
    print(X_train.shape)
    print(y_train.shape)
    print(X_test.shape)
    print(y_test.shape)

    # run all classifier to determine the best
    print("running classifier1")
    classifier_model1 = classifier1(X_train, X_test, y_train, y_test)
    print("running classifier2")
    classifier_model2 = classifier2(X_train, X_test, y_train, y_test)
    print("running classifier3")
    classifier_model3 = classifier3(X_train, X_test, y_train, y_test)
    print("running classifier4")
    classifier_model4 = classifier4(X_train, X_test, y_train, y_test)

    # rerun the best on the data
    csv_connection = open("test.csv", "wb")
    f = csv.writer(csv_connection)
    # smv = soil moisture value. comes from the smv sensor on the hardware
    f.writerow(["pk", "dt", "name", "temp", "humidity", "smv", "trigger"])

    # todo capture new data
    # production url
    url = "http://api.openweathermap.org" + "/data/2.5/forecast?id=" + str(
        232422) + "&mode=json&units=metric&cnt=21&appid=1f846e7a0e00cf8c2f96dd5e768580fb"
    # development url
    # url = "http://127.0.0.1:8080/weather1.json"
    print(url)
    # 'load'-for json document, 'loads'-for json string
    x = json.load(urllib.request.urlopen(url))
    print(x)
    city = x.get('city')

    count = 1
    for list_data in x.get('list'):
        f.writerow([count, list_data["dt_txt"],
                    city["name"], list_data["main"]["temp"], list_data["main"]["humidity"],
                    str(uuid.uuid4().get_node())[0:3],
                    0])
        count += 1
    csv_connection.close()

    # csv_url = "http://127.0.0.1:8080/weather.csv"
    # todo point to a global source for the csv file
    csv_url = "test.csv"
    data = pd.read_csv(csv_url, index_col=0)
    feature_cols = ['temp', 'humidity', 'smv']

    print("ACTUAL DATA")
    print(data)

    X = data[feature_cols]
    print(X.head())
    print(type(X))
    print(X.shape)

    # choose best model and predict
    if final_classifier == 1:
        y = classifier_model1.predict(X)
        print("FINAL PREDICTION: model1")
        print(y)
    elif final_classifier == 2:
        y = classifier_model2.predict(X)
        print("FINAL PREDICTION: model2")
        print(y)
    elif final_classifier == 3:
        y = classifier_model3.predict(X)
        print("FINAL PREDICTION: model3")
        print(y)
    elif final_classifier == 4:
        y = classifier_model4.predict(X)
        print("FINAL PREDICTION: model4")
        print(y)

    # save the triggers
    csv_connection = open("test.csv", "wb")
    f = csv.writer(csv_connection)
    print("saving data...")
    count = 1
    for list_data in x.get('list'):
        f.writerow([count, list_data["dt_txt"],
                    city["name"], list_data["main"]["temp"], list_data["main"]["humidity"],
                    str(uuid.uuid4().get_node())[0:3],
                    y[count - 1]])
        count += 1
    csv_connection.close()


@api_view(['GET', 'POST'])
def metrics_route(request):
    return master_route(request, 'metrics', Metric, MetricSerializer)


@api_view(['GET'])
def metrics_post(request, pk, irri):
    print("metrics_post data")
    print(pk)

    metric = Metric(user=User.objects.get(id=1), water_volume=pk, isIrrigating=irri)
    metric.save()
    print(metric)
    return master_route(request, 'metrics', Metric, MetricSerializer)


@api_view(['GET', 'POST'])
def feedbacks_route(request):
    return master_route(request, 'feedbacks', Feedback, FeedbackSerializer)


@api_view(['GET', 'POST', 'PUT'])
def triggers_route(request):
    return master_route(request, 'triggers', Trigger, TriggerSerializer)


@api_view(['GET', 'POST', 'PUT'])
def start_learning(request):
    if request.method == 'GET':
        initialise()
    return master_route(request, 'triggers', Trigger, TriggerSerializer)


@api_view(['GET', 'POST'])
def crops_route(request):
    return master_route(request, 'crops', Crop, CropSerializer)


@api_view(['GET', 'POST', 'PUT'])
def users_route(request):
    if request.method == 'PUT':
        error_response = Response({"status": "Failed to login user"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            users = User.objects.filter(phoneNumber=request.data['phoneNumber'])
            if users is not None and users[0].password == request.data['password']:
                return Response({"users": UserSerializer(users, many=True).data}, status=status.HTTP_202_ACCEPTED)
            else:
                return error_response
        except Exception:
            return error_response
    # handles user sign-up and get all users
    return master_route(request, 'users', User, UserSerializer)


@api_view(['PUT'])
def user_update(request, pk):
    if request.method == 'PUT':
        # only updates crop
        try:
            User.objects.filter(id=pk).update(crop=request.data['crop'])
            return Response({"status": "Successfully updated user information"}, status=status.HTTP_201_CREATED)
        except Exception:
            return Response({"status": "Failed updated user information"}, status=status.HTTP_404_NOT_FOUND)


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
