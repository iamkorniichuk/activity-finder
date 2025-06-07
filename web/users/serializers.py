from commons.serializers import serializers
from commons.serializers.fields import WebsiteLinksField

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "image",
            "display_name",
            "description",
            "birth_date",
            "website_links",
        )
        read_only_fields = ("pk",)

    website_links = WebsiteLinksField(allow_empty=True, required=False)
