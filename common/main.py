from fastapi import Request


def get_template(request: Request):
    dict = {'request': request}
    return dict
