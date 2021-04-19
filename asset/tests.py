from django.test import TestCase
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
