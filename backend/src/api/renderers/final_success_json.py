from typing import Any

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from api.responses import build_success_payload


class FinalSuccessJSONRenderer(JSONRenderer):
    def render(
        self,
        data: Any,
        accepted_media_type: str | None = None,
        renderer_context: dict[str, Any] | None = None,
    ) -> bytes:
        response: Response | None = None

        if renderer_context is not None:
            possible_response = renderer_context.get("response")

            if isinstance(possible_response, Response):
                response = possible_response

        if response is None:
            return super().render(data, accepted_media_type, renderer_context)

        # A 204 response must not contain a response body
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return b""

        # Do not treat redirects, client errors, or server errors as success
        if not status.is_success(response.status_code):
            return super().render(data, accepted_media_type, renderer_context)

        if response.exception:
            return super().render(data, accepted_media_type, renderer_context)

        success_payload = build_success_payload(
            data=data, status_code=response.status_code
        )

        return super().render(success_payload, accepted_media_type, renderer_context)
