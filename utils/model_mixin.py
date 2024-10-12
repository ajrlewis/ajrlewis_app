import datetime

from loguru import logger

from app import db


class ModelMixin:
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=True)

    @property
    def id(self):
        return getattr(self, f"{self.__table__}_id")

    # TODO (ajrl) Filter columns by name and their expected type.
    @classmethod
    def add(cls, data):
        expected_keys = [column.name for column in cls.__table__.columns]
        # expected_types = [type(column) for column in cls.__table__.columns]
        filtered_data = {
            key: value for key, value in data.items() if key in expected_keys
        }
        record = cls(**filtered_data)
        db.session.add(record)
        db.session.commit()
        return record

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # TODO (ajrl) Make sure type of value is correct.
    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                # if type(value) == type(self.getttr(key)):
                setattr(self, key, value)
        db.session.commit()
