from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import LSAProfile
from .serializers import LSASearchSerializer


class LSASearchView(APIView):
    def get(self, request):
        skill = request.query_params.get("skill", "").strip()

        queryset = (
            LSAProfile.objects
            .filter(is_active=True)
            .prefetch_related("skills")
            .distinct()
            .order_by("name")
        )

        if skill:
            queryset = queryset.filter(
                skills__name__iexact=skill
            )

        serializer = LSASearchSerializer(queryset, many=True)

        return Response(
            {
                "count": queryset.count(),
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )