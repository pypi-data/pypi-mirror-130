from http import HTTPStatus

from modules.rest.schemas import BaseResponse
from modules.rest.utils import ResponseObject
from modules.rest.views import change_event


@change_event.after_request
def wrap_error_request(response):
    if response.status_code >= 400:
        j = response.json
        kwargs = dict()
        if "message" in j:
            kwargs["message"] = j["message"]

        if "errors" in j:
            kwargs["exceptionDetail"] = j["errors"]

        if "code" in j:
            kwargs["status"] = j["code"]

        if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
            kwargs["message"] = "Validation Error"

        _response = ResponseObject(**kwargs)
        _schema = BaseResponse()
        _response = _schema.dumps(_response)
        response.set_data(_response)
        return response
    else:
        return response
