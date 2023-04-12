from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Apartment(db.Model, SerializerMixin):
    __tablename__ = 'apartments'

    serialize_rules = ('-leases.apartment',)

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    leases = db.relationship('Lease', backref='apartment', cascade='all, delete, delete-orphan')

    @validates('number')
    def validate_number(self, key, number):
        if number < 0:
            raise ValueError("number must be higher than 0")
        return number
    
class Tenant(db.Model, SerializerMixin):
    __tablename__ = 'tenants'

    serialize_rules = ('-leases.tenant',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    leases = db.relationship('Lease', backref='tenant', cascade='all, delete, delete-orphan')

    @validates('age')
    def validate_age(self, key, age):
        if age < 18:
            raise ValueError("Age must be higher than 18")
        return age

class Lease(db.Model, SerializerMixin):
    __tablename__ = 'leases'

    serialize_rules = ('-apartment.leases', '-tenant.leases',)

    id = db.Column(db.Integer, primary_key=True)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))
    rent = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())