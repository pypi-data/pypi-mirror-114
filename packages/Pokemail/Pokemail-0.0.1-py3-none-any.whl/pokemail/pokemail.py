import time
from requests import Session


class Pokemail:
    def __init__(self, username):
        self.username = username
        self.base_url = 'https://www.guerrillamail.com/ajax.php'
        self.session = Session()

        self.create_account()

    def create_account(self):
        params = (
            ('f', 'set_email_user'),
        )

        data = {
            'email_user': self.username,
            'lang': 'en',
            'site': 'guerrillamail.com',
            'in': ' Set cancel'
        }

        r = self.session.post(self.base_url, params=params, data=data)

        if r.status_code == 200:
            return True

    def check_email(self):
        params = (
            ('f', 'check_email'),
            ('seq', '1'),
            ('site', 'guerrillamail.com'),
            ('in', self.username),
            ('_', str(round(time.time()))),
        )
        return self.session.get(self.base_url, params=params)

    def fetch_email(self, mail_id):
        params = (
            ('f', 'fetch_email'),
            ('seq', mail_id),
            ('site', 'guerrillamail.com'),
            ('in', self.username),
            ('_', str(round(time.time()))),
        )
        return self.session.get(self.base_url, params=params)
