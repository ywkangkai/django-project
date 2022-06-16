from rest_framework import serializers
from .models import GitStatus



class RepositoryModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = GitStatus
        fields = '__all__'



