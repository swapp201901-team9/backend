from django.test import TestCase
from django.http import HttpRequest
from rest_framework.parsers import JSONParser
from .models import Group
from .views import *

class GroupTestCase(TestCase):
    def setUp(self):
        Group.objects.create(group_type = "major", group_name="cse")
    
    def test_group_type_created(self):
        """if group type has the unified name protocol"""
        cse = Group.objects.get(group_name= "cse")
        self.assertEqual(cse.group_type, "major")

# LoadDesignCase to be made
class GetEmptyDesignCase(TestCase):
    def test_default_attributes(self):
        """empty design objects have default values"""
        FakeRequest = HttpRequest()
        FakeRequest.method = 'GET'
        response = main(FakeRequest)
        
        print("----------GetEmptyDesignCase---------")
        response.render()
        data = JSONParser().parse(response.content)
        print(data)
        

# class CreateDesignCase(TestCase):     
#     def setUp(self):
#         Group.objects.create(group_type = "major", group_name="cse")
    
#     def test_group_type_created(self):
#         """if group type has the unified name protocol"""
#         cse = Group.objects.get(group_name= "cse")
#         self.assertEqual(cse.group_type, "major")
