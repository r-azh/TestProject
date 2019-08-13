# pip install openapi-core
import os

import yaml
from openapi_core import create_spec, validate_parameters, validate_body
from openapi_core.validation import request, response
from openapi_core.validators import RequestValidator

file_name = 'test_schema.yaml'
with open(file_name, encoding='utf-8') as f:
    yaml_content = yaml.load(f)
    spec = create_spec(yaml_content)

    validator = RequestValidator(spec)
    result = validator.validate(request)

    # raise errors if request invalid
    result.raise_for_errors()

    # get list of errors
    errors = result.errors

    # get parameters dictionary with path, query, cookies and headers parameters
    validated_params = result.parameters

    # get body
    validated_body = result.body

    validated_params_ = validate_parameters(spec, request)
    validated_body_ = validate_body(spec, request)

##########################
from openapi_core.validators import ResponseValidator

validator = ResponseValidator(spec)
result = validator.validate(request, response)

# raise errors if response invalid
result.raise_for_errors()

# get list of errors
errors = result.errors

# get headers
validated_headers = result.headers

# get data
validated_data = result.data

from openapi_core import validate_data

validated_data = validate_data(spec, request, response)

##########################
    # from bravado_core.spec import Spec

    # spec2 = Spec.from_dict(yaml_content['components']['schemas']['User'])
    # user = spec2['components']['schemas']['User']
