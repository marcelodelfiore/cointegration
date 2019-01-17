import requests

class Tradezone:

    def __init__(self):
        req = requests.get('http://localhost:31008/login?product=A762C7B7-AB84-485B-8D09-4EB948572348&version=2.0.0.0&description=teste')
        self.session_id = req.text

    def logout_command(self):
        request_string = "http://localhost:31008/logout?id=" + self.session_id
        requests.get(request_string)

    def daily_quote_history(self, symbol, start_date, end_date):
        request_string = "http://localhost:31008/gethistory?id=" + self.session_id + "&symbol=" + symbol + "&from=" \
                         + start_date + " " + "10:00:00&to=" + end_date + " " + "18:00:00&size=1440&maxbars=0"
        req = requests.get(request_string)
        return req.text
