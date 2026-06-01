from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import LostItem, FoundItem
import io
from PIL import Image


def create_test_image():
    img = Image.new('RGB', (100, 100), color='red')
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    return SimpleUploadedFile('test.jpg', buffer.read(), content_type='image/jpeg')


class LostItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_create_lost_item(self):
        item = LostItem.objects.create(
            user=self.user,
            item_name='Test Wallet',
            category='Accessories',
            description='Black leather wallet',
            lost_location='Central Park',
            lost_date='2026-01-01',
        )
        self.assertEqual(str(item), 'Test Wallet')
        self.assertEqual(item.status, 'Lost')

    def test_create_lost_item_with_image(self):
        image = create_test_image()
        item = LostItem.objects.create(
            user=self.user,
            item_name='Test Phone',
            category='Electronics',
            description='iPhone 15',
            lost_location='Library',
            lost_date='2026-01-15',
            image=image,
        )
        self.assertTrue(item.image)
        self.assertIn('lost_items/', item.image.name)


class FoundItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_create_found_item(self):
        item = FoundItem.objects.create(
            user=self.user,
            item_name='Found Keys',
            category='Accessories',
            description='Set of 3 keys',
            found_location='Bus Stop',
        )
        self.assertEqual(str(item), 'Found Keys')
        self.assertEqual(item.status, 'Found')

    def test_create_found_item_with_image(self):
        image = create_test_image()
        item = FoundItem.objects.create(
            user=self.user,
            item_name='Found Bag',
            category='Bags',
            description='Blue backpack',
            found_location='Cafeteria',
            image=image,
        )
        self.assertTrue(item.image)
        self.assertIn('found_items/', item.image.name)


class LostItemViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.item = LostItem.objects.create(
            user=self.user,
            item_name='Lost Watch',
            category='Accessories',
            description='Gold watch',
            lost_location='Gym',
            lost_date='2026-02-01',
        )

    def test_lost_item_list_loads(self):
        response = self.client.get(reverse('lost_item_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lost Items')
        self.assertContains(response, 'Lost Watch')

    def test_lost_item_list_uses_base_template(self):
        response = self.client.get(reverse('lost_item_list'))
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'items/lost_item_list.html')

    def test_lost_item_detail_loads(self):
        response = self.client.get(reverse('lost_item_detail', args=[self.item.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lost Watch')
        self.assertContains(response, 'Gold watch')

    def test_create_lost_item_requires_login(self):
        response = self.client.get(reverse('create_lost_item'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_create_lost_item_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('create_lost_item'))
        self.assertEqual(response.status_code, 200)

    def test_create_lost_item_post(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('create_lost_item'), {
            'item_name': 'New Lost Item',
            'category': 'Electronics',
            'description': 'A laptop',
            'lost_location': 'Office',
            'lost_date': '2026-03-01',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(LostItem.objects.filter(item_name='New Lost Item').exists())

    def test_create_lost_item_with_image(self):
        self.client.login(username='testuser', password='testpass123')
        image = create_test_image()
        response = self.client.post(reverse('create_lost_item'), {
            'item_name': 'Item With Image',
            'category': 'Electronics',
            'description': 'Has an image',
            'lost_location': 'Park',
            'lost_date': '2026-03-01',
            'image': image,
        })
        self.assertEqual(response.status_code, 302)
        item = LostItem.objects.get(item_name='Item With Image')
        self.assertTrue(item.image)


class FoundItemViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.item = FoundItem.objects.create(
            user=self.user,
            item_name='Found Phone',
            category='Electronics',
            description='Samsung phone',
            found_location='Library',
        )

    def test_found_item_list_loads(self):
        response = self.client.get(reverse('found_item_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Found Items')
        self.assertContains(response, 'Found Phone')

    def test_found_item_list_uses_base_template(self):
        response = self.client.get(reverse('found_item_list'))
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'items/found_item_list.html')

    def test_found_item_detail_loads(self):
        response = self.client.get(reverse('found_item_detail', args=[self.item.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Found Phone')

    def test_create_found_item_requires_login(self):
        response = self.client.get(reverse('create_found_item'))
        self.assertEqual(response.status_code, 302)

    def test_create_found_item_post(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('create_found_item'), {
            'item_name': 'Found Wallet',
            'category': 'Accessories',
            'description': 'Brown wallet',
            'found_location': 'Bus',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(FoundItem.objects.filter(item_name='Found Wallet').exists())

    def test_create_found_item_with_image(self):
        self.client.login(username='testuser', password='testpass123')
        image = create_test_image()
        response = self.client.post(reverse('create_found_item'), {
            'item_name': 'Found With Pic',
            'category': 'Bags',
            'description': 'Bag with pic',
            'found_location': 'Train',
            'image': image,
        })
        self.assertEqual(response.status_code, 302)
        item = FoundItem.objects.get(item_name='Found With Pic')
        self.assertTrue(item.image)


class ImageURLTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_lost_item_image_url(self):
        image = create_test_image()
        item = LostItem.objects.create(
            user=self.user,
            item_name='URL Test',
            category='Electronics',
            description='Test',
            lost_location='Test',
            lost_date='2026-01-01',
            image=image,
        )
        self.assertTrue(item.image.url.startswith('/media/') or 'cloudinary' in item.image.url)

    def test_found_item_image_url(self):
        image = create_test_image()
        item = FoundItem.objects.create(
            user=self.user,
            item_name='URL Test',
            category='Electronics',
            description='Test',
            found_location='Test',
            image=image,
        )
        self.assertTrue(item.image.url.startswith('/media/') or 'cloudinary' in item.image.url)
