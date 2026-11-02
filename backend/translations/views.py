from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .data import SUPPORTED_LANGUAGES
from .models import Translation


class TranslationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        language = request.query_params.get("lang", "ru")

        if language not in SUPPORTED_LANGUAGES:
            language = "ru"

        rows = (
            Translation.objects
            .filter(is_active=True)
            .values("key", language)
            .order_by("key")
        )

        translations = {}

        for row in rows:
            value = row.get(language, "")

            if value:
                translations[row["key"]] = value

        return Response({
            "language": language,
            "translations": translations,
        })
