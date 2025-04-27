from rest_framework import serializers

import magic


class ContentTypeValidator:
    def __init__(self, *content_types):
        self.content_types = content_types

    def __call__(self, file):
        sample = file.read(2048)
        file.seek(0)

        mime_type = magic.from_buffer(sample, mime=True)

        if mime_type not in self.content_types:
            allowed_content_types = ", ".join(self.content_types)
            raise serializers.ValidationError(
                f"Passed file is not one of allowed content types: {allowed_content_types}"
            )

    def __eq__(self, other):
        return (
            isinstance(other, ContentTypeValidator)
            and self.content_types == other.content_types
        )


media_content_type_validator = ContentTypeValidator(
    "image/heic",
    "image/heif",
    "image/jpeg",
    "image/png",
    "video/mp4",
    "video/webm",
)
