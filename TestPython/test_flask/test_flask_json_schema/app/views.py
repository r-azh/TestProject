import json
import pprint
from http import HTTPStatus

from flask import request, Response
from jsonschema import FormatChecker, validate, ErrorTree, ValidationError
from jsonschema.validators import validator_for
from openapi_core import create_spec, validate_parameters, validate_body, validate_data

from TestPython.test_flask.test_flask_json_schema.app import app

file_name = '../test_schema.json'


@app.route('/users', methods=['POST'])
def create_user():
    user = request.get_json()
    validation_result = validate_request_body(request)
    if validation_result is not None:
        return Response(response=validation_result, status=HTTPStatus.BAD_REQUEST, mimetype="application/text")
    return Response(response=json.dumps(user), status=HTTPStatus.CREATED, mimetype='application/json')


@app.route('/users/<user_id>', methods=['GET'])
def retrieve_user(user_id):
    user = response_dict[int(user_id)]
    response = Response(response=json.dumps(user), status=HTTPStatus.OK, mimetype='application/json')
    validation_result = validate_response(request, response)
    if validation_result is not None:
        return Response(response=validation_result, status=HTTPStatus.INTERNAL_SERVER_ERROR, mimetype="application/text")
    return response


def validate_request_body(flask_request):
    with open(file_name, encoding='utf-8') as f:
        json_content = json.load(f)
        user_schema = json_content['components']['schemas']['User']
        # try:
        #     result = validate(flask_request.get_json(), user_schema, format_checker=FormatChecker())
        # except Exception as ex:
        #     # return ex.__repr__() #or
        #     error_param = ex.context[-1].instance if hasattr(ex, 'context') and len(ex.context) > 0 else ex
        #     return ex.message
        # v = Draft4Validator(user_schema)
        cls = validator_for(user_schema)
        cls.check_schema(user_schema)
        tree = ErrorTree(cls(user_schema, format_checker=FormatChecker()).iter_errors(json_content))

        # tree = ErrorTree(v.iter_errors(flask_request.get_json()))

        if tree.total_errors > 0:
            print(tree.total_errors)
            error_list = parse_tree_errors(tree)
            pprint.pprint(error_list)
            return ', '.join(e['message'] for e in error_list) if error_list else None


def parse_tree_errors(tree):
    errors = []
    if len(tree.errors) > 0:
        for error_key, error_value in tree.errors.items():
            if isinstance(error_value, ValidationError):
                errors.append({
                    'type': type(error_value),
                    'key': error_key,
                    'validator': error_value.validator,
                    'validator_value': error_value.validator_value,
                    'instance': error_value.instance,
                    'path': error_value.path.popleft() if len(error_value.path) > 0 else '',
                    'message': error_value.message
                })
    else:
        for key, value in tree._contents.items():
            err_list = parse_tree_errors(value)
            errors.extend(err_list) if err_list else None
    return errors if len(errors) > 0 else None


def validate_response(flask_request, flask_response):
    with open(file_name, encoding='utf-8') as f:
        json_content = json.load(f)
        user_schema = json_content['components']['schemas']['User']
        try:
            result = validate(flask_response.get_json(), user_schema, format_checker=FormatChecker())
        except Exception as ex:
            # return ex.__repr__() #or
            error_param = ex.context[-1].instance if hasattr(ex, 'context') and len(ex.context) > 0 else ex
            return ex.message


response_dict = {
    1: {
        "id": 1,
        "name": 'rezvan'
    },
    2: {
        "id_": 1,
        "name": 'rezvan'
    },
    3: {
        "id": 1
    },
    4: {
        "id": 'a',
        "name": 'rezvan'
    }
}


# {
#    "description": "empty request body",
#    "type": "object",
#    "additionalProperties": false,
#    "properties": {
#     }
 # }