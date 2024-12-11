
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        errors = []
        if isinstance(response.data, dict):
            for key, value in response.data.items():
                if isinstance(value, list):
                    errors.extend(value)
                else:
                    errors.append(str(value))
        else:
            errors.append(str(response.data))
        
        return custom_response(
            data=None,
            message=response.data.get("detail", "An unexpected error occurred.")
            if isinstance(response.data, dict) else "An unexpected error occurred.",
            errors=errors,
            status="error",
            status_code=response.status_code
        )

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
