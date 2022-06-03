"""
The database tables json serialization schemas 
"""
from server import ma
from .models import Appointment, Clinic, Patient, Provider


class ClinicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Clinic
        load_instance = True


class AppointmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment
        load_instance = True


class PatientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Patient
        load_instance = True


class ProviderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Provider
        load_instance = True
