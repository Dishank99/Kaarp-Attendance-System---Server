from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from .models import *
from .serializers import *

from datetime import datetime


#API for user validation
class ValidateUser(APIView):
    '''
    validates user against email of mobile_no and returns user info and also updated device id
    user should not be a superuser, should be active(which sginifies that he/she is approved)
    device_id should also be mentioned in request body, so that it is updated every time
    reuqest body:
        credential (email/mobile_no)
    reponse body:
        id, fname, lname, date_of_joining, role, device_id, email, mobile_no
    '''
    def post(self,request):
        credential = request.data.get('credential')
        user_type = request.data.get('type')
        device_id = request.data.get('device_id')
        try:
            validated_user = KaarpUser.objects.get(
                                    Q(email=credential)|Q(mobile_no=credential),
                                    is_superuser=False, is_active=True,
                                    )
        except KaarpUser.DoesNotExist:
            return Response({'details':'User not Found'}, content_type='application/json', status=HTTP_404_NOT_FOUND)
        else:
            # update device id
            validated_user.device_id = device_id
            validated_user.save()
            result_set = {
                            'user':UserSerializer(validated_user).data
                        }
        
        return Response(result_set, content_type='application/json', status=HTTP_200_OK)

# API for user requests management
class UserRequests(APIView):
    '''
    returns all the pending requests for a particualr user type
    if a data range is passed then the requests between those days will be returns else all the requests will be returned
    query params:
        from_date, to_date, user_type
    response body:
        fname, lname, email, mobile_no, date_of_request, role
    '''
    # Note: No need to check for super user as a super user wont be sending request
    def get(self,request):
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        user_type = request.query_params.get('user_type')
        if not user_type:
            return Response({'details':'Please mention the user_type'}, content_type='application/json', status=HTTP_400_BAD_REQUEST)

        pending_requests = KaarpUser.objects.filter(role__role=user_type, is_approved=False, is_active=False, is_superuser=False)

        if from_date and to_date:
            from_date = datetime.strptime(from_date, '%Y-%m-%d')
            to_date = datetime.strptime(to_date, '%Y-%m-%d') 
            pending_requests = pending_requests.filter(datetime_of_request__range=(from_date, to_date))

        result_set = {'requests':UserRequestSerializer(pending_requests,many=True).data}

        return Response(result_set, content_type='application/json', status=HTTP_200_OK)

    '''
    creates a new request for registration
    user type has to be mentioned so that request is categorized according to it
    request body:
        fname, lname, email, mobile_no, user_type
    reponse body:
        200 ok
    '''
    def post(self,request):
        fname = request.data.get('fname')
        lname = request.data.get('lname')
        email = request.data.get('email')
        mobile_no = request.data.get('mobile_no')
        user_type = request.data.get('user_type')

        if fname and lname and email and mobile_no and user_type:
            try:
                role_for_given_user_type = UserRoles.objects.get(role = user_type)
            except UserRoles.DoesNotExists:
                return Response({'details':'Please mention the correct user_type'}, content_type='application/json', status=HTTP_400_BAD_REQUEST)
            
            # checks if request for given email and mobile no is present, if yes than the object is stored in request
            # and is_created is True
            # if not then is_created is false ans created object with give email and mobile no along with data ni 'dafaults' is stored in request
            request, is_created = KaarpUser.objects.get_or_create(
                email=email, mobile_no=mobile_no, 
                defaults={
                    'fname': fname, 'lname': lname, 
                    'role' : role_for_given_user_type
                }
            )
            if is_created:
                request_data = UserRequestSerializer(request).data
                return Response({'details':'Request Created', 'request_data':request_data}, content_type='appication/json',status=HTTP_20O_OK)
                
            else:
                return Response({'details':'Request for this email and mobile no is already present'}, 
                                content_type='application/json', status=HTTP_409_CONFLICT)
        else:
            return Response({'details':'Please mention the complete request'}, content_type='application/json', status=HTTP_400_BAD_REQUEST)
        
    '''
    updates the request from pending to approved
    set is_approved flag and is_active flag to true and sets the datetime_of_activation as current datetime
    query_param:
        id
    response body:
        200 ok
    ''' 
    # Note: No need to check for super user as a super user wont be sending request       
    def patch(self,request):
        user_id = request.query_params.get('id')
        if not user_id:
            return Response({'details':'Please mention the user_id'}, content_type='application/json', status=HTTP_400_BAD_REQUEST)
        
        try:
            pending_request = KaarpUser.objects.get(id=user_id)
        except KaarpUser.DoesNotExist:
            return Response({'details':'Please mention the correct id'}, content_type='application/json', status=HTTP_404_NOT_FOUND)

        # set is_approved flag and is_active flag to true and sets the datetime_of_activation as current datetime
        if pending_request.is_approved and pending_request.is_active:
            request_data = UserRequestSerializer(pending_request).data
            return Response({'details':'Request is already Approved', 'request_data':request_data}, content_type='appication/json',status=HTTP_200_OK)
        pending_request.is_approved = True
        pending_request.is_active = True
        pending_request.datetime_of_activation = datetime.now()
        pending_request.set_password(pending_request.mobile_no)
        pending_request.save()

        request_data = UserRequestSerializer(pending_request).data
        return Response({'details':'Request Approved', 'request_data':request_data}, content_type='appication/json',status=HTTP_201_CREATED)

    '''
    deletes the PENDING request
    first checks if its not prroved and user is not active
    query param:
        id
    response body:
        204 no content
    '''
    # Note: No need to check for super user as a super user wont be sending request
    def delete(self,request):
        user_id = request.query_params.get('id')
        if not user_id:
            return Response({'details':'Please mention the user_id'}, content_type='application/json', status=HTTP_400_BAD_REQUEST)
        
        try:
            pending_request = KaarpUser.objects.get(id=user_id)
        except KaarpUser.DoesNotExist:
            return Response({'details':'Please mention the correct id'}, content_type='application/json', status=HTTP_404_NOT_FOUND)
        
        if pending_request.is_approved and pending_request.is_active:
            return Response({'details':'Request is approved. Its not pending anymore'}, content_type='application/json', status=HTTP_400_BAD_REQUEST)

        pending_request.delete()
        return Response({'details':'Request Deleted'}, content_type='appication/json',status=HTTP_204_NO_CONTENT)
