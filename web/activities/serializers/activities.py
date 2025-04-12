from rest_framework import serializers

from commons.serializers import MainModelSerializer
from activities.models import Activity, ActivityMedia


class ActivityMediaSerializer(MainModelSerializer):
    class Meta:
        model = ActivityMedia
        fields = (
            "pk",
            "file",
            "order",
            "created_at",
        )
        read_only_fields = ("pk", "order", "created_at")


class ActivitySerializer(MainModelSerializer):
    class Meta:
        model = Activity
        fields = (
            "pk",
            "name",
            "description",
            "media",
            "files",
            "location",
            "is_remote",
        )
        read_only_fields = ("pk",)
        current_user_field = "created_by"

    media = ActivityMediaSerializer(many=True, read_only=True)
    files = serializers.ListField(child=serializers.FileField(), write_only=True)

    def validate(self, data):
        location = self.get_current("location", data)
        is_remote = self.get_current("is_remote", data)
        if not is_remote and not location:
            raise serializers.ValidationError(
                {"location": "Required when `is_remote` is false."}
            )
        return super().validate(data)

    def validate_files(self, files):
        for file in files:
            serializer = ActivityMediaSerializer(data={"file": file})
            serializer.is_valid(raise_exception=True)

        max_length = 10
        if len(files) > max_length:
            raise serializers.ValidationError(
                f"You can upload up to {max_length} media files only."
            )
        return files

    def create(self, validated_data):
        files = validated_data.pop("files")

        model = self.Meta.model
        activity = model.objects.create(**validated_data)

        media = []
        for order, file in enumerate(files):
            obj = ActivityMedia(
                activity=activity,
                order=order,
                file=file,
            )
            media.append(obj)

        ActivityMedia.objects.bulk_create(media)
        return activity
