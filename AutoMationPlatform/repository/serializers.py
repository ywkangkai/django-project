from rest_framework import serializers
from .models import Repository
from gitstatus.models import GitStatus

class GitStatusModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitStatus
        fields = '__all__'

class RepositoryModelSerializer(serializers.ModelSerializer):

    respository_set = GitStatusModelSerializer(many=True, read_only=True)
    class Meta:
        model = Repository
        # fields = '__all__'
        fields = ('id', 'name', 'git', 'server', 'type', 'address', 'send', 'build', 'respository_set')



class RepositoryEditSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=50)
    git = serializers.CharField(max_length=500)
    server = serializers.CharField(max_length=200)
    type = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=500)
    send = serializers.BooleanField()
    build = serializers.CharField(max_length=5000)