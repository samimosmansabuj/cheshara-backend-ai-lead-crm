from rest_framework.viewsets import ModelViewSet
from core.utils.viewsets import OwnModelViewSet
from .models import BusinessType, Industry
from .permissions import AdminWritePermission
from .serializers import (
    BusinessTypeSerializer,
    IndustrySerializer,
)


class BusinessTypeViewSet(OwnModelViewSet):
    serializer_class = BusinessTypeSerializer
    permission_classes = [AdminWritePermission]
    queryset = BusinessType.objects.filter(is_active=True).order_by("sort_order", "name")


class IndustryViewSet(OwnModelViewSet):
    serializer_class = IndustrySerializer
    permission_classes = [AdminWritePermission]
    queryset = Industry.objects.filter(is_active=True).order_by("sort_order", "name")




from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from .models import (
    TwilioConfiguration,
    FreeTrailPhoneNumber,
    FreeTrailDetails,
)

from core.utils.viewsets import OwnReadOnlyModelViewSet
from .serializers import FreeTrailPhoneNumberSerializer, SearchTrialNumberSerializer, SendSMSSerializer
from twilio.rest import Client
import os
import logging
logger = logging.getLogger(__name__)
from business.choices import PhoneNumberStatus
from twilio.base.exceptions import TwilioRestException

class FreeTrailPhoneNumberViewSet(OwnReadOnlyModelViewSet):
    serializer_class = FreeTrailPhoneNumberSerializer
    queryset = (FreeTrailPhoneNumber.objects.select_related().order_by("phone_number"))

    FREE_TRAIL_ACCOUNT_SID = os.getenv("FREE_TRAIL_ACCOUNT_SID")
    FREE_TRAIL_AUTH_TOKEN = os.getenv("FREE_TRAIL_AUTH_TOKEN")

    MASTER_ACCOUNT_SID = os.getenv("ACCOUNT_SID")
    MASTER_AUTH_TOKEN = os.getenv("AUTH_TOKEN")
    
    # All Available Trial Number---
    @action(detail=False, methods=["get"])
    def available(self, request):
        queryset = self.get_queryset().filter(status=PhoneNumberStatus.ACTIVE, is_used=False)
        return Response(
            {
                "success": True,
                "count": len(queryset),
                "results": self.get_serializer(queryset, many=True).data,
            },
            status=status.HTTP_200_OK,
        )


    # Search Available number in Twilio---
    def serialize_search_phone_number(self, number):
        return {
            "friendly_name": number.friendly_name,
            "phone_number": number.phone_number,
            "lata": getattr(number, "lata", None),
            "rate_center": getattr(number, "rate_center", None),
            "region": getattr(number, "region", None),
            "postal_code": getattr(number, "postal_code", None),
            "locality": getattr(number, "locality", None),
            "iso_country": getattr(number, "iso_country", None),
            "capabilities": number.capabilities,
            "address_requirements": number.address_requirements,
        }

    @action(detail=False, methods=["get"], url_path="search-number")
    def search_number(self, request):
        serializer = SearchTrialNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        country=serializer.validated_data.get("country", "US")
        # area_code=serializer.validated_data.get("area_code"),
        # contains=serializer.validated_data.get("contains"),
        # limit=serializer.validated_data.get("limit"),

        FREE_TRAIL_ACCOUNT_SID = os.getenv("FREE_TRAIL_ACCOUNT_SID")
        FREE_TRAIL_AUTH_TOKEN = os.getenv("FREE_TRAIL_AUTH_TOKEN")
        client = Client(FREE_TRAIL_ACCOUNT_SID, FREE_TRAIL_AUTH_TOKEN)
        resource = client.available_phone_numbers(country).toll_free
        # resource = client.available_phone_numbers(country).local
        numbers = resource.list(limit=2, sms_enabled=True)
        numbers_list = [
            self.serialize_search_phone_number(number)
            for number in numbers
        ]

        return Response(
            {
                "success": True,
                "count": len(numbers_list),
                "results": numbers_list,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"], url_path="check-availability")
    def check_availability(self, request):
        data = request.data
        last_4_digit = data.get("last_4_digit", None)
        if last_4_digit is None:
            return Response(
                {
                    "success": False,
                    "message": "Submit Must be last 4 digit of number."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


        FREE_TRAIL_ACCOUNT_SID = os.getenv("FREE_TRAIL_ACCOUNT_SID")
        FREE_TRAIL_AUTH_TOKEN = os.getenv("FREE_TRAIL_AUTH_TOKEN")
        client = Client(FREE_TRAIL_ACCOUNT_SID, FREE_TRAIL_AUTH_TOKEN)
        resource = client.available_phone_numbers("US").toll_free.list(limit=2, sms_enabled=True, contains=last_4_digit)
        numbers_list = [
            self.serialize_search_phone_number(number)
            for number in resource
        ]
        return Response(
            {
                "success": True,
                "count": len(numbers_list),
                "results": numbers_list,
            },
            status=status.HTTP_200_OK,
        )


    # Purchase Number from Twilio---
    def serialize_purchase_phone_number(self, phone):
        return {
            "sid": getattr(phone, "sid", None),
            "account_sid": getattr(phone, "account_sid", None),
            "friendly_name": getattr(phone, "friendly_name", None),
            "phone_number": getattr(phone, "phone_number", None),
            "country_code": getattr(phone, "iso_country", None),
            "capabilities": getattr(phone, "capabilities", {}),
            "voice_url": getattr(phone, "voice_url", None),
            "sms_url": getattr(phone, "sms_url", None),
            "status_callback": getattr(phone, "status_callback", None),
            "address_requirements": getattr(phone, "address_requirements", None),
            "date_created": getattr(phone, "date_created", None),
            "date_updated": getattr(phone, "date_updated", None),
            "uri": getattr(phone, "uri", None),
        }
    
    def to_dict(self, phone):
        return {
            "sid": phone.sid,
            "account_sid": phone.account_sid,
            "phone_number": phone.phone_number,
            "friendly_name": phone.friendly_name,
            "status": phone.status,
            "type": phone.type,
            "origin": phone.origin,
            "capabilities": phone.capabilities,
            "sms_url": phone.sms_url,
            "voice_url": phone.voice_url,
            "sms_method": phone.sms_method,
            "voice_method": phone.voice_method,
            "status_callback": phone.status_callback,
            "status_callback_method": phone.status_callback_method,
            "voice_fallback_url": phone.voice_fallback_url,
            "voice_fallback_method": phone.voice_fallback_method,
            "sms_fallback_url": phone.sms_fallback_url,
            "sms_fallback_method": phone.sms_fallback_method,
            "address_sid": phone.address_sid,
            "bundle_sid": phone.bundle_sid,
            "identity_sid": phone.identity_sid,
            "trunk_sid": phone.trunk_sid,
            "voice_application_sid": phone.voice_application_sid,
            "sms_application_sid": phone.sms_application_sid,
            "voice_receive_mode": phone.voice_receive_mode,
            "voice_caller_id_lookup": phone.voice_caller_id_lookup,
            "emergency_status": phone.emergency_status,
            "emergency_address_sid": phone.emergency_address_sid,
            "emergency_address_status": phone.emergency_address_status,
            "api_version": phone.api_version,
            "address_requirements": phone.address_requirements,
            "beta": phone.beta,
            "uri": phone.uri,
            "date_created": phone.date_created,
            "date_updated": phone.date_updated,
        }

    @action(detail=False, methods=["post"])
    @transaction.atomic
    def purchase(self, request):
        data = request.data
        print("data: ", data)
        phone_number = data.get("phone_number", None)


        if phone_number is not None:
            payload = {"phone_number": phone_number,}

            FREE_TRAIL_ACCOUNT_SID = os.getenv("FREE_TRAIL_ACCOUNT_SID")
            FREE_TRAIL_AUTH_TOKEN = os.getenv("FREE_TRAIL_AUTH_TOKEN")
            client = Client(FREE_TRAIL_ACCOUNT_SID, FREE_TRAIL_AUTH_TOKEN)
            purchased = client.incoming_phone_numbers.create(**payload)
            print("purchased: ", purchased)
            logger.info("Phone number purchased successfully (%s)", purchased.phone_number,)
            
            serialize_phone_number = self.to_dict(purchased)
            print("serialize_phone_number: ", serialize_phone_number)
            
            OWNER_ACCOUNT_SID = os.getenv("ACCOUNT_SID")
            obj, created = FreeTrailPhoneNumber.objects.update_or_create(
                provider_phone_sid=serialize_phone_number["sid"],
                phone_number=serialize_phone_number["phone_number"],
                defaults={
                    "owner_account_sid": OWNER_ACCOUNT_SID,
                    "account_sid": FREE_TRAIL_ACCOUNT_SID,
                    "account_auth_token": FREE_TRAIL_AUTH_TOKEN,
                    "capabilities": serialize_phone_number["capabilities"],
                    "metadata": serialize_phone_number,
                    "status": PhoneNumberStatus.ACTIVE,

                    "purchased_at": serialize_phone_number["date_created"],
                    "last_synced_at": serialize_phone_number["date_updated"],
                    "is_used": False,
                    "webhook_url": serialize_phone_number["sms_url"] or "",
                },
            )
            
            return Response(
                {
                    "success": True,
                    "message": "Trial number purchased successfully.",
                    "data": self.get_serializer(obj).data
                }, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    "success": False,
                    "message": "Parchase Number field i empty."
                }, status=status.HTTP_400_BAD_REQUEST
            )
    

    # Sub Account Create in Twilio---
    def serialize_subaccount(self, sub_account):
        return {
            "sid": sub_account.sid,
            "friendly_name": sub_account.friendly_name,
            "status": sub_account.status,
            "owner_account_sid": sub_account.owner_account_sid,
            # "date_created": sub_account.date_created,
            "auth_token": sub_account.auth_token,
        }
    
    @action(detail=False, methods=["post"], url_path="create-free-trail-account")
    @transaction.atomic
    def create_free_trail_account(self, request):
        data = request.data
        account_name = data.get("account_name", None)

        # ACCOUNT_SID = os.getenv("ACCOUNT_SID")
        # AUTH_TOKEN = os.getenv("AUTH_TOKEN")
        # client = Client(ACCOUNT_SID, AUTH_TOKEN)
        # sub_account = client.api.accounts.create(
        #     friendly_name=account_name
        # )
        # serialize_subaccount = self.serialize_subaccount(sub_account)
        return Response(
            {
                "success": True,
                # "data": serialize_subaccount,
            },
            status=status.HTTP_200_OK,
        ) 


    # Release Twilio Number---
    @action(detail=True, methods=["post"])
    @transaction.atomic
    def release(self, request, pk):
        object = self.get_object()
        trial_client = self.get_trial_client()
        trial_client.incoming_phone_numbers(object.provider_phone_sid).delete()

        object.status = PhoneNumberStatus.RELEASED
        object.released_at = timezone.now()
        object.last_synced_at = timezone.now()
        object.save()
        return Response(
            {
                "success": True,
                "message": "Trial number released successfully.",
            },
            status=status.HTTP_200_OK,
        )


    # Sync Twilio Number---
    @action(detail=True, methods=["get"])
    @transaction.atomic
    def sync(self, request, pk):
        object = self.get_object()
        client = self.get_client(object)
        phone  = client.incoming_phone_numbers(object.provider_phone_sid).fetch()
        phone_serializer = self.to_dict(phone)
        return Response(
            {
                "success": True,
                "data": phone_serializer
            }, status=status.HTTP_200_OK
        )


    # Update Twilio Number---
    @action(detail=True, methods=["post"], url_path="update-twilio-phone")
    def update_twilio_phone(self, request, pk):
        object = self.get_object()
        client = self.get_client(object)      
        phone = client.incoming_phone_numbers(object.provider_phone_sid).update(
            sms_url="https://api.remyza.com/api/v1/twilio/webhook/",
            sms_method="POST",
        )

        print(phone.sms_url)

        phone_serializer = self.to_dict(phone)
        return Response(
            {
                "success": True,
                "data": phone_serializer
            }, status=status.HTTP_200_OK
        )


    @action(detail=True, methods=["post"], url_path="send-test-sms")
    @transaction.atomic
    def send_test_sms(self, request, pk=None):
        phone_number = self.get_object()

        serializer = SendSMSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # client = self.get_trial_client()
        client = self.get_master_client()

        try:
            message = client.messages.create(
                from_=phone_number.phone_number,
                to=serializer.validated_data["to"],
                body=serializer.validated_data["body"],
            )
            print("message--------: ", message)
            print("message dict--------: ", message.__dict__)

            return Response(
                {
                    "success": True,
                    "message": "SMS sent successfully.",
                    "data": {
                        "sid": message.sid,
                        "status": message.status,
                        "from": message.from_,
                        "to": message.to,
                        "body": message.body,
                        "date_created": message.date_created,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except TwilioRestException as e:
            return Response(
                {
                    "success": False,
                    "detail": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )




    
    def all_number_synce(self):
        object = self.get_object()
        trial_client = self.get_trial_client()
        numbers = trial_client.incoming_phone_numbers.list(limit=100)
        for number in numbers:
            all_number = (
                {
                    "sid": number.sid,
                    "phone_number": number.phone_number,
                    "friendly_name": number.friendly_name,
                    "account_sid": number.account_sid,
                    "country": number.iso_country,
                    "capabilities": number.capabilities,
                    "voice_url": number.voice_url,
                    "sms_url": number.sms_url,
                    "date_created": number.date_created,
                    "uri": number.uri,
                }
            )
        return all_number

    def get_client(self, object: FreeTrailPhoneNumber):
        return Client(object.account_sid, object.account_auth_token)
    
    def get_trial_client(self):
        return Client(self.FREE_TRAIL_ACCOUNT_SID, self.FREE_TRAIL_AUTH_TOKEN)

    def get_master_client(self):
        return Client(self.MASTER_ACCOUNT_SID, self.MASTER_AUTH_TOKEN)


