from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.db.models import Q
from ohm2_handlers_light import utils as h_utils
from ohm2_handlers_light.definitions import RunException
from . import models as matialvarezs_request_handler_models
from . import errors as matialvarezs_request_handler_errors
from . import settings
import os, time, random
import requests, simplejson as json, tenacity
from . import exceptions

random_string = "tcqbKo7e388aBSe5RwdtriURrQdVLqhm"

"""
def parse_model_attributes(**kwargs):
	attributes = {}
	
	return attributes

def create_model(**kwargs):

	for key, value in parse_model_attributes(**kwargs).items():
		kwargs[key] = value
	return h_utils.db_create(matialvarezs_request_handler_models.Model, **kwargs)

def get_model(**kwargs):
	return h_utils.db_get(matialvarezs_request_handler_models.Model, **kwargs)

def get_or_none_model(**kwargs):
	return h_utils.db_get_or_none(matialvarezs_request_handler_models.Model, **kwargs)

def filter_model(**kwargs):
	return h_utils.db_filter(matialvarezs_request_handler_models.Model, **kwargs)

def q_model(q, **otions):
	return h_utils.db_q(matialvarezs_request_handler_models.Model, q)

def delete_model(entry, **options):
	return h_utils.db_delete(entry)

def update_model(entry, **kwargs):
	attributes = {}
	for key, value in parse_model_attributes(**kwargs).items():
		attributes[key] = value
	return h_utils.db_update(entry, **attributes)
"""


def by_method_request(method, *args, **kwargs):
    method = getattr(requests, method, None)
    if method is None:
        raise exceptions.MethodNotSupported()
    return method(*args, **kwargs)


def get_response(method, *args, **kwargs):
    try:
        return by_method_request(method, *args, **kwargs), None
    except requests.exceptions.Timeout:
        return None, "TIMEOUT_ERROR"  # raise exceptions.Timeout()
    except requests.exceptions.ConnectionError:
        return None, "CONNECTION_ERROR"  # raise exceptions.ConnectionError()

        # return response


def get_custom_get_response(max_tries, delay_between_requests):
    @tenacity.retry(
        retry=(tenacity.retry_if_exception_type(exceptions.Timeout) | tenacity.retry_if_exception_type(
            exceptions.ConnectionError)),
        stop=tenacity.stop_after_attempt(max_tries),
        wait=tenacity.wait_fixed(delay_between_requests)
    )
    def _get_response(method, *args, **kwargs):
        return get_response(method, *args, **kwargs)

    return _get_response


def get_default_headers():
    headers = {
        "User-Agent": "TEST",
    }
    return headers


def safe_request(url, method="post", **options):
    max_tries = options.get("max_tries", 5)
    delay_between_requests = options.get("delay_between_requests", 1)
    request_timeout = options.get("request_timeout", None)

    return_value_on_max_tries_reached = options.get("return_value_on_max_tries_reached", None)
    basic_auth_username = options.get('basic_auth_username', None)
    basic_auth_password = options.get('basic_auth_password', None)
    get_response_kwargs = {}
    verify_ssl_certificate = options.get('verify_ssl_certificate', False)
    get_response_kwargs['verify'] = verify_ssl_certificate

    if basic_auth_username and basic_auth_password:
        get_response_kwargs['auth'] = requests.auth.HTTPBasicAuth(basic_auth_username, basic_auth_password)

    if request_timeout:
        get_response_kwargs["timeout"] = request_timeout

    headers = options.get("headers", None)
    if options.get("get_default_headers") and headers is None:
        headers = get_default_headers()

    if headers:
        get_response_kwargs["headers"] = headers

    data = options.get("data", None)
    if data:
        if options.get("convert_data_to_json", False) is True:
            data = json.dumps(data)
        get_response_kwargs["data"] = data

    try:
        return get_custom_get_response(max_tries, delay_between_requests)(method, url, **get_response_kwargs)
    except tenacity.RetryError:
        response = return_value_on_max_tries_reached
    return response


def send_post_and_get_response(url, **options):
    return safe_request(url, "post", **options)


def send_get_and_get_response(url, **options):
    return safe_request(url, "get", **options)


def send_put_and_get_response(url, **options):
    return safe_request(url, "put", **options)


def send_delete_and_get_response(url, **options):
    return safe_request(url, "delete", **options)


def send_post(url, **options):
    response, error = send_post_and_get_response(url, **options)
    if response:
        if response.status_code == requests.codes.ok:
            return (True, None)
        return (False, response.reason)
    return (False, exceptions.BadRequest())


def send_get(url, **options):
    response, error = send_get_and_get_response(url, **options)
    if response:
        if response.status_code == requests.codes.ok:
            return (True, None)
        return (False, response.reason)
    return (False, exceptions.BadRequest())


def send_put(url, **options):
    response, error = send_put_and_get_response(url, **options)
    if response:
        if response.status_code == requests.codes.ok:
            return (True, None)
        return (False, response.reason)
    return (False, exceptions.BadRequest())


def send_delete(url, **options):
    response, error = send_delete_and_get_response(url, **options)
    if response:
        if response.status_code == requests.codes.ok:
            return (True, None)
        return (False, response.reason)
    return (False, exceptions.BadRequest())
