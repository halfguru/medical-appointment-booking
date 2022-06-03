"""
The database models representing the tables attributes and relationships
"""

from datetime import datetime

from server import db


class Timestamp(object):
    """
    Timestamp attributes
    """
    created = db.Column(db.DateTime(timezone=False), index=True, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime(timezone=False), onupdate=datetime.utcnow)


class Clinic(Timestamp, db.Model):
    """
    Clinic table with name attribute
    """
    name = db.Column(db.String(100), primary_key=True)

    # Relationships
    patients = db.relationship('Patient', back_populates='clinic')
    providers = db.relationship('Provider', back_populates='clinic')
    appointments = db.relationship('Appointment', back_populates='clinic')


class Patient(Timestamp, db.Model):
    """
    Patient table with first name and last name attributes
    """
    clinic_id = db.Column(db.String(100), db.ForeignKey('clinic.name'), nullable=False)
    first_name = db.Column(db.String(50), primary_key=True)
    last_name = db.Column(db.String(50), primary_key=True)

    __table_args__ = (
        db.PrimaryKeyConstraint(
            'first_name', 'last_name', name='name_pk'
        ),
        {}
    )

    # Relationships
    clinic = db.relationship('Clinic', back_populates='patients')
    appointments = db.relationship('Appointment', back_populates='patients')

    def __repr__(self):
        return f'<Patient {self.first_name} {self.last_name}>'


class Provider(Timestamp, db.Model):
    """
    Provider table with first name and last name attributes
    """
    clinic_id = db.Column(db.String(100), db.ForeignKey('clinic.name'), nullable=False)
    first_name = db.Column(db.String(50), primary_key=True)
    last_name = db.Column(db.String(50), primary_key=True)

    # Relationships
    clinic = db.relationship('Clinic', back_populates='providers')
    appointments = db.relationship('Appointment', back_populates='providers')

    def __repr__(self):
        return f'<Provider {self.first_name} {self.last_name}>'


class Appointment(Timestamp, db.Model):
    """
    Appointment table with id, start, end, patient name and provider name attributes
    """
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime(timezone=False), nullable=False)
    end = db.Column(db.DateTime(timezone=False), nullable=False)
    clinic_id = db.Column(db.String(50), db.ForeignKey('clinic.name'), nullable=False)
    patient_first_name = db.Column(db.String(50), nullable=False)
    patient_last_name = db.Column(db.String(50),  nullable=False)
    provider_first_name = db.Column(db.String(50), nullable=False)
    provider_last_name = db.Column(db.String(50), nullable=False)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['patient_first_name', 'patient_last_name'],
            ['patient.first_name', 'patient.last_name'],
            name='fk_patient'
        ),
        db.ForeignKeyConstraint(
            ['provider_first_name', 'provider_last_name'],
            ['provider.first_name', 'provider.last_name'],
            name='fk_provider'
        ),
        {}
    )

    # Relationships
    clinic = db.relationship('Clinic', back_populates='appointments')
    patients = db.relationship('Patient', back_populates='appointments')
    providers = db.relationship('Provider', back_populates='appointments')

    def __repr__(self):
        return (f'<Appointment {self.patients} with ',
                f'{self.providers} @ {self.start}>')
