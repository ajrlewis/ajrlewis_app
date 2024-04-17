from app import db


class ModelMixin:
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
