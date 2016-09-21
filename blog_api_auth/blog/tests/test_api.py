from datetime import date

from blog.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .fixtures import *


class UserTestCase(APITestCase):
    def setUp(self):
        super(UserTestCase, self).setUp()
        self.user = User.objects.create_user(
            username='larrypage', password='abc123', first_name='Larry',
            last_name='Page', email='lpage@google.com', accesskey='a' * 32,
            secretkey='b' * 32)

    def test_list(self):
        """Should return a list of all users when user is authenticated"""
        expected = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': 1,
                    'username': 'larrypage',
                    'first_name': 'Larry',
                    'last_name': 'Page',
                    'email': 'lpage@google.com',
                    'accesskey': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
                }
            ]
        }
        params = {'accesskey': self.user.accesskey}
        response = self.client.get('/api/users', params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected)

    def test_list_missing_accesskey(self):
        """Should return 403 when no accesskey is given in url"""
        response = self.client.get('/api/users')
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_list_invalid_accesskey(self):
        """Should return 403 when given accesskey is invalid"""
        params = {'accesskey': 'INVALID'}
        response = self.client.get('/api/users', params)
        expected = {'detail': 'Invalid Accesskey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_detail(self):
        """Should return the detail of given user when user is authenticated"""
        expected = {
            'id': 1,
            'username': 'larrypage',
            'first_name': 'Larry',
            'last_name': 'Page',
            'email': 'lpage@google.com',
            'accesskey': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        }
        params = {'accesskey': self.user.accesskey}
        response = self.client.get('/api/users/{}'.format(self.user.id), params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected)

    def test_detail_missing_accesskey(self):
        """Should return 403 when no accesskey is given in url"""
        response = self.client.get('/api/users/{}'.format(self.user.id))
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_detail_invalid_accesskey(self):
        """Should return 403 when no accesskey is given in url"""
        params = {'accesskey': 'INVALID'}
        response = self.client.get('/api/users/{}'.format(self.user.id), params)
        expected = {'detail': 'Invalid Accesskey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_detail_not_found_id(self):
        """Should return 404 when given id does not exist"""
        params = {'accesskey': self.user.accesskey}
        response = self.client.get('/api/users/{}'.format('foobar'), params)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create(self):
        """Should create a new user when given data is valid"""
        self.assertEqual(User.objects.count(), 1)
        payload = {
            'username': 'sergeybrin',
            'accesskey': 'c' * 32,
            'secretkey': 'c' * 32,
            'password': 'abc123'
        }
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.post(
            '/api/users?accesskey={}'.format(self.user.accesskey),
            data=payload, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        user = User.objects.get(username='sergeybrin')
        self.assertTrue(user.check_password('abc123'))

    def test_create_missing_accesskey(self):
        """Should return 403 when no accesskey is given in url"""
        payload = {
            'username': 'sergeybrin',
            'accesskey': 'c' * 32,
            'secretkey': 'c' * 32,
            'password': 'abc123'
        }
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.post('/api/users', data=payload, **headers)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_create_missing_secretkey(self):
        """Should return 403 when no secretkey is given in headers"""
        payload = {
            'username': 'sergeybrin',
            'accesskey': 'c' * 32,
            'secretkey': 'c' * 32,
            'password': 'abc123'
        }
        response = self.client.post(
            '/api/users?accesskey={}'.format(self.user.accesskey), data=payload)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_create_invalid_accesskey(self):
        """Should return 403 when given accesskey is invalid"""
        payload = {
            'username': 'sergeybrin',
            'accesskey': 'c' * 32,
            'secretkey': 'c' * 32,
            'password': 'abc123'
        }
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.post(
            '/api/users?accesskey={}'.format('INVALID'),
            data=payload, **headers)
        expected = {'detail': 'Invalid Accesskey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_create_invalid_secretkey(self):
        """Should return 403 when given accesskey is invalid"""
        payload = {
            'username': 'sergeybrin',
            'accesskey': 'c' * 32,
            'secretkey': 'c' * 32,
            'password': 'abc123'
        }
        headers = {'HTTP_X_SECRET_KEY': 'INVALID'}
        response = self.client.post(
            '/api/users?accesskey={}'.format(self.user.accesskey),
            data=payload, **headers)
        expected = {'detail': 'Invalid Secretkey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_full_update(self):
        """Should full update an user when given data is valid"""
        payload = {
            'username': 'lpage',
            'first_name': 'Larry',
            'last_name': 'Page',
            'accesskey': 'a' * 32,
            'secretkey': 'b' * 32,
            'password': 'newpassword'
        }
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.put(
            '/api/users/{}?accesskey={}'.format(self.user.id, self.user.accesskey),
            data=payload, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.username, 'lpage')
        self.assertTrue(user.check_password('newpassword'))

    def test_full_update_missing_accesskey(self):
        """Should return 403 when no accesskey is given in url"""
        payload = {
            'username': 'lpage',
            'first_name': 'Larry',
            'last_name': 'Page',
            'accesskey': 'a' * 32,
            'secretkey': 'b' * 32,
            'password': 'newpassword'
        }
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.put(
            '/api/users/{}'.format(self.user.id), data=payload, **headers)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_full_update_missing_secretkey(self):
        """Should return 403 when no secretkey is given in headers"""
        payload = {
            'username': 'lpage',
            'first_name': 'Larry',
            'last_name': 'Page',
            'accesskey': 'a' * 32,
            'secretkey': 'b' * 32,
            'password': 'newpassword'
        }
        response = self.client.put(
            '/api/users/{}?accesskey={}'.format(self.user.id, self.user.accesskey),
            data=payload)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_full_update_invalid_accesskey(self):
        """Should return 403 when given accesskey is invalid"""
        payload = {
            'username': 'lpage',
            'first_name': 'Larry',
            'last_name': 'Page',
            'accesskey': 'a' * 32,
            'secretkey': 'b' * 32,
            'password': 'newpassword'
        }
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.put(
            '/api/users/{}?accesskey={}'.format(self.user.id, 'INVALID'),
            data=payload, **headers)
        expected = {'detail': 'Invalid Accesskey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_full_update_invalid_secretkey(self):
        """Should return 403 when given accesskey is invalid"""
        payload = {
            'username': 'lpage',
            'first_name': 'Larry',
            'last_name': 'Page',
            'accesskey': 'a' * 32,
            'secretkey': 'b' * 32,
            'password': 'newpassword'
        }
        headers = {'HTTP_X_SECRET_KEY': 'INVALID'}
        response = self.client.put(
            '/api/users/{}?accesskey={}'.format(self.user.id, self.user.accesskey),
            data=payload, **headers)
        expected = {'detail': 'Invalid Secretkey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_partial_update(self):
        """Should partial update an user when given data is valid"""
        payload = {
            'username': 'lpage',
        }
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.patch(
            '/api/users/{}?accesskey={}'.format(self.user.id, self.user.accesskey),
            data=payload, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.username, 'lpage')

    def test_partial_update_missing_accesskey(self):
        """Should return 403 when no accesskey is given in url"""
        payload = {
            'username': 'lpage',
        }
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.patch(
            '/api/users/{}'.format(self.user.id), data=payload, **headers)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_partial_update_missing_secretkey(self):
        """Should return 403 when no secretkey is given in headers"""
        payload = {
            'username': 'lpage',
        }
        response = self.client.patch(
            '/api/users/{}?accesskey={}'.format(self.user.id, self.user.accesskey),
            data=payload)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_partial_update_invalid_accesskey(self):
        """Should return 403 when given accesskey is invalid"""
        payload = {
            'username': 'lpage',
        }
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.patch(
            '/api/users/{}?accesskey={}'.format(self.user.id, 'INVALID'),
            data=payload, **headers)
        expected = {'detail': 'Invalid Accesskey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_partial_update_invalid_secretkey(self):
        """Should return 403 when given accesskey is invalid"""
        payload = {
            'username': 'lpage',
        }
        headers = {'HTTP_X_SECRET_KEY': 'INVALID'}
        response = self.client.patch(
            '/api/users/{}?accesskey={}'.format(self.user.id, self.user.accesskey),
            data=payload, **headers)
        expected = {'detail': 'Invalid Secretkey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_delete(self):
        """Should delete an user when given id is valid"""
        self.assertEqual(User.objects.count(), 1)
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.delete(
            '/api/users/{}?accesskey={}'.format(
                self.user.id, self.user.accesskey), **headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='larrypage')

    def test_delete_missing_accesskey(self):
        """Should return 403 when no accesskey is given in url"""
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.delete(
            '/api/users/{}'.format(self.user.id), **headers)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_delete_missing_secretkey(self):
        """Should return 403 when no secretkey is given in headers"""
        response = self.client.delete(
            '/api/users/{}?accesskey={}'.format(
                self.user.id, self.user.accesskey))
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_delete_invalid_accesskey(self):
        """Should return 403 when given accesskey is invalid"""
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.delete(
            '/api/users/{}?accesskey={}'.format(
                self.user.id, 'INVALID'), **headers)
        expected = {'detail': 'Invalid Accesskey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_delete_invalid_secretkey(self):
        """Should return 403 when given accesskey is invalid"""
        headers = {'HTTP_X_SECRET_KEY': 'INVALID'}
        response = self.client.delete(
            '/api/users/{}?accesskey={}'.format(
                self.user.id, self.user.accesskey), **headers)
        expected = {'detail': 'Invalid Secretkey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)


class EntryTestCase(APITestCase):
    def setUp(self):
        super(EntryTestCase, self).setUp()
        self.blog = BlogFactory()
        self.user = User.objects.create_user(
            username='larrypage', password='abc123', first_name='Larry',
            last_name='Page', email='lpage@google.com', accesskey='a' * 32,
            secretkey='b' * 32)
        self.user_2 = User.objects.create_user(
            username='sergeybrin', password='abc123', first_name='Sergey',
            last_name='Brin', email='sbrin@google.com', accesskey='x' * 32,
            secretkey='z' * 32)

        self.entry = EntryFactory(
            blog=self.blog, scoring=2.04, number_comments='10')
        self.entry.users.add(self.user)
        self.entry.pub_date = date(2016, 1, 15)
        self.entry.save()

        self.entry_2 = EntryFactory(
            blog=self.blog, scoring=4.25, number_comments='20')
        self.entry_2.pub_date = date(2016, 1, 15)
        self.entry_2.save()

    def test_list(self):
        """Should return a list of all entries when user is authenticated"""
        expected = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'users': [
                        'http://testserver/api/users/1'
                    ],
                    'blog': 'http://testserver/api/blogs/1',
                    'body_text': 'Some body text',
                    'headline': 'Some headline',
                    'mod_date': str(date.today()),
                    'number_comments': 10,
                    'pub_date': '2016-01-15',
                    'scoring': '2.04',
                    'url': 'http://testserver/api/entries/1'
                },
                {
                    'users': [],
                    'blog': 'http://testserver/api/blogs/1',
                    'body_text': 'Some body text',
                    'headline': 'Some headline',
                    'mod_date': str(date.today()),
                    'number_comments': 20,
                    'pub_date': '2016-01-15',
                    'scoring': '4.25',
                    'url': 'http://testserver/api/entries/2'
                }
            ]
        }
        params = {'accesskey': self.user.accesskey}
        response = self.client.get('/api/entries', params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected)

    def test_list_missing_accesskey(self):
        """Should return 403 when no accesskey is given in url"""
        response = self.client.get('/api/entries')
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_list_invalid_accesskey(self):
        """Should return 403 when given accesskey is invalid"""
        params = {'accesskey': 'INVALID'}
        response = self.client.get('/api/entries', params)
        expected = {'detail': 'Invalid Accesskey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_detail(self):
        """Should return the detail of given entry when user is authenticated"""
        expected = {
            'users': [
                'http://testserver/api/users/1'
            ],
            'blog': 'http://testserver/api/blogs/1',
            'body_text': 'Some body text',
            'headline': 'Some headline',
            'mod_date': str(date.today()),
            'number_comments': 10,
            'pub_date': '2016-01-15',
            'scoring': '2.04',
            'url': 'http://testserver/api/entries/1'
        }
        params = {'accesskey': self.user.accesskey}
        response = self.client.get(
            '/api/entries/{}'.format(self.entry.id), params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected)

    def test_detail_missing_accesskey(self):
        """Should return 403 when no accesskey is given in url"""
        response = self.client.get('/api/entries/{}'.format(self.entry.id))
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_detail_invalid_accesskey(self):
        """Should return 403 when given accesskey is invalid"""
        params = {'accesskey': 'INVALID'}
        response = self.client.get(
            '/api/entries/{}'.format(self.entry.id), params)
        expected = {'detail': 'Invalid Accesskey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_create(self):
        """Should create a new entry when given data is valid and user is authenticated"""
        self.assertEqual(Entry.objects.count(), 2)
        payload = {
            'blog': 'http://testserver/api/blogs/1',
            'users': ['http://testserver/api/users/1'],
            'headline': 'New entry',
            'body_text': 'Some body text',
            'number_comments': 15,
            'scoring': 4.25
        }
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.post(
            '/api/entries?accesskey={}'.format(
                self.user.accesskey), data=payload, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Entry.objects.count(), 3)
        entry = Entry.objects.get(headline='New entry')
        self.assertEqual(entry.blog, self.blog)
        self.assertEqual(entry.users.count(), 1)
        self.assertEqual(entry.body_text, 'Some body text')
        self.assertEqual(entry.number_comments, 15)
        self.assertEqual(entry.scoring, 4.25)

    def test_create_missing_accesskey(self):
        """Should return 403 when no accesskey is given in url"""
        payload = {
            'blog': 'http://testserver/api/blogs/1',
            'users': ['http://testserver/api/users/1'],
            'headline': 'New entry',
            'body_text': 'Some body text',
            'number_comments': 15,
            'scoring': 4.25
        }
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.post(
            '/api/entries', data=payload, format='json', **headers)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_create_missing_secretkey(self):
        """Should return 403 when no secretkey is given in headers"""
        payload = {
            'blog': 'http://testserver/api/blogs/1',
            'users': ['http://testserver/api/users/1'],
            'headline': 'New entry',
            'body_text': 'Some body text',
            'number_comments': 15,
            'scoring': 4.25
        }
        response = self.client.post(
            '/api/entries?accesskey={}'.format(
                self.user.accesskey), data=payload, format='json')
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_create_invalid_accesskey(self):
        """Should return 403 when given accesskey is invalid"""
        payload = {
            'blog': 'http://testserver/api/blogs/1',
            'users': ['http://testserver/api/users/1'],
            'headline': 'New entry',
            'body_text': 'Some body text',
            'number_comments': 15,
            'scoring': 4.25
        }
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.post(
            '/api/entries?accesskey={}'.format('INVALID'),
            data=payload, format='json', **headers)
        expected = {'detail': 'Invalid Accesskey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_create_invalid_secretkey(self):
        """Should return 403 when given accesskey is invalid"""
        payload = {
            'blog': 'http://testserver/api/blogs/1',
            'users': ['http://testserver/api/users/1'],
            'headline': 'New entry',
            'body_text': 'Some body text',
            'number_comments': 15,
            'scoring': 4.25
        }
        headers = {'HTTP_X_SECRET_KEY': 'INVALID'}
        response = self.client.post(
            '/api/entries?accesskey={}'.format(
                self.user.accesskey), data=payload, format='json', **headers)
        expected = {'detail': 'Invalid Secretkey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_full_update(self):
        """Should full update an entry when given data is valid and user is authenticated"""
        payload = {
            'blog': 'http://testserver/api/blogs/1',
            'users': ['http://testserver/api/users/1'],
            'headline': 'New headline',
            'body_text': 'Some body text',
            'number_comments': 15,
            'scoring': 4.25
        }
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.put(
            '/api/entries/{}?accesskey={}'.format(
                self.entry.id, self.user.accesskey), data=payload, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        entry = Entry.objects.get(id=self.entry.id)
        self.assertEqual(entry.headline, 'New headline')

    def test_full_update_permission_denied(self):
        """Should return 403 when an user tries to full update an entry from other user"""
        payload = {
            'blog': 'http://testserver/api/blogs/1',
            'users': ['http://testserver/api/users/1'],
            'headline': 'New headline',
            'body_text': 'Some body text',
            'number_comments': 15,
            'scoring': 4.25
        }
        headers = {'HTTP_X_SECRET_KEY': self.user_2.secretkey}
        response = self.client.put(
            '/api/entries/{}?accesskey={}'.format(
                self.entry.id, self.user_2.accesskey), data=payload, **headers)
        expected = {
            'detail': 'You do not have permission to perform this action.'
        }
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_full_update_missing_accesskey(self):
        """Should return 403 when no accesskey is given in url"""
        payload = {
            'blog': 'http://testserver/api/blogs/1',
            'users': ['http://testserver/api/users/1'],
            'headline': 'New headline',
            'body_text': 'Some body text',
            'number_comments': 15,
            'scoring': 4.25
        }
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.put(
            '/api/entries/{}'.format(self.entry.id), data=payload, **headers)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_full_update_missing_secretkey(self):
        """Should return 403 when no secretkey is given in headers"""
        payload = {
            'blog': 'http://testserver/api/blogs/1',
            'users': ['http://testserver/api/users/1'],
            'headline': 'New headline',
            'body_text': 'Some body text',
            'number_comments': 15,
            'scoring': 4.25
        }
        response = self.client.put(
            '/api/entries/{}?accesskey={}'.format(
                self.entry.id, self.user.accesskey), data=payload)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_full_update_invalid_accesskey(self):
        """Should return 403 when given accesskey is invalid"""
        payload = {
            'blog': 'http://testserver/api/blogs/1',
            'users': ['http://testserver/api/users/1'],
            'headline': 'New headline',
            'body_text': 'Some body text',
            'number_comments': 15,
            'scoring': 4.25
        }
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.put(
            '/api/entries/{}?accesskey={}'.format(
                self.entry.id, 'INVALID'), data=payload, **headers)
        expected = {'detail': 'Invalid Accesskey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_full_update_invalid_secretkey(self):
        """Should return 403 when given accesskey is invalid"""
        payload = {
            'blog': 'http://testserver/api/blogs/1',
            'users': ['http://testserver/api/users/1'],
            'headline': 'New headline',
            'body_text': 'Some body text',
            'number_comments': 15,
            'scoring': 4.25
        }
        headers = {'HTTP_X_SECRET_KEY': 'INVALID'}
        response = self.client.put(
            '/api/entries/{}?accesskey={}'.format(
                self.entry.id, self.user.accesskey), data=payload, **headers)
        expected = {'detail': 'Invalid Secretkey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_partial_update(self):
        """Should partial update an entry when given data is valid and user is authenticated"""
        payload = {
            'headline': 'New headline',
        }
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.patch(
            '/api/entries/{}?accesskey={}'.format(
                self.entry.id, self.user.accesskey), data=payload, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        entry = Entry.objects.get(id=self.entry.id)
        self.assertEqual(entry.headline, 'New headline')

    def test_partial_update_permission_denied(self):
        """Should return 403 when an user tries to partial update an entry from other user"""
        payload = {
            'headline': 'New headline',
        }
        headers = {'HTTP_X_SECRET_KEY': self.user_2.secretkey}
        response = self.client.patch(
            '/api/entries/{}?accesskey={}'.format(
                self.entry.id, self.user_2.accesskey), data=payload, **headers)
        expected = {
            'detail': 'You do not have permission to perform this action.'
        }
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_partial_update_missing_accesskey(self):
        """Should return 403 when no accesskey is given in url"""
        payload = {
            'headline': 'New headline',
        }
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.patch(
            '/api/entries/{}'.format(self.entry.id), data=payload, **headers)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_partial_update_missing_secretkey(self):
        """Should return 403 when no secretkey is given in headers"""
        payload = {
            'headline': 'New headline',
        }
        response = self.client.patch(
            '/api/entries/{}?accesskey={}'.format(
                self.entry.id, self.user.accesskey), data=payload)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_partial_update_invalid_accesskey(self):
        """Should return 403 when given accesskey is invalid"""
        payload = {
            'headline': 'New headline',
        }
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.patch(
            '/api/entries/{}?accesskey={}'.format(
                self.entry.id, 'INVALID'), data=payload, **headers)
        expected = {'detail': 'Invalid Accesskey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_partial_update_invalid_secretkey(self):
        """Should return 403 when given secretkey is invalid"""
        payload = {
            'headline': 'New headline',
        }
        headers = {'HTTP_X_SECRET_KEY': 'INVALID'}
        response = self.client.patch(
            '/api/entries/{}?accesskey={}'.format(
                self.entry.id, self.user.accesskey), data=payload, **headers)
        expected = {'detail': 'Invalid Secretkey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_delete(self):
        """Should delete user when given id is valid and user is authenticated"""
        self.assertEqual(Entry.objects.count(), 2)
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.delete(
            '/api/entries/{}?accesskey={}'.format(
                self.entry.id, self.user.accesskey), **headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Entry.objects.count(), 1)
        with self.assertRaises(Entry.DoesNotExist):
            Entry.objects.get(id=self.entry.id)

    def test_delete_permission_denied(self):
        """Should return 403 when an user tries to delete an entry from other user"""
        headers = {'HTTP_X_SECRET_KEY': self.user_2.secretkey}
        response = self.client.delete(
            '/api/entries/{}?accesskey={}'.format(
                self.entry.id, self.user_2.accesskey), **headers)
        expected = {
            'detail': 'You do not have permission to perform this action.'
        }
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_delete_missing_accesskey(self):
        """Should return 403 when no accesskey is given in url"""
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.delete(
            '/api/entries/{}'.format(self.entry.id), **headers)
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_delete_missing_secretkey(self):
        """Should return 403 when no secretkey is given in headers"""
        response = self.client.delete(
            '/api/entries/{}?accesskey={}'.format(
                self.entry.id, self.user.accesskey))
        expected = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_delete_invalid_accesskey(self):
        """Should return 403 when given accesskey is invalid"""
        headers = {'HTTP_X_SECRET_KEY': self.user.secretkey}
        response = self.client.delete(
            '/api/entries/{}?accesskey={}'.format(
                self.entry.id, 'INVALID'), **headers)
        expected = {'detail': 'Invalid Accesskey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)

    def test_delete_invalid_secretkey(self):
        """Should return 403 when given secretkey is invalid"""
        self.assertEqual(Entry.objects.count(), 2)
        headers = {'HTTP_X_SECRET_KEY': 'INVALID'}
        response = self.client.delete(
            '/api/entries/{}?accesskey={}'.format(
                self.entry.id, self.user.accesskey), **headers)
        expected = {'detail': 'Invalid Secretkey'}
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), expected)
