"""
Server entry point
"""
from server import app, connexion_app, db
from database.models import Appointment, Patient, Provider

if __name__ == '__main__':
    app.config.update({
        'KONCH_CONTEXT': {
            'db': db,
            'Appointment': Appointment,
            'Patient': Patient,
            'Provider': Provider
        }
    })

    # Add API routings from swagger yaml configuration file
    connexion_app.add_api('swagger.yaml')

    # Create database
    db.create_all()

    # Run our standalone gevent server
    connexion_app.run(host='0.0.0.0', port=8080, server='gevent')
