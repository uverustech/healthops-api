

from rest_framework.response import Response

class CustomResponseMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        """
        Overrides the finalize_response method to format all responses
        in a consistent format.
        """
        # Ensure the response is an instance of DRF's Response
        if not isinstance(response, Response):
            return super().finalize_response(request, response, *args, **kwargs)
        
        # Preserve original response context (required by DRF)
        response.accepted_renderer = self.request.accepted_renderer
        response.accepted_media_type = self.request.accepted_media_type
        try:
            response.renderer_context = self.request.renderer_context
        except:
            pass

        # Prepare custom structure
        status = "success" if response.status_code < 400 else "error"
        wrapped_response = {
            "status": status,
            "errors": response.data if status == "error" else [],
            "data": response.data if status == "success" else {},
            "message": response.data.get("detail", "") if isinstance(response.data, dict) else "",
        }

        # Replace response data with the wrapped response
        response.data = wrapped_response
        return super().finalize_response(request, response, *args, **kwargs)
