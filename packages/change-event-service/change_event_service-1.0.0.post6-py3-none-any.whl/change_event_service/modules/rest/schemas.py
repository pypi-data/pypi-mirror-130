from marshmallow import Schema, fields


class BaseResponse(Schema):
    data = fields.Dict()
    message = fields.String()
    statusCode = fields.String()
    exceptionDetail = fields.String()

    class Meta:
        ordered = True


class ChangeEventSchema(BaseResponse):
    id = fields.Integer(dump_only=True)
    ip = fields.String()
    user_id = fields.String()
    new_value = fields.String()
    object_id = fields.String()
    old_value = fields.String()
    user_name = fields.String()
    event_time = fields.DateTime()
    event_type = fields.String()
    field_name = fields.String()
    object_name = fields.String()
    tag = fields.String()
    time_range = fields.List(fields.String())


class ChangeEventSearch(ChangeEventSchema):
    id = fields.String(dump_only=True)


class Pagination(Schema):
    page = fields.Integer()
    total_pages = fields.Integer()
    total = fields.Integer()


class ChangeEventResponse(BaseResponse):
    data = fields.Nested(ChangeEventSchema)
    page = fields.Nested(Pagination)


class ChangeEventsResponse(ChangeEventResponse):
    data = fields.Nested(ChangeEventSchema, many=True)
