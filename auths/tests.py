from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

class UserRegistrationTest(TestCase):
    def test_complete_user_registration(self):
        User = get_user_model()

        # Step 1: Email
        data_step1 = {'email': 'testuser@example.com'}
        response = self.client.post(reverse('mail'), data=data_step1)
        self.assertEqual(response.status_code, 302)  # Check for a redirect

        # Step 2: User Information
        data_step2 = {
            'name': 'John',
            'prenoms': 'Doe',
            'age': 30,
            'phone': '1234567890',
            'country': 'US',
        }
        response = self.client.post(reverse('userInfo'), data=data_step2)
        self.assertEqual(response.status_code, 302)

        # Step 3: Birth
        data_step3 = {
            # Add data for the 'birth' step as needed
        }
        response = self.client.post(reverse('birth'), data=data_step3)
        self.assertEqual(response.status_code, 302)

        # Step 4: Address
        data_step4 = {
            'logement': 'Apartment',
            'address': '123 Main St',
        }
        response = self.client.post(reverse('adresse'), data=data_step4)
        self.assertEqual(response.status_code, 302)

        # Step 5: Financial
        data_step5 = {
            'res': 'Fiscal Resident',
            'prin': 'Type',
        }
        response = self.client.post(reverse('financial'), data=data_step5)
        self.assertEqual(response.status_code, 302)

        # Step 6: Usage
        data_step6 = {
            # Add data for the 'usage' step as needed
        }
        response = self.client.post(reverse('usage'), data=data_step6)
        self.assertEqual(response.status_code, 302)

        # Step 7: Profession
        data_step7 = {
            'profession': 'Engineer',
        }
        response = self.client.post(reverse('profession'), data=data_step7)
        self.assertEqual(response.status_code, 302)

        # Step 8: Revenu
        data_step8 = {
            'revenu': 50000,
        }
        response = self.client.post(reverse('revenu'), data=data_step8)
        self.assertEqual(response.status_code, 302)

        # Step 9: Password
        data_step9 = {
            'password': 'testpassword',
        }
        response = self.client.post(reverse('password'), data=data_step9)
        self.assertEqual(response.status_code, 302)

        # Ensure that the user is now logged in after registration
        user = User.objects.get(email='testuser@example.com')
        self.assertTrue(user.is_authenticated)

    def tearDown(self):
        # Clean up after the test by deleting the test user
        User = get_user_model()
        User.objects.filter(email='testuser@example.com').delete()
