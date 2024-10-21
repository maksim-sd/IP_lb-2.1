from http.server import SimpleHTTPRequestHandler, HTTPServer
from jinja2 import Environment, PackageLoader, select_autoescape
import json, os
from datetime import datetime


def advanteges_load():
    if os.path.exists("./data/advanteges.json"):
        with open("./data/advanteges.json", "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def tariffs_load():
    if os.path.exists("./data/tariffs.json"):
        with open("./data/tariffs.json", "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def send_bid(bid):
    with open("./data/bid.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        data.append({f"bid-{datetime.now().strftime("%d/%m%/Y-%H:%M:%S")}": bid})

    with open("./data/bid.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


class MySiteHandler(SimpleHTTPRequestHandler):
    env = Environment(
        loader = PackageLoader("main"),
        autoescape = select_autoescape()
    )
    
    def do_GET(self):
        if self.path == "/":
            self.render_index()
        elif self.path.startswith("/media/"):
            super().do_GET()
        elif self.path == "/advanteges":
            self.render_advanteges()
        elif self.path == "/tariffs":
            self.render_tariffs()
        elif self.path == "/contacts":
            self.render_contacts()
        else:
            self.render_error()

    def do_POST(self):
        if self.path == "/send_bid":
            content_len = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_len).decode("utf-8").split("&")

            bid_dict = {}

            for item in post_data:
                if item != "":
                    key, value = item.split("=")
                    bid_dict[key] = value

            send_bid(bid_dict)
            self.render_contacts()

    def render_error(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<h1 style='text-align: center;'>Not Found 404</h1>".encode("utf-8"))

    def render_index(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        template = self.env.get_template("index.html").render()
        self.wfile.write(template.encode("utf-8"))

    def render_advanteges(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        template = self.env.get_template("advanteges.html").render(advanteges=advanteges_load())
        self.wfile.write(template.encode("utf-8"))
    
    def render_tariffs(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        template = self.env.get_template("tariffs.html").render(tariffs=tariffs_load())
        self.wfile.write(template.encode("utf-8"))

    def render_contacts(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        template = self.env.get_template("contacts.html").render()
        self.wfile.write(template.encode("utf-8"))


if __name__ == "__main__":
    httpd = HTTPServer(("", 8000), MySiteHandler)
    print("Server start...")
    httpd.serve_forever()