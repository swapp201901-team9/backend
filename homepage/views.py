from django.shortcuts import render
from django.core.files import File
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
# from .forms import DesignForm, GroupForm
from .models import *
from .serializers import *
from .permissions import *

from base64 import b64decode as decode
import json
import re
# Create your views here.


class AuthList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        content = {
            'status': 'user is authenticated'
        }
        return Response(content)

@api_view(['GET', 'POST','DELETE'])
@permission_classes((IsAuthenticatedOrPOSTOnly,))
def user_list(request):
    if request.method == 'GET':
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # requested data should contain username, password attributes.
        auth = request.data
        try: # if request is bad request, return 400
            username = auth['username']
            pwd = auth['password']
            if len(username)<4 or len(username)>20:
                return Response(status = status.HTTP_400_BAD_REQUEST)
            p = re.compile('\W+')
            if (p.search(username) != None or pwd == ''):
                return Response(status = status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        try: # if there is an user that has same username, return 405
            old_user = User.objects.get(username=username)
            return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)
        except User.DoesNotExist:
            pass
        user = User.objects.create_user(username, password=pwd)
        user.save()
        return Response(status = status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        # requested data should contain username attribute.
        request.user.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['GET','PUT','DELETE'])
def user_detail(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.user.id == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        if user!=request.user:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        serializer = UserSerializer(user,data=request.data)
        if serializer.is_valid():
            # if password is bad, return 400
            pwd=request.data['password']
            if(pwd==''):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if user == request.user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)



@api_view(['GET'])
def profile_list(request):
    if request.user.id==None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    serializer = ProfileSerializer(Profile.objects.all(), many=True)
    if request.method == 'GET':
        return Response(serializer.data)

@api_view(['GET','PUT'])
def profile(request, username):
    context = {'domain': request.META['HTTP_HOST']}
    if request.user.id == None:
        return Response(status= status.HTTP_403_FORBIDDEN)
    try:
        user= User.objects.get(username=username)
        profile=Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer=ProfileSerializer(profile, context=context)
        return Response(serializer.data)
    if request.method == 'PUT':
        if profile.user!= request.user:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        data = request.data
        if 'myimage' in data and data['myimage'] == 'null':
            data['myimage'] = File(open('media/default/defaultImage.jpg', 'rb'))
        serializer = ProfileSerializer(profile, data=data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_403_FORBIDDEN)

def set_default_text(design):
    if design.front_chest_text == None:
        frontchest = Text()
        frontchest.textvalue = "S"
        frontchest.fontFamily = "arial"
        frontchest.fill = "#3f51b5"
        frontchest.fontStyle = "bold"
        frontchest.fontSize = 50
        frontchest.left = 250
        frontchest.top = 110
        frontchest.stroke = "#000000"
        frontchest.strokeWidth = 2
        design.front_chest_text = frontchest
    
    if design.right_arm_text == None:
        rightarm = Text()
        rightarm.textvalue = "19"
        rightarm.fontFamily = "arial"
        rightarm.fill = "#607d8b"
        rightarm.fontStyle = "bold"
        rightarm.fontSize = 50
        rightarm.left = 50
        rightarm.top = 120
        rightarm.stroke = ""
        rightarm.strokeWidth = 0
        design.right_arm_text = rightarm

    if design.upper_back_text == None:
        upperback = Text()
        upperback.textvalue = "SEOUL NAT'L"
        upperback.fontFamily = "arial"
        upperback.fill = "#ffc107"
        upperback.fontStyle = "bold"
        upperback.fontSize = 25
        upperback.left = 135
        upperback.top = 125
        upperback.stroke = ""
        upperback.strokeWidth = 0
        design.upper_back_text = upperback

    if design.middle_back_text == None:
        middleback = Text()
        middleback.textvalue = "UNIVERSITY"
        middleback.fontFamily = "arial"
        middleback.fill = "#ffc107"
        middleback.fontStyle = "bold"
        middleback.fontSize = 20
        middleback.left = 155
        middleback.top = 155
        middleback.stroke = ""
        middleback.strokeWidth = 0
        design.middle_back_text = middleback

    if design.lower_back_text == None:
        lowerback = Text()
        lowerback.textvalue = "UNIVERSITY"
        lowerback.fontFamily = "arial"
        lowerback.fill = "#ffc107"
        lowerback.fontStyle = "bold"
        lowerback.fontSize = 15
        lowerback.left = 150
        lowerback.top = 190
        lowerback.stroke = ""
        lowerback.strokeWidth = 0
        design.lower_back_text = lowerback

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrGETDELETEOnly,))
def main(request):    
    if request.method == 'GET':
        # check if user is logged in
        if request.user.id == None: 
            design = Design()
        else:
            try:
                user = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)    

            design = user.recent
            # if there is no design user is working on, create a new one
            if design == None:
                design = Design()
                design.owner = request.user
                design.group = user.user_group
                design.save()
                user.recent = design
                user.save()
        set_default_text(design)
        design_serializer = UserDesignSerializer(design)
        return Response(design_serializer.data)
    
    # saves design to user group
    if request.method == 'PUT':
        try:
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)    

        data = json.loads(request.body.decode("utf-8")) 
        design_id=data['id']
        if design_id != user.recent.id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.recent.body=data['detail_body']
        user.recent.sleeve=data['detail_sleeve']
        user.recent.button=data['detail_buttons']
        user.recent.banding=data['detail_banding']
        user.recent.stripe=data['detail_stripes']
        user.recent.save()
        design_serializer = UserDesignSerializer(user.recent)
        return Response(design_serializer.data)

    # doesn't really delete design but saves it in user group
    # needs to be deleted in user group detail
    if request.method == 'DELETE':
        if request.user.id == None: 
            design = Design()
        else:    
            try:
                user = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            design = Design()
            design.owner = request.user
            design.group = user.user_group
            design.save()
            user.recent = design
            user.save()
            
        set_default_text(design)
        design_serializer = UserDesignSerializer(design)
        return Response(design_serializer.data)

    # # save design and copys design to requested group
    # if request.method == 'POST':
    #     design_id=request.data['id']
    #     if design_id != user.recent.id:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #     user.recent.detail_body=request.data['detail_body']
    #     user.recent.detail_sleeve=request.data['detail_sleeve']
        # user.recent.detail_buttons=request.data['detail_buttons']
        # user.recent.detail_banding=request.data['detail_banding']
        # user.recent.detail_stripes=request.data['detail_stripes']
    #     user.recent.save()

    #     try:
    #         group = Group.objects.get(id=request.data['group'])
    #     except Group.DoesNotExist:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #     if request.user not in group.users.all():
    #         return Response(status=status.HTTP_403_FORBIDDEN)
        
    #     post_design=Design()
    #     post_design.owner = request.user
    #     post_design.group = group
    #     post_design.detail_body = request.data['detail_body']
    #     post_design.detail_sleeve = request.data['detail_sleeve']
    # post_design.detail_buttons=request.data['detail_buttons']
        # post_design.detail_banding=request.data['detail_banding']
        # post_design.detail_stripes=request.data['detail_stripes']
    #     post_design.save()

    #     design_serializer = UserDesignSerializer(user.recent)
    #     return Response(design_serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticatedOrNothing,))
def post_design(request, group_id, design_id):
    # copys design to requested group
    if request.method == 'GET':
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.user not in group.users.all():
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        try:
            design = Design.objects.get(id=design_id)
        except Design.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)        

        post_design=Design()
        post_design.owner = request.user
        post_design.group = group
        post_design.body = design.detail_body
        post_design.sleeve = design.detail_sleeve
        post_design.button = design.detail_buttons
        post_design.banding = design.detail_banding
        post_design.stripe = design.detail_stripes
        post_design.save()

        design_serializer = UserDesignSerializer(post_design)
        return Response(design_serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticatedOrNothing,))
def group_detail(request, group_id):
    if request.method == 'GET':
        if request.user.id == None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(username=request.user)
        except User.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if user not in group.users.all():
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        try:
            designs = Design.objects.all().filter(group=group).order_by('likes').reverse()
        except Design.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        design_serializer = GroupDesignSerializer(designs, user=request.user, many=True)
        
        return Response(design_serializer.data)

@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticatedOrGETOnly,))
def create_group(request):
    # if request.method == 'GET':
    #     try:
    #         groups = Group.objects.all()
    #     except Group.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     group_serializer = GroupSerializer(groups, many=True)
    #     context = {
    #         'form': GroupForm(),
    #         'groupList': group_serializer.data
    #     }
    #     return render(request, 'main/create_group.html', context)

    if request.method == 'POST':
        if request.user.id == None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(username=request.user)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        data = json.loads(request.body.decode("utf-8"))
        
        try: # if there is a group that has same groupname, return 409
            old_group = Group.objects.get(group_name = data['groupname'])
            return Response(status = status.HTTP_409_CONFLICT)
        except Group.DoesNotExist:
            pass
        
        group = Group()
        group.group_type = data['grouptype']
        group.group_name = data['groupname']
        group.save()
        group.users.add(user)
        group.master.add(user)
        group_serializer = GroupSerializer(group)
        return Response(group_serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticatedOrNothing,))
def group_list(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.user.id == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if request.method == 'GET':
        try:
            groups = Group.objects.filter(users__username=username)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        group_serializer = GroupSerializer(instance=groups, user=user, many=True)
        return Response(group_serializer.data)  

@api_view(['GET'])
@permission_classes((IsAuthenticatedOrNothing,))
def join_group(request, group_id):
    if request.method == 'GET':
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.user.id == None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(username=request.user)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        group.users.add(user)
        group_serializer = GroupSerializer(group)
        return Response(group_serializer.data)

@api_view(['GET'])
def group_list_all(request):
    if request.method == 'GET':
        try:
            groups = Group.objects.all().exclude(group_type='UR').order_by('created_at').reverse()
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        group_serializer = GroupSerializer(instance=groups, user=request.user, many=True)
        return Response(group_serializer.data)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrNothing,))
def update_group(request, group_id):
    if request.user.id == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if user not in group.users.all():
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        groups = Group.objects.filter(id=group_id)
        group_serializer = GroupSerializer(instance=groups, many=True)
        return Response(group_serializer.data)

    if user not in group.master.all():
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        group_name=request.data['group_name']
        group_type=request.data['group_type']

        if group_type=='UR':
            return Response(status = status.HTTP_403_FORBIDDEN)
        try: # if there is a group that has same groupname, return 409
            old_group = Group.objects.get(group_name = group_name)
            return Response(status = status.HTTP_409_CONFLICT)
        except Group.DoesNotExist:
            pass
        
        group.group_type = group_type
        group.group_name = group_name
        group.save()
        
        groups = Group.objects.filter(id=group_id)
        group_serializer = GroupSerializer(instance=groups, many=True)
        return Response(group_serializer.data)

    if request.method == 'DELETE':
        group.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((IsAuthenticatedOrNothing,))
def member_list(request, group_id):
    if request.user.id == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if user not in group.master.all():
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        member_serializer = MemberSerializer(instance=group.users, group=group, many=True)
        return Response(member_serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticatedOrNothing,))
def update_member(request, group_id, user_id):
    if request.user.id == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.user not in group.master.all():
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if target_user not in group.users.all():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        return Response(status=status.HTTP_200_OK)
    if request.method == 'PUT':
        if target_user not in group.master.all():
            group.master.add(target_user)
    
    if request.method == 'DELETE':
        if target_user == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        group.users.remove(target_user)
        if target_user in group.master.all():
            group.master.remove(target_user)
    
    member_serializer = MemberSerializer(instance=group.users, group=group, many=True)
    return Response(member_serializer.data)

@api_view(['GET',])
@permission_classes((IsAuthenticatedOrNothing,))
def drop_group(request, group_id):
    if request.user.id == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.user not in group.users.all():
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        if request.user in group.master.all() and group.master.all().count()<=1:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        group.users.remove(request.user)
        if request.user in group.master.all():
            group.master.remove(request.user)
    
    return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
@permission_classes((IsAuthenticatedOrNothing,))
def update_likes(request, design_id):
    if request.method == 'GET':
        if request.user.id == None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(username=request.user)
        except User.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        try:
            design = Design.objects.get(id=design_id)
        except Design.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.user not in design.group.users.all():
            return Response(status=status.HTTP_403_FORBIDDEN)
        if request.user in design.who.all():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        
        design.who.add(user)
        design.likes = design.likes + 1
        design.save()
        design_serializer = UserDesignSerializer(design)
        return Response(design_serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticatedOrNothing,))
def undo_likes(request, design_id):
    if request.method == 'GET':
        if request.user.id == None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(username=request.user)
        except User.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        try:
            design = Design.objects.get(id=design_id)
        except Design.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.user not in design.group.users.all():
            return Response(status=status.HTTP_403_FORBIDDEN)
        if request.user not in design.who.all():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        
        design.who.remove(user)
        design.likes = design.likes - 1
        design.save()
        design_serializer = UserDesignSerializer(design)
        return Response(design_serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticatedOrNothing,))
def design_list(request, group_id):
    if request.method == 'GET':
        try:
            designs = Design.objects.filter(group__id=group_id)
        except Design.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        design_serializer = GroupDesignSerializer(designs, many=True)
        return Response(design_serializer.data)  

@api_view(['GET'])
@permission_classes((IsAuthenticatedOrNothing,))
def delete_design(request, design_id):
    if request.method == 'GET':
        if request.user.id == None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(username=request.user)
        except User.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        try:
            design = Design.objects.get(id=design_id)
        except Design.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.user not in design.group.master.all() and request.user != design.owner:
            return Response(status=status.HTTP_403_FORBIDDEN)
    
        design.delete()

        return Response(status=status.HTTP_200_OK)