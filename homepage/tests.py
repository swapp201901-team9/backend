from django.test import TestCase, Client
from django.http.request import HttpRequest
from django.http.cookie import SimpleCookie
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from .models import Group
from .views import *

from base64 import b64encode as encode
import io

#################### Test Login Page ####################

class UserJoinCase(TestCase):
    def test_join(self):
        try: # if there is an user that has same username, test fails(unlikely)
            user = User.objects.get(username='user01')
            self.assertEqual(1, 2)
        except User.DoesNotExist:
            pass
        response = self.client.post('/users/', {'username': 'user01', 'password': 'pass'})
        self.assertEqual(response.status_code//100, 2)
        
        ## User Object Check
        try:
            user = User.objects.get(username='user01')
        except User.DoesNotExist:
            self.assertEqual(1, 2)
        self.assertEqual(user.username, 'user01')
        self.assertFalse(user.id==None)
        
        ## User Group Check
        try:
            group = Group.objects.get(group_name='user_group_user01')
        except User.DoesNotExist:
            self.assertEqual(1, 2)
        self.assertEqual(group.group_type, 'UR')
        self.assertEqual(group.group_name, 'user_group_user01')
        self.assertTrue(user in group.master.all())
        self.assertFalse(group.id==None)
        

        ## Profile Object Check
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            self.assertEqual(1, 2)
        self.assertEqual(profile.user.username, 'user01')
        self.assertTrue(profile.recent==None)
        self.assertTrue(group in profile.groups.all())

class UserLoginCase(TestCase):
    def setUp(self):
        response = self.client.post('/users/', {'username': 'user02', 'password': 'pass'})
    
    def test_login(self):
        # Check if logged in successfully
        credentials = encode(b'user02:pass')
        response = self.client.get('/auth/', HTTP_AUTHORIZATION='Basic ' + credentials.decode())
        self.assertEqual(response.status_code//100, 2)
        

#################### Test Main Page ####################

class GetEmptyDesignCase(TestCase):
    def setUp(self):
        self.client.post('/users/', {'username': 'user03', 'password': 'pass'})

    def test_default_attributes(self):
        """empty design objects have default values"""
        response = self.client.get('/')
        self.assertEqual(response.status_code//100, 2)
        response.render()
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(data['detail_sleeve'], '#fcfcfc')
        self.assertEqual(data['likes'], 0)
        self.assertEqual(data['detail_body'], '#001c58')
        # id, group, owner should be null for non-authorized requests
        self.assertEqual(data['id'], None)
        self.assertEqual(data['group'], None)
        self.assertEqual(data['owner'], None)

        # login to created account
        self.client.login(username='user03',password='pass')
        response = self.client.get('/')
        self.assertEqual(response.status_code//100, 2)
        response.render()
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(data['detail_sleeve'], '#fcfcfc')
        self.assertEqual(data['likes'], 0)
        self.assertEqual(data['detail_body'], '#001c58')
        # id, group, owner should not be null for authorized requests
        self.assertFalse(data['id']==None)
        self.assertEquals(Group.objects.get(id=data['group']).group_name, 'user_group_user03')
        self.assertFalse(data['owner']==None)


class SaveDesignCase(TestCase):
    def setUp(self):
        self.client.post('/users/', {'username': 'user04', 'password': 'pass'})
        self.client.login(username='user04',password='pass')

    def test_save_design(self):
        """get design id"""
        response = self.client.get('/')
        response.render()
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        design_id = data['id']
        """save design"""
        self.client.put('/', {
            "detail_body": "#232323",
            "detail_buttons": "#232323",
            "detail_sleeve": "#232323",
            "detail_banding": "#232323",
            "detail_stripes": "#232323",
            "id": design_id
        }, 'application/json')
        response = self.client.get('/')
        self.assertEqual(response.status_code//100, 2)
        response.render()
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(data['detail_sleeve'], '#232323')
        self.assertEqual(data['likes'], 0)
        self.assertEqual(data['detail_body'], '#232323')
        # id, group, owner should not be null for authorized requests
        self.assertEquals(data['id'], design_id)
        self.assertEquals(Group.objects.get(id=data['group']).group_name, 'user_group_user04')
        self.assertFalse(data['owner']==None)

# class NewDesignCase(TestCase):
#     def setUp(self):
#         self.client.post('/users/', {'username': 'user05', 'password': 'pass'})
#         self.client.login(username='user05',password='pass')

#     def test_save_design(self):
#         """get design id"""
#         response = self.client.get('/')
#         response.render()
#         stream = io.BytesIO(response.content)
#         data = JSONParser().parse(stream)
#         design_id = data['id']
#         """save design"""
#         self.client.put('/', {
#             "detail_body": "#232323",
#             "detail_buttons": "#232323",
#             "detail_sleeve": "#232323",
#             "detail_banding": "#232323",
#             "detail_stripes": "#232323",
#             "id": design_id
#         }, 'application/json')
#         response = self.client.get('/')
#         self.assertEqual(response.status_code//100, 2)
#         response.render()e
#         stream = io.BytesIO(response.content)
#         data = JSONParser().parse(stream)
#         self.assertEqual(data['detail_sleeve'], '#232323')
#         self.assertEqual(data['likes'], 0)
#         self.assertEqual(data['detail_body'], '#232323')
#         # id, group, owner should not be null for authorized requests
#         self.assertEquals(data['id'], design_id)
#         self.assertEquals(Group.objects.get(id=data['group']).group_name, 'user_group_user04')
#         self.assertFalse(data['owner']==None)