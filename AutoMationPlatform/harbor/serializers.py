from rest_framework import serializers




class HarborSerializer(serializers.Serializer):

    id = serializers.CharField(max_length=100, read_only=True)

    name = serializers.CharField(max_length=100)







