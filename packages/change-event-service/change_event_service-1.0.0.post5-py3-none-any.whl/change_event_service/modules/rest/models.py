import os
from ...database import db


class LogModel:
    userName = ""

    def __init__(self, userName):
        self.userName = userName

    def __repr__(self):
        return 'Change Event %r' % self.id


class ChangeEventModel(db.Model):
    __tablename__ = 'tbl_audit_log'
    id = db.Column(db.BigInteger, primary_key=True)
    ip = db.Column(db.String)
    user_id = db.Column(db.String)
    new_value = db.Column(db.String)
    object_id = db.Column(db.BigInteger)
    old_value = db.Column(db.String)
    user_name = db.Column(db.String)
    event_time = db.Column(db.TIMESTAMP)
    field_name = db.Column(db.String)
    object_name = db.Column(db.String)
    tag = db.Column(db.String)


    def __init__(self, ip, user_id, new_value, object_id, old_value, user_name, event_time,event_type, field_name, object_name, tag):
        self.ip = ip
        self.user_id = user_id
        self.new_value = new_value
        self.object_id = object_id
        self.old_value = old_value
        self.user_name = user_name
        self.event_time = event_time
        self.event_type = event_type
        self.field_name = field_name
        self.object_name = object_name
        self.tag = tag


    def __repr__(self):
        return 'Change Event %r' % self.id
