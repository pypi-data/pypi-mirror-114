import datetime

from locust import task, HttpUser, between, SequentialTaskSet
import random
import time
from urllib.parse import urlencode


class LoadTest(SequentialTaskSet):
    _base_headers = {'Content-Type': 'application/json'}
    limit = 10
    offset = 0
    current_article = None
    query_params = {}
    session_id = None

    _recommended_articles = []
    _interesting_topics = []
    _subscribed_topics = []

    def headers(self):
        return {
            'sent-at': str(time.time())
        }

    def make_url(self, url, query_params: dict = None):
        if not query_params:
            query_params = {}

        if self.session_id:
            query_params['session'] = self.session_id

        encoded_query_string = urlencode(query_params)

        if encoded_query_string == '':
            return url

        return '{}?{}'.format(url, urlencode(query_params))

    def post(self, url, query_params: dict = None, data=None):
        url = self.make_url(url, query_params)

        return self.client.post(
            url,
            headers=self.headers(),
            data=data
        )

    def get(self, url, query_params: dict = None):
        if not url.startswith('/'):
            url = '/' + url

        url = self.make_url(url, query_params)

        return self.client.get(url)

    def subscribe_to_random_topic(self):
        interesting_topic = random.choice(self._interesting_topics)
        print('Subscribing to topic {}'.format(interesting_topic['title']))
        self.post('/subscribe_topic', data=dict(
            topic_id=interesting_topic['id']
        ))

    def navigate_to_home(self):
        self._recommended_articles = self.get('/user_articles/recommended').json()
        self._interesting_topics = self.get('/interesting_topics').json()
        self._subscribed_topics = self.get('/subscribed_topics').json()

    def read_random_article(self):
        """
        Fetches an article, uploads some user activity
        """
        article = random.choice(self._recommended_articles)
        print("Reading article {}".format(article['title']))
        self.get('user_article', query_params=dict(
            article_id=article['id']
        ))
        time.sleep(1)
        self.upload_scroll_activity()
        time.sleep(1)
        self.upload_scroll_activity()

    def upload_scroll_activity(self):
        response = self.post('/upload_user_activity_data', data=dict(
            event='UMR - SCROLL',
            extra_data='',
            time=datetime.datetime.utcnow().isoformat() + 'Z'
        ))

        if response.status_code != 200:
            print({'content':   response.content, 'status_code': response.status_code})
            exit(-1)

    @task()
    def task_register(self):
        """
        Register leads to the home page, which makes the articles load, as well as the interesting topics and the
        subscribed topics
        """
        random_number = random.randint(0, 10000000)

        response = self.post('/add_user/johan+{}@gmail.com'.format(random_number),
                         data=dict(password='password123', invite_code='please'))
        assert response.status_code == 200
        self.session_id = response.content.decode('utf-8')



        # Registering redirects to /articles page
        self.navigate_to_home()

    @task()
    def task_subscribe_to_topic(self):
        self.subscribe_to_random_topic()

    @task()
    def task_subscribe_to_another_topic(self):
        self.subscribe_to_random_topic()

    @task()
    def task_read_article(self):
        self.read_random_article()

    @task()
    def task_go_back_home(self):
        self.navigate_to_home()

    @task()
    def task_read_another_article(self):
        self.read_random_article()

    @task()
    def task_view_settings_page(self):
        self.get('/get_user_details')
        self.get('/system_languages')

    @task()
    def task_update_settings_page(self):
        self.post('/user_settings', data=dict(
            learned_language='fr',
            native_language='nl'
        ))
        self.navigate_to_home()


class User(HttpUser):
    tasks = [LoadTest]

    wait_time = between(7, 15)
