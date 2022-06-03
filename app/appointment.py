"""
Appointment utility functions
"""
from datetime import datetime, timedelta
from database.models import Appointment
from flask import abort
from server import db
from utils import *


APPOINTMENT_MINUTE_CHUNK = 15


def get_time_slots(start_time, end_time):
    """
    Get a list of 15 minute time slots for a time interval
    """
    dt_start_time = start_time
    dt_end_time = end_time
    available_date_times = [dt_start_time]
    while dt_start_time < dt_end_time:
        dt_start_time += timedelta(minutes=15)
        available_date_times.append(dt_start_time)
    return available_date_times


def appointment_valid(start_time, end_time):
    """
    Check if appointment start and end time is valid

    If appointment time is not valid, create an error response
    """
    start_time = datetime.fromisoformat(start_time)
    end_time = datetime.fromisoformat(end_time)
    if start_time.minute % APPOINTMENT_MINUTE_CHUNK != 0:
        response = create_response(status_code=405, error='Start time is not in 15 minute chunks')
        abort(response)
    if end_time.minute % APPOINTMENT_MINUTE_CHUNK != 0:
        response = create_response(status_code=405, error='End time is not in 15 minute chunks')
        abort(response)
    if start_time >= end_time:
        response = create_response(status_code=405, error='Start time is later than End')
        abort(response)


def appointment_overlaps(provider_clinic_id_field,
                         provider_clinic_id,
                         provider_first_name_field,
                         provider_first_name,
                         provider_last_name_field,
                         provider_last_name,
                         start_time,
                         end_time):
    """
    Find if apointment overlaps with other provider appointments

    If there is an overlap, create an error response
    """
    appointments_start_overlap = (Appointment.query.filter(db.and_(provider_clinic_id_field.like(provider_clinic_id),
                                                                   provider_first_name_field.like(provider_first_name),
                                                                   provider_last_name_field.like(provider_last_name)))
                                  .filter(db.and_(start_time >= Appointment.start,
                                                  start_time < Appointment.end)).
                                  all())
    if appointments_start_overlap:
        response = create_response(
            status_code=409,
            error='New appointment starts before already booked appointment ends.')
        abort(response)

    appointments_end_overlap = (Appointment.query.filter(db.and_(provider_clinic_id_field.like(provider_clinic_id),
                                                                 provider_first_name_field.like(provider_first_name),
                                                                 provider_last_name_field.like(provider_last_name)))
                                .filter(db.and_(end_time > Appointment.start,
                                                end_time <= Appointment.end)).
                                all())

    if appointments_end_overlap:
        response = create_response(
            status_code=409,
            error='New appointment ends after already booked appointment starts.')
        abort(response)

    appointments_overlap = (Appointment.query.filter(db.and_(provider_clinic_id_field.like(provider_clinic_id),
                                                             provider_first_name_field.like(provider_first_name),
                                                             provider_last_name_field.like(provider_last_name)))
                            .filter(db.and_(start_time < Appointment.start,
                                            end_time > Appointment.end)).
                            all())

    if appointments_overlap:
        response = create_response(
            status_code=409,
            error='New appointment overlaps another already booked appointment')
        abort(response)
