from like_grow_app.model.facebook_user import FacebookUser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from allauth.socialaccount.models import SocialAccount
from like_grow_app.serializers.facebook_user_serializer import FacebookUserSerializer
import json
import operator
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from functools import reduce
from django.conf import settings
from simple_search import search_filter
from django.db import transaction
''' utility '''
from rest_apiresponse.apiresponse import ApiResponse

from utility.utils import MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, get_serielizer_error, get_pagination_resp, transform_list
from utility.constants import *


class FacebookUserViewSet(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    serializer_class = FacebookUserSerializer
    authentication_classes = [OAuth2Authentication, ]
    # permission_classes = [IsAuthenticated]
    singular_name = 'Facebook User'
    model_class = FacebookUser.objects
    
    search_fields = ['name', 'city', 'marks', 'email']

    def get_object(self, pk):
        try:
            return self.model_class.get(pk=pk)
        except:
            return None
    
    @transaction.atomic()
    def create(self, request, *args, **kwargs):
            '''
            :To create the new record
            '''
            sp1 = transaction.savepoint()
        
            ''' capture data '''
            req_data = request.data.copy()
            email = req_data.get('email')
            
            required_filed = [ 'name', 'email', 'accessToken']
            for key in required_filed:
                if not req_data.get(key):
                    return ApiResponse.response_bad_request(self, message=f"{key} is required")
            
            if email:
                is_email_exist = self.model_class.filter(email=req_data.get('email')).first()
                if is_email_exist:
                    return ApiResponse.response_bad_request(self, message="Email is already exist")
            if req_data.get('id'):
                req_data['user_id'] = req_data.get('id')

            if req_data.get('accessToken'):
                req_data['access_token'] = req_data.get('accessToken')

            serializer = self.serializer_class(data=req_data)

            ''' validate serializer '''
            if serializer.is_valid():
                serializer.save()
                serializer_instance = serializer.instance
                req_data['user_id'] = req_data.get('id')
                req_data['access_token'] = req_data.get('accessToken')

                transaction.savepoint_commit(sp1)
                return ApiResponse.response_created(self, data=req_data,
                                                    message=self.singular_name + ' created successfully.')

            ''' serializer error '''
            error_resp = get_serielizer_error(serializer)
            transaction.savepoint_rollback(sp1)
            return ApiResponse.response_bad_request(self, message=error_resp)