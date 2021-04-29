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

class RegisterViewTestCase(TestCase):
    def test_status_code_200(self):
        response = self.client.get(reverse('register'))
        self.assertEquals(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response,'base.html')
        self.assertTemplateUsed(response,'register.html')
    
    def test_post(self):
        response = self.client.post(reverse('register'), data={'first_name' : 'test', 'last_name' : 'test', 'email' : 'test@test.com','username' : 'test', 'password1' : 'Axksd32x', 'password2' : 'Axksd32x'}, follow = True)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'home.html')
        self.assertRedirects(response=response, expected_url = reverse('home'))

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

class AssetsViewTestCase(TestCase):
    def test_status_code_200(self):
        response = self.client.get(reverse('assets'))
        self.assertEquals(response.status_code, 200)

class MonitoringViewTestCase(TestCase):
    def test_status(self):
        us = User.objects.create(username = 'test')
        us.set_password('test')
        us.save()
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('monitoring'))
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'monitoring.html')
        self.assertEquals(response.status_code, 200)
        self.client.logout()
        us.delete()
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

class TestAssetForm(TestCase):
    def test_fields_label(self):
        form = AssetForm()
        self.assertTrue(form.fields['update_time'].label == 'Update time')
        self.assertTrue(form.fields['inferior_limit'].label == 'Inferior limit')
        self.assertTrue(form.fields['upper_limit'].label == 'Upper limit')

    def test_valid_asset(self):
        form = AssetForm(data = {
            'update_time' : 62,
            'inferior_limit' : 34.22,
            'upper_limit' : 47.25
        })
        self.assertTrue(form.is_valid())
