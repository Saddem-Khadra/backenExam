from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # handlers = {
    #     "NotSold": _handle_generic_error,
    # }

    response = exception_handler(exc, context)

    if response is not None:
        status_code = response.status_code
        detail = []
        for k, v in dict(response.data).items():
            if k != 'detail':
                detail.append(f"{k} : {v[0]}")
                response.data.pop(k)
        if len(detail) != 0:
            response.data['detail'] = " ".join(detail)
        response.data['status_code'] = status_code

    # exception_class = exc.__class__.__name__

    # if exception_class in handlers:
    #     return handlers[exception_class](exc, context, response)
    return response

# def _handle_generic_error(exc, context, response):
#     response.data = {
#         'detail': exc.detail,
#         'status_code': response.status_code
#     }
#     return response
