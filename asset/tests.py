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