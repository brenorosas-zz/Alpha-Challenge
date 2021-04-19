from django.test import TestCase
from .forms import *
from .models import *
# Create your tests here.
#Models
class AssetTestCase(TestCase):
    def setUp(self):
        us = User.objects.create(username = 'test')
        us.set_password('test')
        us.save()
        Asset.objects.create(
            name = 'NameTest',
            user = us,
            update_time = 60,
            inferior_limit = 29.50,
            upper_limit = 129.50
        )

    def test_retorno_str(self):
        as1 = Asset.objects.get(name = 'NameTest')
        self.assertEquals(as1.__str__(), 'NameTest')

#views
class LoginViewTestCase(TestCase):
    def test_status_code_200(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'login.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_post(self):
        us = User.objects.create(username = 'test')
        us.set_password('test')
        us.save()
        response = self.client.post(reverse('login'), data = {'username' : 'test', 'password' : 'test'}, follow = True)
        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(response.status_code, 200)
        us.delete()

class HomeViewTestCase(TestCase):
    def test_status_code_200(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'home.html')

class LogoutViewTestCase(TestCase):
    def test_status_code_302(self):
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 302)

#forms
class TestUserCreationForm(TestCase):
    def test_fields_label(self):
        form = UserCreationForm()
        self.assertTrue(form.fields['email'].label == 'Email')
        self.assertTrue(form.fields['first_name'].label == 'First Name')
        self.assertTrue(form.fields['last_name'].label == 'Last Name')
    
    def test_valid_user(self):
        form = UserCreationForm(data = {
            'username' : 'test',
            'first_name' : 'Test First Name',
            'last_name' : 'Test Last Name',
            'email' : 'testemail@test.com',
            'password1':'Test1034', 
            'password2':'Test1034'
        })
        self.assertTrue(form.is_valid())
        us = form.save()
        self.assertTrue(User.objects.filter(username = 'test').exists())
        us.delete()
        self.assertFalse(User.objects.filter(username = 'test').exists())
    
    def test_invalid_user(self):
        form = UserCreationForm(data = {
            'username' : 'test',
            'first_name' : 'Test First Name',
            'last_name' : 'Test Last Name',
            'email' : 'test',
            'password1':'1234', 
            'password2':'1234'
        })
        self.assertFalse(form.is_valid())
        self.assertFalse(User.objects.filter(username = 'test').exists())
