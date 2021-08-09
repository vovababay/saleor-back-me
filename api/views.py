from django.core.exceptions import ValidationError
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import *
@api_view(['GET', 'POST'])
def payment_url(request):
    if request.method == 'POST':
        
        if "amount" not in request.data:
            return Response({"required field": "amount"}, status=status.HTTP_400_BAD_REQUEST)
        if ("email" not in request.data) and ("phone" not in request.data):
            return Response({"required fields": "email or phone"}, status=status.HTTP_400_BAD_REQUEST)
        if "products" not in request.data:
            return Response({"required field": "products"}, status=status.HTTP_400_BAD_REQUEST)
        if "description" not in request.data:
            return Response({"required field": "description"}, status=status.HTTP_400_BAD_REQUEST)
        for product in request.data["products"]:
            if "name" not in product:
                return Response({"one of the products is missing a ": "name"}, status=status.HTTP_400_BAD_REQUEST)
            if "quantity" not in product:
                return Response({"one of the products is missing a": "quantity"}, status=status.HTTP_400_BAD_REQUEST)
            if "amount" not in product:
                return Response({"one of the products is missing a": "amount"}, status=status.HTTP_400_BAD_REQUEST)
            
        print(create_hash_token(request.data))
        return Response({"111": "222"}, status=status.HTTP_200_OK)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    
#Email
#Phone
#OrderId 
#
#
