from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os.path
from google.auth.transport.requests import Request
from datetime import date, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']

class PostToGoogleCalendar:
    def __init__(self):
        self.credentials = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.credentials = pickle.load(token)
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.credentials = flow.run_local_server()
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.credentials, token)

        self.service = build('calendar', 'v3', credentials=self.credentials)
        result = self.service.calendarList().list().execute()
        self.calendar_id = result['items'][0]['id']


    def get_events(self):
        current_day_date = date.today()
        this_sunday_date = current_day_date - timedelta(days = (current_day_date.weekday() + 1) % 7)
        sunday_time = '08:00:00.000000Z'
        iso = f'{this_sunday_date}T{sunday_time}'
        events_result = self.service.events().list(calendarId=self.calendar_id, timeMin=iso,
                                                maxResults=500, singleEvents=True,
                                                orderBy='startTime').execute()
        return events_result.get('items', [])

    def create_event(self, event):
        if not self.already_exists(event):
            return self.service.events().insert(calendarId = self.calendar_id, body = event).execute() 
        else:
            return 'Event Already Exists'

    def already_exists(self, event):
        events = self.get_date_events(event['start']['dateTime'], self.get_events())
        event_list = [event['summary'] for event in events]
        if event['summary'] not in event_list:
            return False
        else:
            return True

    def get_date_events(self, date, events):
        lst = []
        date = date
        for event in events:
            if event.get('start').get('dateTime'):
                d1 = event['start']['dateTime']
                d1 = d1[:-6]
                if d1 == date:
                    lst.append(event)
        return lst

