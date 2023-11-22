from flask import jsonify, request
from ecommercetools import seo


def get_search():
    if not request.args.get('query'):
        return None
    else:
        data = seo.get_serps(query=request.args.get('query'), output="dictionary", pages=1,
                             domain="google.com", host_language="id")
        return data