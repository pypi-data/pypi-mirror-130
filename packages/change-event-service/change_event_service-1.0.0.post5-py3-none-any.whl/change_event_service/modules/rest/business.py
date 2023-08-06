import traceback
from datetime import datetime
from flask_smorest import abort
from flask_sqlalchemy import Pagination
from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound
from http import HTTPStatus
from ...database import db
from ...modules.rest.models import ChangeEventModel
from ...modules.rest.utils import ResponseObject, PaginationObject

def pika_create_change_event(data):
    if(hasattr(data,'user_id') == False):
        pass
    else:
        data['user_id'] = str(data['user_id'])
        change_event = ChangeEventModel(ip=data['ip'],user_id=data['user_id'], new_value=data['new_value'],object_id=data['object_id'], old_value=data['old_value']
                                    ,user_name=data['user_name'],event_time=data['event_time'], event_type=data['event_type'],field_name=data['field_name']
                                    ,object_name=data['object_name'], tag=data['tag'])
        db.session.add(change_event)
        db.session.commit()



def create_change_event(args):
    ip = args.get('ip')
    user_id = args.get('user_id')
    new_value = args.get('new_value')
    object_id = args.get('object_id')
    old_value = args.get('old_value')
    user_name = args.get('user_name')
    event_time = args.get('event_time')
    event_type = args.get('event_type')
    field_name = args.get('field_name')
    object_name = args.get('object_name')
    tag = args.get('tag')

    change_event = ChangeEventModel(ip=ip,user_id=user_id,new_value=new_value,object_id=object_id,old_value=old_value,user_name=user_name,event_time=event_time,event_type=event_type,
                                    field_name=field_name,object_name=object_name,tag=tag)
    db.session.add(change_event)
    db.session.commit()
    return ResponseObject(message="Change Event is successfully created.", status=HTTPStatus.OK)


def search_change_event_with_fieldName_tagName_userName_eventTime(args, pagination_parameters):
    user_name = args.get('user_name')
    event_time = args.get('event_time')
    field_name = args.get('field_name')
    change_event_tag = args.get('tag')
    time_range = args.get('time_range')
    timeRange1 = time_range[0]
    timeRange2 = time_range[1]

    date_time_obj1 = datetime.strptime(timeRange1, '%Y-%m-%d %H:%M:%S.%f').date()

    date_time_obj2 = datetime.strptime(timeRange2, '%Y-%m-%d %H:%M:%S.%f').date()
    tagList = change_event_tag.split(",")

    try:
        for x in tagList:
            _response = ChangeEventModel.query.filter(and_(ChangeEventModel.tag.contains(x),
                ChangeEventModel.field_name == field_name, ChangeEventModel.user_name == user_name),
                                                      (ChangeEventModel.event_time >= date_time_obj1), ChangeEventModel.event_time <= date_time_obj2).paginate(pagination_parameters.page,
                                                                             pagination_parameters.page_size)
    except NoResultFound as e:
        abort(HTTPStatus.NOT_FOUND, message="Change Event is not found", exc=e)
    pagination_parameters.item_count = _response.total
    a = _response.items
    return ResponseObject(data=_response.items, page=PaginationObject(page=_response.page, total_pages=_response.pages,
                                                                      total=_response.total), status=HTTPStatus.OK)


def search_change_event(args, pagination_parameters):
    ip = args.get('ip')
    user_id = args.get('user_id')
    new_value = args.get('new_value')
    object_id = args.get('object_id')
    old_value = args.get('old_value')
    user_name = args.get('user_name')
    event_time = args.get('event_time')
    event_type = args.get('event_type')
    field_name = args.get('field_name')
    object_name = args.get('object_name')
    tag = args.get('tag')

    _response = ChangeEventModel.query.filter(
        and_(ChangeEventModel.ip == ip, ChangeEventModel.user_id == user_id, ChangeEventModel.new_value == new_value,
             ChangeEventModel.object_id == object_id, ChangeEventModel.old_value == old_value,
             ChangeEventModel.user_name == user_name,
             ChangeEventModel.event_time == event_time, ChangeEventModel.event_type == event_type,
             ChangeEventModel.field_name == field_name,
             ChangeEventModel.object_name == object_name, ChangeEventModel.tag == tag
             )).paginate(pagination_parameters.page,
                         pagination_parameters.page_size)
    pagination_parameters.item_count = _response.total
    return ResponseObject(data=_response.items, page=Pagination(page=_response.page, total_pages=_response.pages,
                                                                total=_response.total),
                          status=HTTPStatus.OK)


def fetch_change_event(change_event_id):
    try:
        _response = ChangeEventModel.query.filter(
            ChangeEventModel.id == change_event_id).one()
    except NoResultFound as e:
        abort(HTTPStatus.NOT_FOUND, message="Change Event is not found", exc=e)

    return ResponseObject(data=_response, status=HTTPStatus.OK)


def fetch_change_event_field_name(change_event_field_name, pagination_parameters):
    try:
        _response = ChangeEventModel.query.filter(
            ChangeEventModel.field_name == change_event_field_name).paginate(pagination_parameters.page,
                                                                             pagination_parameters.page_size)
    except NoResultFound as e:
        abort(HTTPStatus.NOT_FOUND, message="Change Event is not found", exc=e)
    pagination_parameters.item_count = _response.total
    return ResponseObject(data=_response.items, page=PaginationObject(page=_response.page, total_pages=_response.pages,
                                                                      total=_response.total), status=HTTPStatus.OK)


def fetch_change_event_tag(change_event_tag, pagination_parameters):
    tagList = change_event_tag.split(",")
    try:
        for x in tagList:
            _response = ChangeEventModel.query.filter(ChangeEventModel.tag.contains(x)).paginate(
                pagination_parameters.page,
                pagination_parameters.page_size)
    except NoResultFound as e:
            abort(HTTPStatus.NOT_FOUND, message="Change Event is not found", exc=e)
    pagination_parameters.item_count = _response.total
    return ResponseObject(data=_response.items, page=PaginationObject(page=_response.page, total_pages=_response.pages,
                                                                      total=_response.total), status=HTTPStatus.OK)


def update_change_event(change_event_id, args):
    try:
        change_event = ChangeEventModel.query.filter(ChangeEventModel.id == change_event_id).one()
    except NoResultFound as e:
        abort(HTTPStatus.NOT_FOUND, message="Change Event is not found", exc=e)
    try:
        log = args.get("log")
        change_event.log = log
        db.session.add(change_event)
        db.session.commit()
    except Exception as e:
        tb = traceback.format_exc()
        abort(HTTPStatus.BAD_GATEWAY, message="Change Event is not found", messages=tb, exc=e)

    return ResponseObject(message="Change Event is successfully updated.", status=HTTPStatus.OK)


def delete_change_event(change_event_id):
    try:
        change_event = ChangeEventModel.query.filter(ChangeEventModel.id == change_event_id).one()
    except NoResultFound as e:
        abort(HTTPStatus.NOT_FOUND, message="Change Event is not found", exc=e)

    try:
        db.session.delete(change_event)
        db.session.commit()
    except Exception as e:
        abort(HTTPStatus.BAD_GATEWAY, message="Change Event could not deleted.", exc=e)

    return ResponseObject(message="Change Event is successfully deleted")
