"""
Helper utility functions
"""

from flask import Response
import json


def create_response(status_code=200, data_field='data', data=None, headers=None, error=None):
    """
    Given data and error, create response
    """
    # format output
    output = {}
    if error:
        output['error'] = error

    if data:
        output[data_field] = data

    # create response
    return Response(
        response=json.dumps(output),
        status=status_code,
        headers=headers,
        content_type='application/json',
    )


def getitem(model, model_id_field, id_to_search):
    """
    Helper function to search model for given id
    """
    item = model.query.filter(model_id_field == id_to_search).all()

    if len(item) == 0:
        return None

    return item[0]
