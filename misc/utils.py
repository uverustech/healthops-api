
from rest_framework.response import Response
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Let DRF handle the exception first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Customize the response format
        return custom_response(
            data=None,
            message=str(exc.detail if hasattr(exc, 'detail') else exc),
            errors=response.data if isinstance(response.data, dict) else [str(exc)],
            status="error",
            status_code=response.status_code
        )

    # Fallback for unhandled exceptions
    return custom_response(
        data=None,
        message="An unexpected error occurred.",
        errors=[str(exc)],
        status="error",
        status_code=500
    )

def custom_response(data=None, message=None, errors=None, status="success", status_code=200):
    return Response({
        "status": status,
        "errors": errors or [],
        "data": data or {},
        "message": message or "",
    }, status=status_code)
