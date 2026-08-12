from rest_framework import serializers

from .models import LSAProfile


class LSASearchSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()

    class Meta:
        model = LSAProfile
        fields = ["id", "name", "email", "skills"]

    def get_skills(self, obj):
        return [skill.name for skill in obj.skills.all()]