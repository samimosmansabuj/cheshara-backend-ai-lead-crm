from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import CreateAPIView
from django.db import transaction
import json

class BaseAPIView(APIView):
    serializer_class = None

    def get_serializer(self, *args, **kwargs):
        if self.serializer_class is None:
            return None

        kwargs.setdefault(
            "context",
            {"request": self.request}
        )

        return self.serializer_class(*args, **kwargs)

    def success_response(self, data=None, message=None, status_code=status.HTTP_200_OK,):
        response = {"success": True,}
        if message:
            response["message"] = message
        if data is not None:
            response["data"] = data
        return Response(response, status=status_code)

    def error_response(
        self,
        detail,
        status_code=status.HTTP_400_BAD_REQUEST,
    ):
        return Response(
            {
                "success": False,
                "detail": detail,
            },
            status=status_code,
        )

    def handle_exception_response(self, e, serializer=None):
        if isinstance(e, ValidationError):

            if serializer and serializer.errors:
                detail = {
                    key: str(value[0]) if isinstance(value, list) else str(value)
                    for key, value in serializer.errors.items()
                }
            else:
                detail = (
                    e.detail
                    if hasattr(e, "detail")
                    else str(e)
                )

            return self.error_response(detail)

        if isinstance(e, NotFound):
            return self.error_response(
                str(e),
                status.HTTP_404_NOT_FOUND,
            )

        return self.error_response(str(e))

class OwnAPIView(APIView):
    serializer_class = None
    
    def get_serializer(self, data):
        if self.serializer_class:
            return self.serializer_class(data=data, context={"request": self.request})
        return None
    
    def success_response(self, serializer=None) -> Response:
        return Response(
            {
                "success": True,
                "detail": ""
            }, status=status.HTTP_200_OK
        )
    
    def serializer_error_response(self, serializer=None, error=None) -> Response:
        if serializer and serializer.errors:
            detail = {
                key: str(value[0]) if isinstance(value, list) else str(value)
                for key, value in serializer.errors.items()
            }
        elif error:
            detail = error.detail if hasattr(error, "detail") else str(error)
        else:
            detail = "Validation error."
        return Response(
            {
                "success": False,
                "detail": detail
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def post(self, request, *args, **kwargs) -> Response:
        try:
            if self.get_serializer(data=request.data):
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                return self.success_response(serializer)
            return self.success_response()
        except ValidationError as e:
            return self.serializer_error_response(
                serializer=locals().get("serializer"),
                error=e
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "detail": str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )

class BasePatchAPIView(BaseAPIView):
    success_message = "Updated successfully"
        
    def get_instance(self):
        raise NotImplementedError
    
    def patch(self, request, *args, **kwargs):
        try:
            instance = self.get_instance()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            return self.success_response(serializer)
        except ValidationError as e:
            return self.serializer_error_response(
                serializer=locals().get("serializer"),
                error=e
            )
        except NotFound as e:
            return Response(
                {
                    "success": False,
                    "detail": str(e)
                }, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "detail": str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )

class BaseGetAPIView(APIView):
    serializer_class = None
    
    def get_serializer(self, *args, **kwargs):
        if self.serializer_class is None:
            return None

        kwargs.setdefault(
            "context",
            {"request": self.request}
        )

        return self.serializer_class(*args, **kwargs)
    
    def get_instance(self):
        return None
    
    def success_response(self, data=None, message=None, status_code=status.HTTP_200_OK,):
        response = {"success": True,}
        if message:
            response["message"] = message
        if data is not None:
            response["data"] = data
        return Response(response, status=status_code)
    
    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_instance()
            serializer = self.get_serializer(instance)
            return self.success_response(serializer)
        except NotFound as e:
            return Response(
                {
                    "success": False,
                    "detail": str(e)
                }, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "detail": str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )




class BaseCreateAPIView(CreateAPIView):
    success_message = "Created successfully"
    
    def get_serializer(self, data):
        if self.serializer_class:
            return self.serializer_class(data=data, context={"request": self.request})
        return None
    
    def create_perform(self, serializer):
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "success": True,
                "message": self.success_message
            }, status=status.HTTP_201_CREATED, headers=headers
        )

    def validation_error_response(self, serializer=None, error=None) -> Response:
        if serializer and serializer.errors:
            detail = {
                key: str(value[0]) if isinstance(value, list) else str(value)
                for key, value in serializer.errors.items()
            }
        elif error:
            detail = error.detail if hasattr(error, "detail") else str(error)
        else:
            detail = "Validation error."
        return Response(
            {
                "success": False,
                "detail": detail
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                return self.create_perform(serializer)
        except ValidationError as e:
            return self.validation_error_response(
                serializer=locals().get("serializer"),
                error=e
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "detail": str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )


