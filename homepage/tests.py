from django.test import TestCase, Client
from django.http.request import HttpRequest
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
        c = Client()
        response = c.post('/users/', {'username': 'user01', 'password': 'pass'})
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
        c = Client()
        response = c.post('/users/', {'username': 'user02', 'password': 'pass'})
    
    def test_login(self):
        # Check if joined successfully        
        try:
            user = User.objects.get(username='user02')
        except User.DoesNotExist:
            self.assertEqual(1, 2)
        
        # Check if logged in successfully
        c = Client()
        credentials = encode(b'user02:pass')
        response = c.get('/auth/', HTTP_AUTHORIZATION='Basic ' + credentials.decode())
        self.assertEqual(response.status_code//100, 2)
        

#################### Test Main Page ####################

class GetEmptyDesignCase(TestCase):
    def setUp(self):
        c = Client()
        response = c.post('/users/', {'username': 'user03', 'password': 'pass'})

    def test_default_attributes(self):
        """empty design objects have default values"""
        FakeRequest = HttpRequest()
        FakeRequest.method = 'GET'
        
        response = main(FakeRequest)
        response.render()
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(data['detail_sleeve'], 'WT')
        self.assertEqual(data['likes'], 0)
        self.assertEqual(data['detail_body'], 'BK')
        # id, group, owner should be null for non-authorized requests
        self.assertEqual(data['id'], None)
        self.assertEqual(data['group'], None)
        self.assertEqual(data['owner'], None)

        user = User.objects.get(username='user03')
        FakeRequest.user = user
        response = main(FakeRequest)
        response.render()
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(data['detail_sleeve'], 'WT')
        self.assertEqual(data['likes'], 0)
        self.assertEqual(data['detail_body'], 'BK')
        # id, group, owner should not be null for authorized requests
        self.assertFalse(data['id']==None)
        self.assertEquals(Group.objects.get(id=data['group']).group_name, 'user_group_user03')
        self.assertFalse(data['owner']==None)


# class CreateDesignCase(TestCase):
    
