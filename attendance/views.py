from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.timezone import localtime, now

from .models import *
from .utils import *

User = get_user_model()

class DailyRecord(APIView):
    # Note: Attendance can only be recorded of ACTIVE users

    '''
    returns attendance for a particular date with recorded attendance and user who have not yet recorded
    if user_id is provided then, attendance record of that user can be fetched as well.
    query params:
        on_date, user_id(optional)
    response body:
        attendance_record: {
                                date,
                                attendance_records: {
                                                        [
                                                            {
                                                                user_data: {
                                                                                user_id,
                                                                                user_fullname,
                                                                            }
                                                                attendance_data:{
                                                                                    date_of_creation,
                                                                                    time_of_creation,
                                                                                    location_latitude,
                                                                                    location_longitude,
                                                                                    location_string,
                                                                                    location_timestamp,
                                                                                    is_present,
                                                                                    validity_data,
                                                                                }
                                                            },
                                                            ...
                                                        ]   
                                                    },
                            }
    '''
    def get(self,request):
        on_date = request.query_params.get('on_date')
        user_id = request.query_params.get('user_id')

        attendance_record = Attendance.get_user_left_join_attendance_for_date(user_id, on_date)
        if not attendance_record:
            return Response({'details':'Attendance Record Not Found'}, content_type='application/json', status=HTTP_404_NOT_FOUND)
    
        result_set = {
                        'date':on_date,
                        'attendance_records':attendance_record
                    }       
        return Response(result_set, content_type='application/json', status=HTTP_200_OK)

    '''
    accepts location latitude and longitude
    computes the location string
    checks the validity of users using mobile no and saves the attendance data for a user_id that is active and not a superuser
    request body:
        latitude, longitude, location_timestamp, mobile_no, user_id
    response body: 
        201 created
    '''
    def post(self,request):
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        timestamp = request.data.get('location_timestamp')
        mobile_no = request.data.get('mobile_no')
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id = user_id)
        except User.DoesNotExist:
            return Response({'details':'User Not Found'}, content_type='application/json', status=HTTP_404_NOT_FOUND)            
        
        # check if user is active and not super user else he is unauthorized
        if not user.is_active or user.is_superuser:
            return Response({'details':'User is not authorised to mark attendance'}, content_type='application/json', status=HTTP_403_FORBIDDEN)

        # check is already has attendance for current date                
        current_date = localtime(now()).date()
        print(current_date)
        is_record_present = Attendance.objects.filter(user_id=user_id, date_of_creation=current_date).first()
        if is_record_present:
            return Response({'details':'User already has marked attendance for given date'}, content_type='application/json', status=HTTP_403_FORBIDDEN)
        
        # compute location string from latitude, longitude
        try:
            location_string = get_location_string(latitude, longitude)
        except:
            return Response({'details':'Could not retrive Location string'}, content_type='application/json', status=HTTP_404_NOT_FOUND)            

        # check validity using mobile no
        validity_data = user.is_mobile_no_of_user_valid(mobile_no)
        print(validity_data)

        # create attendance object set is_present to true and save
        attendance_record = Attendance.objects.create(
            user = user,
            location_latitude = latitude,
            location_longitude = longitude,
            location_timestamp = timestamp,
            location_string = location_string,
            is_present = True,
            validity_data = validity_data,
        )
        # attendance_record.save()

        return Response({'details':'Attendance Marked'}, content_type='application/json', status=HTTP_201_CREATED)

    # '''
    # updation of user's attendance
    # query params:
    #     user_id
    # requestbody:
    #     (any data that needs to be updated)
    # response body:
    #     200 ok
    # '''
    # def patch(self, request):
    #     user_id = request.query_params.get('user_id')
    #     data_to_be_updated = request.data
        
    #     try:
    #         attendance_record = Attendance.objects.get(user_id = user_id)
    #     except Attendance.DoesNotExist:
    #         return Response({'details':'Attendance Not Found'}, content_type='application/json', status=HTTP_404_NOT_FOUND)

    #     for each_data_key in data_to_be_updated:
    #         attendance_record[each_data_key] = data_to_be_updated[each_data_key]
    #     attendance_record.save()
        
    #     return Response('hi')    
