from flask import jsonify


def unauthorized():
    response = jsonify({'error': 'Unauthorized'})
    response.status_code = 401
    return response



