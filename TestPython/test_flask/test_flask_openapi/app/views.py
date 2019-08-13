import json
from http import HTTPStatus

import yaml
from flask import request, Response
from openapi_core import create_spec, validate_parameters, validate_body
from openapi_core.validators import RequestValidator, ResponseValidator
from openapi_core.wrappers.flask import FlaskOpenAPIResponse

from TestPython.test_flask.test_flask_openapi import app
from TestPython.test_flask.test_flask_openapi import FlaskOpenAPIRequestWrapper

file_name = '../Pandora_1.0.0_swagger.yaml'
# file_name = '../test_schema.yaml'


@app.route('/users', methods=['POST'])
def create_user():
    user = request.get_json()
    validation_result = validate_request_body(request)
    if validation_result is not None:
        return Response(response=validation_result, status=HTTPStatus.BAD_REQUEST, mimetype="application/text")
    return Response(response=json.dumps(user), status=HTTPStatus.CREATED, mimetype='application/json')


@app.route('/users/<int:user_id>', methods=['GET'])
def retrieve_user(user_id):
    user = response_dict[int(user_id)]
    response = Response(response=json.dumps(user), status=HTTPStatus.OK.value, mimetype='application/json')  # should send .value
    validation_result = validate_response(request, response)
    if validation_result is not None:
        return Response(response=validation_result, status=HTTPStatus.INTERNAL_SERVER_ERROR, mimetype="application/text")
    return response


def validate_request_body(flask_request):
    with open(file_name, encoding='utf-8') as f:
        try:
            yaml_content = yaml.load(f)
            spec = create_spec(yaml_content)

            validator = RequestValidator(spec)
        except Exception as ex:
            raise ex

        openapi_request = FlaskOpenAPIRequestWrapper(flask_request)
        try:
            # result = validator.validate(openapi_request)
            # or
            validated_params = validate_parameters(spec, request, wrapper_class=FlaskOpenAPIRequestWrapper)
            validated_body = validate_body(spec, request, wrapper_class=FlaskOpenAPIRequestWrapper)
            print("validated_params: ", validated_params)
            print("validated_body: ", validated_body)
        except Exception as ex:
            # return ex.__repr__() #or
            return str(ex)


def validate_response(flask_request, flask_response):
    with open(file_name, encoding='utf-8') as f:
        yaml_content = yaml.load(f)
        spec = create_spec(yaml_content)

        validator = ResponseValidator(spec)

        openapi_request = FlaskOpenAPIRequest(flask_request)
        openapi_response = FlaskOpenAPIResponse(flask_response)

        try:
            result = validator.validate(openapi_request, openapi_response)
            # or
            # validated_data = validate_data(
            #     spec, flask_request, flask_response, response_wrapper_class=FlaskOpenAPIResponse, request_wrapper_class=FlaskOpenAPIRequest)
        except Exception as ex:
            return str(ex)


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