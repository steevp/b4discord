import re
from xmlrpc.client import ServerProxy, Transport, Binary, Error

class Bot:

    API_URL = "http://yourewinner.com/winnerapi/mobiquo.php"
    PAGE_SIZE = 15 # number of posts per page
    
    def __init__(self):
        self.client = ServerProxy(self.API_URL, CookiesTransport())
        self.logged_in = False

    def login(self, username, password):
        username = Binary(username.encode("utf-8"))
        password = Binary(password.encode("utf-8"))
        try:
            r = self.client.login(username, password)
            self.logged_in = r["result"]
        except Error as e:
            print("ERROR:", e)
            self.logged_in = False
    
    def get_recent(self, page=1):
        start = self.PAGE_SIZE * page - self.PAGE_SIZE
        end = self.PAGE_SIZE * page - 1
        try:
            r = self.client.get_new_topic(start, end)
            for t in r:
                yield PostWrapper(t)
        except Error as e:
            print("ERROR:", e)

    def new_topic(self, board, subject, msg):
        if not self.logged_in:
            raise Exception("You must be logged in to do that!")
        subject = Binary(subject.encode("utf-8"))
        msg = Binary(msg.encode("utf-8"))
        try:
            r = self.client.new_topic(board, subject, msg)
            return "http://yourewinner.com/index.php?topic={}.0".format(r["topic_id"])
        except Error as e:
            print("ERROR:", e)

    def rate_post(self, url, rating):
        p = re.compile(r'topic=(\d+).msg(\d+)')
        m = p.search(url)
        if m:
            topic, post = m.groups()
            for i in range(2):
                try:
                    self.client.rate_post(post, rating)
                except Error as e:
                    print("ERROR:", e)

class CookiesTransport(Transport):
    # Custom Transport that saves cookies
    def __init__(self):
        super().__init__()
        self._cookies = []
    
    def send_headers(self, connection, headers):
        if self._cookies:
           connection.putheader("Cookie", "; ".join(self._cookies))
        super().send_headers(connection, headers)

    def parse_response(self, response):
        cookie_headers = response.msg.get_all("Set-Cookie")
        if cookie_headers:
            for header in cookie_headers:
                cookie = header.split(";", 1)[0]
                self._cookies.append(cookie)
        return super().parse_response(response)

class PostWrapper:
    
    def __init__(self, obj):
        self.author = obj["post_author_name"].data.decode("utf-8")
        self.msg = obj["short_content"].data.decode("utf-8")
        self.board_id = obj["forum_id"]
        self.board_name = obj["forum_name"].data.decode("utf-8")
        self.topic_id = obj["topic_id"]
        self.post_time = obj["post_time"]

    def __str__(self):
        return "{}: {}".format(self.author, self.msg)

if __name__ == "__main__":
    b = Bot()
    b.login("b", "123456")
    for r in b.get_recent():
        print(r)
