from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import status, parsers, renderers
from .serializers import *
from rest_framework.response import Response
from .models import Csv
from clustering.settings import MEDIA_ROOT
import os

import pandas as pd


def get_dummies(df):
    '''returns df with dummy variables if
    df has str columns with unique values < 11'''
    str_cols = []
    for index, value in df.dtypes.items():
        if value in (object, str):
            str_cols.append(index)

    for index in str_cols:
        if len(df[f"{index}"].unique()) < 11:  # this value can be adjusted
            try:
                df = pd.get_dummies(data=df, columns=[f"{index}"])

            except:
                pass
    return df

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
            df = get_dummies(df)
            df.to_csv(os.path.join(MEDIA_ROOT, 'modified.csv'), index=False)
            modified = Csv.objects.create(csv='modified.csv')
            # serialized = serializer(data = 'modified.csv')

            return Response({"file": b"".join(modified.csv).decode("utf-8")}, status=status.HTTP_200_OK)
            #return Response({'result': 'ok' }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'result': 'ERROR ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)

