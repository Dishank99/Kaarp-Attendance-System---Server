from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import json

User = get_user_model()

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    date_of_creation = models.DateField(auto_now_add=True)
    time_of_creation = models.TimeField(auto_now_add=True)
    
    date_of_updation = models.DateField(auto_now=True)
    time_of_updation = models.TimeField(auto_now_add=True)
    
    location_latitude = models.DecimalField(max_digits=10, decimal_places=8)
    location_longitude = models.DecimalField(max_digits=10, decimal_places=8)
    location_timestamp = models.PositiveIntegerField()
    location_string = models.CharField(max_length=150, null=True, blank=True)
    is_present = models.BooleanField(default=False)
    validity_data = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'Attendance of {self.user} on {self.date_of_creation}'

    @staticmethod
    def get_user_left_join_attendance_for_date(user_id, on_date):
        print(user_id)
        if user_id:
            query = f'SELECT * FROM users_KaarpUser U LEFT JOIN attendance_Attendance A ON U.ID = A.user_id where U.ID = {user_id}'    
        else:
            query = f'SELECT * FROM users_KaarpUser U LEFT JOIN attendance_Attendance A ON U.ID = A.user_id'
        attendance_record = Attendance.objects.raw(query)
        print('reached here',attendance_record.query)
        # print(attendance_record[0])
        res = []
        
        for data in attendance_record:
            if str(data.date_of_creation) == on_date:
                print(data.user_id)
                temp_user_data = {
                                    'user_id':data.user_id, 
                                    'fname':data.fname, 
                                    'lname':data.lname
                                }
                print(temp_user_data)
                temp_attendance_data = {
                                            'attendance_id':data.id,
                                            'date_of_creation':str(data.date_of_creation),
                                            'time_of_creation':str(data.time_of_creation),
                                            'location_latitude':str(data.location_latitude),
                                            'location_longitude':str(data.location_longitude),
                                            'location_string':data.location_string,
                                            'location_timestamp':str(data.location_timestamp),
                                            'is_present':data.is_present,
                                            'validity_data':data.validity_data
                                        } if data.date_of_creation else None
                res.append(
                        {
                            'user_data': temp_user_data,
                            'attendance_record': temp_attendance_data
                        }
                    )
        print('reached here')
        if len(res) == 1: res = res[0]
        return json.loads(json.dumps(res))