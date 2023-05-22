from django.contrib.auth import get_user_model
from django.test import TestCase
from participants.serializers import (
    ParticipantListSerializer,
    ParticipantCreateSerializer,
    ParticipantRetrieveSerializer
)

User = get_user_model()


class ParticipantSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email='test@example.com',
            first_name='John',
            last_name='Doe'
        )

    def test_participant_list_serializer(self):
        serializer = ParticipantListSerializer(instance=self.user)

        for i in ['id', 'username', 'first_name', 'last_name', 'email']:
            self.assertTrue(i in list(serializer.data.keys()))

    def test_participant_create_serializer(self):
        passwd = 'newpass123@123'
        data = {
            'username': 'newuser',
            'password': passwd,
            'email': 'new@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
        }
        serializer = ParticipantCreateSerializer(data=data)
        serializer.is_valid()
        participant = serializer.save()
        self.assertEqual(participant.username, 'newuser')
        self.assertTrue(participant.check_password(passwd))
        self.assertEqual(participant.email, 'new@example.com')
        self.assertEqual(participant.first_name, 'Jane')
        self.assertEqual(participant.last_name, 'Smith')

    def test_participant_retrieve_serializer(self):
        serializer = ParticipantRetrieveSerializer(instance=self.user)
        expected_data = {
            'id': self.user.id,
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
        }

        for i in ['id', 'username', 'first_name', 'last_name', 'email']:
            self.assertEqual(serializer.data.get(i), expected_data.get(i))
