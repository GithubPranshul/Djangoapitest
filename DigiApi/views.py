from django.http import JsonResponse
from .models import Drinks
from .serializers import DrinkSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET", "POST"])
def drink_list(request):
    if request.method == "GET":
        drinks = Drinks.objects.all()
        serializer = DrinkSerializers(drinks, many=True)
        return JsonResponse({"drinks": serializer.data})

    if request.method == "POST":
        serializer = DrinkSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def drink_details(request, id):

    try:
        drink = Drinks.objects.get(pk=id)
    except Drinks.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = DrinkSerializers(drink)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = DrinkSerializers(drink, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        drink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
