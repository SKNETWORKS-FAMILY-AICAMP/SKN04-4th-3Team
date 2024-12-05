from django.test import TestCase, Client
from django.urls import reverse

API_URL = "${window.location.protocol}//${window.location.host}/api/chat/"

class ChatAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse(API_URL)  

    def test_send_message(self):
        response = self.client.post(self.url, {'message': '너는 누구니?'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('bot_response', response.data)

    def test_empty_message(self):
        response = self.client.post(self.url, {'message': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
