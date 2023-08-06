from http import HTTPStatus

from flask.views import MethodView
from flask_smorest import Blueprint
from ...modules.rest.schemas import ChangeEventSchema, ChangeEventResponse, \
    BaseResponse, \
    ChangeEventsResponse
from ...modules.rest.business import create_change_event, fetch_change_event, \
    delete_change_event, fetch_change_event_field_name, fetch_change_event_tag, \
    search_change_event_with_fieldName_tagName_userName_eventTime

change_event = Blueprint("change_event", "pets", url_prefix="/api/v1/change_event",
                         description="change_event tablosundan veri çekmek için kullanılan servis")


@change_event.route("/")
class ChangeEvent(MethodView):
    @change_event.arguments(ChangeEventSchema, location="json")
    @change_event.response(HTTPStatus.CREATED, BaseResponse)
    @change_event.alt_response(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, success=False, schema=BaseResponse)
    @change_event.alt_response(status_code=HTTPStatus.BAD_GATEWAY, success=False, schema=BaseResponse)
    def post(self, args, ):
        """Yeni Change Event oluşturmak için kullanılır"""
        return create_change_event(args)


@change_event.route("/<int:change_event_id>")
class ChangeEventCollection(MethodView):
    @change_event.response(HTTPStatus.OK, ChangeEventResponse)
    @change_event.alt_response(status_code=HTTPStatus.NOT_FOUND, success=False, schema=BaseResponse)
    def get(self, change_event_id):
        """ID bilgisi verilen Change Event'in detaylarını görüntülemek için kullanılır"""
        return fetch_change_event(change_event_id)


    @change_event.response(HTTPStatus.OK, BaseResponse)
    @change_event.alt_response(status_code=HTTPStatus.NOT_FOUND, success=False, schema=BaseResponse)
    @change_event.alt_response(status_code=HTTPStatus.BAD_GATEWAY, success=False, schema=BaseResponse)
    def delete(self, change_event_id):
        """ID bilgisi verilen Change Event'i silmek için kullanılır"""
        return delete_change_event(change_event_id)


@change_event.route("/<string:change_event_field_name>")
class ChangeEventCollectionFieldName(MethodView):
    @change_event.response(HTTPStatus.OK, ChangeEventsResponse)
    @change_event.paginate()
    @change_event.alt_response(status_code=HTTPStatus.NOT_FOUND, success=False, schema=ChangeEventResponse)
    def get(self, change_event_field_name, pagination_parameters, **kwargs):
        """Alan adı bilgisi verilen Change Event'in detaylarını görüntülemek için kullanılır"""
        return fetch_change_event_field_name(change_event_field_name, pagination_parameters)


@change_event.route("/filter/<string:tag_name>")
class ChangeEventCollectionTag(MethodView):
    @change_event.response(HTTPStatus.OK, ChangeEventsResponse)
    @change_event.paginate()
    @change_event.alt_response(status_code=HTTPStatus.NOT_FOUND, success=False, schema=ChangeEventResponse)
    def get(self, tag_name, pagination_parameters, **kwargs):
        """Tag bilgisi verilen Change Event'in detaylarını görüntülemek için kullanılır"""
        return fetch_change_event_tag(tag_name, pagination_parameters)

@change_event.route("/filters/")
class ChangeEventSearchAll(MethodView):

    @change_event.arguments(ChangeEventSchema, location="json")
    @change_event.response(HTTPStatus.OK, ChangeEventsResponse)
    @change_event.paginate()
    @change_event.alt_response(status_code=HTTPStatus.NOT_FOUND, success=False, schema=ChangeEventResponse)
    def post(self, args, pagination_parameters):
        """ Change Event filtrelemek  için kullanılır (fieldName, tag, username, timeRange)"""
        return search_change_event_with_fieldName_tagName_userName_eventTime(args,pagination_parameters)
