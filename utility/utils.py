from stark_utilities.utilities import *
from datetime import datetime , timedelta
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauth2_provider.settings import oauth2_settings
from django.core.mail import send_mail, EmailMessage
from oauthlib.oauth2.rfc6749.tokens import random_token_generator
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db import transaction



""" mixins to handle request url """


class CreateRetrieveUpdateViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    pass


class MultipleFieldPKModelMixin(object):
    """
    Class to override the default behaviour for .get_object for models which have retrieval on fields
    other  than primary keys.
    """

    lookup_field = []
    lookup_url_kwarg = []

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        get_args = {field: self.kwargs[field] for field in self.lookup_field if field in self.kwargs}

        get_args.update({"pk": self.kwargs[field] for field in self.lookup_url_kwarg if field in self.kwargs})
        return get_object_or_404(queryset, **get_args)



""" demo login response """
def get_login_response(user=None, token=None):
    resp_dict = dict()
    resp_dict["id"] = user.id
    resp_dict["first_name"] = user.first_name
    resp_dict["last_name"] = user.last_name
    resp_dict["email"] = user.email
    resp_dict["mobile"] = user.mobile
    resp_dict["username"] = user.username
    # resp_dict["group"] = user.group_id
    return resp_dict

def send_common_email(subject, message, email_to, from_emails):
    try:
        msg = EmailMessage(subject, message, to=[email_to], from_email=from_emails)
        msg.content_subtype = "html"
        msg.send()
    except:
        pass

def generate_token(request, user):
    expire_seconds = oauth2_settings.user_settings["ACCESS_TOKEN_EXPIRE_SECONDS"]

    scopes = oauth2_settings.user_settings["SCOPES"]

    application = Application.objects.first()
    expires = datetime.now() + timedelta(seconds=expire_seconds)
    access_token = AccessToken.objects.create(
        user=user,
        application=application,
        token=random_token_generator(request),
        expires=expires,
        scope=scopes,
    )

    refresh_token = RefreshToken.objects.create(
        user=user, token=random_token_generator(request), access_token=access_token, application=application
    )

    token = {
        "access_token": access_token.token,
        "token_type": "Bearer",
        "expires_in": expire_seconds,
        "refresh_token": refresh_token.token,
        "scope": scopes,
    }
    return token

def get_pagination_resp(data, request):
    page_response = {"total_count": None, "total_pages": None,
                     "current_page": None, "limit": None}
    if request.query_params.get('type') == 'all':
        return {"data": data}

    page = request.query_params.get('page') if request.query_params.get('page') else 1
    limit = request.query_params.get('limit') if request.query_params.get('limit') else settings.PAGE_SIZE
    paginator = Paginator(data, limit)
    category_data = paginator.get_page(page).object_list
    page_response = {"total_count": paginator.count, "total_pages": paginator.num_pages,
                     "current_page": page, "limit": limit}
    current_page = paginator.num_pages
    paginator = {"paginator": page_response}
    if int(current_page) < int(page):
        return {"data": [], "paginator": paginator.get('paginator')}
        # return {"data": [], **paginator}
    response_data = {"data": category_data, "paginator": paginator.get('paginator')}
    return response_data

def transform_list(self, data):
    return map(self.transform_single, data)

def get_serielizer_error(serializer, with_key=False):
    """handle serializer error"""
    msg_list = []
    try:
        mydict = serializer.errors
        for key in sorted(mydict.keys()):
            msg = ""

            if with_key:
                msg = key + " : "

            msg += str(mydict.get(key)[0])

            msg_list.append(msg)
    except:
        msg_list = ["Invalid format"]
    return msg_list


def create_or_update_serializer(
    serializer_class,
    data,
    savepoint=None,
    instance=None
):
    if instance:
        serializer = serializer_class(instance, data=data, partial=True)
    else:
        serializer = serializer_class(data=data)

    if serializer.is_valid():
        serializer.save()
        return  serializer.instance, None
    if savepoint:
        transaction.savepoint_rollback(savepoint)

    return None, get_serielizer_error(serializer)


def generate_otp_number():
    range_start = 10 ** (settings.OTP_LENGTH - 1)
    range_end = (10 ** settings.OTP_LENGTH) - 1
    return randint(range_start, range_end)

