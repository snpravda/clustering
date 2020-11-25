from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import status, parsers, renderers
from .serializers import *
from rest_framework.response import Response
from clustering.settings import REST_FRAMEWORK

import pandas as pd

# Create your views here.

class GetuDummies(GenericAPIView):
    '''post .csv file with string columns
    and if in column is less than 11 string categorical variables (they can repeat)
    it will convert it tinto dummy/indicator variables'''

    parser_classes = ( parsers.FormParser, parsers.MultiPartParser) #parsers.JSONParser)
    #renderer_classes = (renderers.JSONRenderer,)
    serializer_class = CsvUploadSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            file = serializer.save()
            df = pd.read_csv(file.csv.path)
            return  Response({'result': 'ok' }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'result': 'ERROR' + str(e)}, status=status.HTTP_400_BAD_REQUEST)

