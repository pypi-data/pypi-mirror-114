import json
from flask import request, g


def get_request_method():
    return request.method


def get_request_headers(key=None, default=''):
    if key:
        if request.headers:
            return request.headers.get(key, default)
        else:
            return default
    else:
        if request.headers:
            return request.headers
        else:
            if default != '':
                return default
            else:
                return {}


def get_request_data(key=None, default=''):
    if key:
        if request.data:
            return json.loads(request.data).get(key, default)
        else:
            return default
    else:
        if request.data:
            return json.loads(request.data)
        else:
            if default != '':
                return default
            else:
                return {}


def get_request_form(key=None, default=[]):
    if key:
        if request.form:
            return request.form.getlist(key)
        else:
            return default
    else:
        if request.form:
            form = {}
            keys = request.form.keys()
            for key in keys:
                form[key] = request.form.getlist(key)
            return form
        else:
            if default != []:
                return default
            else:
                return {}


def get_request_files(key=None):
    if request.files:
        if key:
            return request.files.get(key)
        return dict(request.files)
    return {}


def get_request_args(key=None):
    if key:
        return request.args.get(key)
    else:
        return request.args


def get_request_url():
    return request.url


def mask_fields_in_data(data, fields, mask='*****'):
    data = data.copy()
    for field in fields:
        if field in data:
            data[field] = mask
    return data
