from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Apartment, Tenant, Lease

app = Flask( __name__ )
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///apartments.db'
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

migrate = Migrate( app, db )
db.init_app( app )

api = Api(app)

class ApartmentsController(Resource):
    def get(self):
        return [apartment.to_dict() for apartment in Apartment.query.all()], 200
    def post(self):
        new_apartment = Apartment(number=request.get_json()['number'])
        db.session.add(new_apartment)
        db.session.commit()
        return new_apartment.to_dict(), 201
api.add_resource(ApartmentsController, '/apartments')

class ApartmentControllerByID(Resource):
    def patch(self, id):
        try:
            apartment = Apartment.query.get(id)
            apartment.number = request.get_json()['number']
            db.session.commit()
            return apartment.to_dict(), 200
        except Exception:
            return {'error': 'Could not update specified apartment'}, 404
    
    def delete(self, id):
        try:
            apartment = Apartment.query.get(id)
            db.session.delete(apartment)
            db.session.commit()
            return '', 204
        except Exception:
            return {'error': 'Could not delete specified apartment'}, 404
api.add_resource(ApartmentControllerByID, '/apartments/<int:id>')

class TenantsController(Resource):
    def get(self):
        return [tenant.to_dict() for tenant in Tenant.query.all()], 200
    def post(self):
        new_tenant = Tenant(name=request.get_json()['name'], age=request.get_json()['age'])
        db.session.add(new_tenant)
        db.session.commit()
        return new_tenant.to_dict(), 201
api.add_resource(TenantsController, '/tenants')

class TenantControllerByID(Resource):
    def patch(self, id):
        try:
            tenant = Tenant.query.get(id)
            tenant.name = request.get_json()['name']
            tenant.age = request.get_json()['age']
            db.session.commit()
            return tenant.to_dict(), 200
        except Exception:
            return {'error': 'Could not update specified tenant'}, 404
    
    def delete(self, id):
        try:
            tenant = Tenant.query.get(id)
            db.session.delete(tenant)
            db.session.commit()
            return '', 204
        except Exception:
            return {'error': 'Could not delete specified tenant'}, 404
api.add_resource(TenantControllerByID, '/tenants/<int:id>')

class LeasesController(Resource):
    def get(self):
        return [lease.to_dict() for lease in Lease.query.all()], 200
    def post(self):
        new_lease = Lease(rent=request.get_json()['rent'], apartment_id=request.get_json()['apartment_id'], tenant_id=request.get_json()['tenant_id'])
        db.session.add(new_lease)
        db.session.commit()
        return new_lease.to_dict(), 201
api.add_resource(LeasesController, '/leases')

class LeaseControllerByID(Resource):
    def patch(self, id):
        try:
            lease = Lease.query.get(id)
            lease.rent = request.get_json()['rent']
            db.session.commit()
            return lease.to_dict(), 200
        except Exception:
            return {'error': 'Could not update specified lease'}, 404
    
    def delete(self, id):
        try:
            lease = Lease.query.get(id)
            db.session.delete(lease)
            db.session.commit()
            return '', 204
        except Exception:
            return {'error': 'Could not delete specified lease'}, 404
api.add_resource(LeaseControllerByID, '/leases/<int:id>')

if __name__ == '__main__':
    app.run( port = 5555, debug = True )