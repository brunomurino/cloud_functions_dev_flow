import helpers
from helpers import *

class mailerlite_interface:

    def __init__(self, api_key):
        self.headers = {'X-MailerLite-ApiKey': api_key}
        self.base_url = 'https://api.mailerlite.com/api/v2'

    def get_data(self, url):
        response = requests.get(self.base_url+url, headers=self.headers)
        data = json.loads(response.text)
        return data

    def get_campaigns(self):
        return self.get_data('/campaigns/sent')

    def get_subscribers(self):
        return self.get_data('/subscribers')

    def get_groups(self):
        return self.get_data('/groups')
    
    def get_groups_members(self, group_id):
        return self.get_data(f'/groups/{group_id}/subscribers')

    def subscriber_activity_type(self, subs_id, act_type):
        return self.get_data(f'/subscribers/{subs_id}/activity/{act_type}')

    def subscriber_activity(self, subs_id):
        return self.get_data(f'/subscribers/{subs_id}/activity')
