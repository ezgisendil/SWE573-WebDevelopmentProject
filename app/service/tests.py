from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Offer, Post, Event, Feedback

# Create your tests here.
User = get_user_model()

class ServiceTest(TestCase):

    def setUp(self):
        newuser = User.objects.create_user('oguz', 'oguz@email.com', 'oguz123')
        self.newuser = newuser
    
    def test_valid_request(self):
        self.client.login(username=self.newuser.username, password=self.newuser.password)
        response = self.client.post("offer/create/", {"title": "this is a valid test"})
        self.assertTrue(response.status_code != 200)

    def test_search_url(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 302)

class OfferTest(TestCase):

    def setUp(self):
        newuser = User.objects.create_user('oguz', 'oguz@email.com', 'oguz123')
        self.newuser = newuser

        Offer.objects.create(title='yoga class',
                            content='online training',
                            location='Online',
                            date='2022-01-10',
                            author=self.newuser,
                            max_participants='3',
                            timecredit='1',
                            num_participants='2'
                            )
        

    def test_offer(self):
        offer = Offer.objects.get()
        self.assertEqual(offer.title, 'yoga class')
        self.assertEqual(offer.content, 'online training')
        self.assertEqual(offer.location, 'Online')
        self.assertEqual(offer.author, self.newuser)
        self.assertEqual(offer.max_participants, 3)
        self.assertEqual(offer.timecredit, 1)
        self.assertEqual(offer.num_participants, 2)

    def test_feedback(self):
        offer = Offer.objects.get()
        feedback = Feedback.objects.create(content='enjoyable yoga class',
                                            rating='5',
                                            receiver=self.newuser,
                                            sender=self.newuser,
                                            offer=offer)
        self.assertEqual(feedback.content, 'enjoyable yoga class')
        self.assertEqual(feedback.rating, '5')


class RequestTest(TestCase):

    def setUp(self):
        newuser = User.objects.create_user('oguz', 'oguz@email.com', 'oguz123')
        self.newuser = newuser

    def test_request(self):        
        request = Post.objects.create(title='Car Wash',
                                    content='Professional car wash',
                                    location='Istanbul',
                                    date='2022-01-17',
                                    author=self.newuser,
                                    duration='10:00')
        self.assertEqual(request.title, 'Car Wash')
        self.assertEqual(request.content, 'Professional car wash')
        self.assertEqual(request.location, 'Istanbul')
        self.assertEqual(request.date, '2022-01-17')

class EventTest(TestCase):

    def setUp(self):
        newuser = User.objects.create_user('oguz', 'oguz@email.com', 'oguz123')
        self.newuser = newuser

    def test_event(self):
        event = Event.objects.create(title='Coffee break',
                                    content='a coffee break with pet owners',
                                    location='Ankara',
                                    date='2022-01-29',
                                    author=self.newuser,
                                    duration='10:00')

        self.assertEqual(event.title, 'Coffee break')
        self.assertEqual(event.content, 'a coffee break with pet owners')
        self.assertEqual(event.max_participant, 3)
        self.assertEqual(event.location, 'Ankara')
        self.assertEqual(event.date, '2022-01-29')




         