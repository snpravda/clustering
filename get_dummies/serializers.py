from rest_framework import serializers
from .models import Csv


class CsvUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Csv
        fields = "__all__"