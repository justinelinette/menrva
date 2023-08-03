from datetime import datetime
from utils.exts import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())

    @classmethod
    def create(cls, **kwargs):
        record = cls(**kwargs)
        db.session.add(record)
        db.session.commit()
        return record

    @classmethod
    def read(cls, record_id):
        return cls.query.get(record_id).first()

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
