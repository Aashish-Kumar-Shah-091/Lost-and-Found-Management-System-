from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from apps.items.models import LostItem, FoundItem
from .models import Claim


class ClaimModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.reporter = User.objects.create_user(username='reporter', password='testpass123')
        self.lost_item = LostItem.objects.create(
            user=self.reporter,
            item_name='Lost Wallet',
            category='Accessories',
            description='Black wallet',
            lost_location='Park',
            lost_date='2026-01-01',
        )

    def test_create_claim(self):
        ct = ContentType.objects.get_for_model(LostItem)
        claim = Claim.objects.create(
            claimant=self.user,
            content_type=ct,
            object_id=self.lost_item.id,
            proof='I can describe it in detail',
        )
        self.assertEqual(claim.status, 'Pending')
        self.assertEqual(claim.claimant, self.user)


class ClaimViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='claimant', password='testpass123')
        self.reporter = User.objects.create_user(username='reporter', password='testpass123')
        self.lost_item = LostItem.objects.create(
            user=self.reporter,
            item_name='Lost Phone',
            category='Electronics',
            description='iPhone',
            lost_location='Office',
            lost_date='2026-01-15',
        )
        self.found_item = FoundItem.objects.create(
            user=self.reporter,
            item_name='Found Bag',
            category='Bags',
            description='Blue bag',
            found_location='Library',
        )

    def test_claim_list_loads(self):
        response = self.client.get(reverse('claim_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'claims/claim_list.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_create_claim_requires_login(self):
        response = self.client.get(reverse('create_claim', args=['lost', self.lost_item.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_create_claim_for_lost_item(self):
        self.client.login(username='claimant', password='testpass123')
        response = self.client.post(
            reverse('create_claim', args=['lost', self.lost_item.pk]),
            {'proof': 'I can describe the serial number'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Claim.objects.filter(claimant=self.user).exists())

    def test_create_claim_for_found_item(self):
        self.client.login(username='claimant', password='testpass123')
        response = self.client.post(
            reverse('create_claim', args=['found', self.found_item.pk]),
            {'proof': 'I can identify the contents'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Claim.objects.filter(claimant=self.user).exists())

    def test_claim_detail_loads(self):
        ct = ContentType.objects.get_for_model(LostItem)
        claim = Claim.objects.create(
            claimant=self.user,
            content_type=ct,
            object_id=self.lost_item.id,
            proof='Test proof',
        )
        response = self.client.get(reverse('claim_detail', args=[claim.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test proof')
        self.assertTemplateUsed(response, 'base.html')


class ClaimWorkflowTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.reporter = User.objects.create_user(
            username='reporter', password='testpass123', email='reporter@test.com'
        )
        self.claimant = User.objects.create_user(
            username='claimant', password='testpass123'
        )

    def test_full_claim_workflow(self):
        self.client.login(username='reporter', password='testpass123')
        self.client.post(reverse('create_lost_item'), {
            'item_name': 'Workflow Item',
            'category': 'Electronics',
            'description': 'Test workflow',
            'lost_location': 'Test Location',
            'lost_date': '2026-01-01',
        })
        item = LostItem.objects.get(item_name='Workflow Item')
        self.client.logout()

        self.client.login(username='claimant', password='testpass123')
        response = self.client.post(
            reverse('create_claim', args=['lost', item.pk]),
            {'proof': 'I have the receipt'}
        )
        self.assertEqual(response.status_code, 302)

        claim = Claim.objects.get(claimant=self.claimant)
        self.assertEqual(claim.status, 'Pending')
        self.assertEqual(claim.object_id, item.id)

        claim.status = 'Approved'
        claim.save()
        self.assertEqual(claim.status, 'Approved')
