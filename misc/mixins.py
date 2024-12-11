

from rest_framework.response import Response

class CustomResponseMixin:
    def finalize_response(self, request, response, *args, **kwargs):
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

        # Determine status and prepare the wrapped response
        if response.status_code < 400:
            message = response.data.get("detail", "") if isinstance(response.data, dict) else ""
            if 'detail' in response.data:
                response.data.pop('detail', None)
            wrapped_response = {
                "status": "success",
                "errors": [],
                "data": response.data,
                "message": message,
            }
        else:
            # Handle errors: always return a list of errors
            errors = []
            if isinstance(response.data, dict):
                if "errors" in response.data.keys():
                    errors = response.data.get('errors')
                else:
                    # Collect all error messages into a flat list
                    for key, value in response.data.items():
                        if isinstance(value, list):
                            errors.extend(value)
                        else:
                            errors.append(str(value))
            else:
                errors.append(str(response.data))  # Catch-all for non-dict responses

            wrapped_response = {
                "status": "error",
                "errors": errors,
                "data": {},
                "message": response.data.get("detail", "An unexpected error occurred.")
                if isinstance(response.data, dict) else "An unexpected error occurred.",
            }

        # Replace response data with the wrapped response
        response.data = wrapped_response
        return super().finalize_response(request, response, *args, **kwargs)
