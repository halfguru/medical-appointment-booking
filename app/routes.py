"""
API routes defining the REST commands actions
"""
from appointment import *
from utils import *
from datetime import datetime, timedelta
from server import db
from database.models import Appointment, Patient, Provider
from database.schemas import ProviderSchema


def get_provider(clinic_id, first_name, last_name):
    """
    Get single provider given clinic id and provider name
    """
    all_providers_filtered = Provider.query.filter(db.and_(Provider.clinic_id.like(clinic_id),
                                                           Provider.first_name.like(first_name),
                                                           Provider.last_name.like(last_name))).all()
    if not all_providers_filtered:
        return create_response(status_code=404, error="Provider doesn't exist")
    result = ProviderSchema(many=True).dump(all_providers_filtered)[0]
    return result


def get_providers(clinic_id):
    """
    Get all providers given clinic id
    """
    all_providers_filtered = Provider.query.filter(Provider.clinic_id.like(clinic_id)).all()
    if not all_providers_filtered:
        return create_response(status_code=404, error="No providers exist")
    result = ProviderSchema(many=True).dump(all_providers_filtered)
    return create_response(status_code=200, data_field="providers", data=result)


def put_appointment(clinic_id,
                    patient_first_name,
                    patient_last_name,
                    provider_first_name,
                    provider_last_name,
                    start_time,
                    end_time):
    """
    Patient book appointment for a given provider and time interval
    """
    # Check if provider exist
    all_providers_filtered = Provider.query.filter(db.and_(Provider.clinic_id.like(clinic_id),
                                                           Provider.first_name.like(provider_first_name),
                                                           Provider.last_name.like(provider_last_name))).all()

    if not all_providers_filtered:
        return create_response(status_code=404, error="Provider doesn't exist")

    all_patients_filtered = Patient.query.filter(db.and_(Patient.clinic_id.like(clinic_id),
                                                         Patient.first_name.like(patient_first_name),
                                                         Patient.last_name.like(patient_last_name))).all()

    # Check if patient exist
    if not all_patients_filtered:
        new_patient = Patient(clinic_id=clinic_id,
                              first_name=patient_first_name,
                              last_name=patient_last_name,
                              created=datetime.now(),
                              updated=datetime.now())
        db.session.add(new_patient)

    # Check if start and end time is valid
    appointment_valid(start_time, end_time)

    # Check if appointment time overlaps with provider other appointments
    appointment_overlaps(Appointment.clinic_id,
                         clinic_id,
                         Appointment.provider_first_name,
                         provider_first_name,
                         Appointment.provider_last_name,
                         provider_last_name,
                         start_time,
                         end_time)

    # Create appointment
    new_appointment = Appointment(clinic_id=clinic_id,
                                  start=datetime.fromisoformat(start_time),
                                  end=datetime.fromisoformat(end_time),
                                  patient_first_name=patient_first_name,
                                  patient_last_name=patient_last_name,
                                  provider_first_name=provider_first_name,
                                  provider_last_name=provider_last_name,
                                  created=datetime.now(),
                                  updated=datetime.now())
    db.session.add(new_appointment)
    db.session.commit()

    return create_response(status_code=200, data="New appointment created")


def get_availabilities(clinic_id,
                       provider_first_name,
                       provider_last_name,
                       start_time,
                       end_time):
    """
    Get all available time slots given clinic id, provider name and time interval
    """
    # Check if provider exist
    all_providers_filtered = Provider.query.filter(db.and_(Provider.clinic_id.like(clinic_id),
                                                           Provider.first_name.like(provider_first_name),
                                                           Provider.last_name.like(provider_last_name))).all()

    if not all_providers_filtered:
        return create_response(status_code=404, error="Provider doesn't exist")

    # Check if start and end time is valid
    appointment_valid(start_time, end_time)

    # Get all available time slots given the time interval input
    available_date_times = get_time_slots(datetime.fromisoformat(start_time), datetime.fromisoformat(end_time))

    all_appointments_filtered = (Appointment.query.filter(db.and_(Appointment.clinic_id.like(clinic_id),
                                                                  Appointment.provider_first_name.like(provider_first_name),
                                                                  Appointment.provider_last_name.like(provider_last_name))).all())

    # Get all unavailable time slots from current appointments
    unavailable_date_times = []
    for appointment_filtered in all_appointments_filtered:
        dt_start_time = appointment_filtered.start
        dt_end_time = appointment_filtered.end
        unavailable_date_times = get_time_slots(dt_start_time, dt_end_time)

    # Get all available time slots given current appointments
    available_date_times = [x for x in available_date_times if x not in unavailable_date_times]
    available_date_times = [x.strftime('%Y-%m-%d %H:%M:%S') for x in available_date_times]

    return create_response(status_code=200, data_field="availabilities", data=available_date_times)
