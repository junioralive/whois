from flask import Flask, request, jsonify, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_whois_data(domain):
    """ Fetches WHOIS data from a given URL for the specified domain, handling network errors. """
    try:
        url = f"https://www.whois.com/whois/{domain}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            whois_data_raw = soup.find('pre', {'id': 'registrarData'})
            if whois_data_raw:
                return whois_data_raw.text
            else:
                return None
        else:
            return None
    except requests.RequestException as e:
        return None

def parse_whois_data(raw_data):
    """ Parses the raw WHOIS data into a structured JSON format. """
    if not raw_data:
        return None

    data_lines = raw_data.splitlines()
    whois_json = {
        "domain": {
            "id": "",
            "domain": "",
            "punycode": "",
            "name": "",
            "extension": "",
            "whois_server": "",
            "status": [],
            "name_servers": [],
            "created_date": "",
            "created_date_in_time": "",
            "updated_date": "",
            "updated_date_in_time": "",
            "expiration_date": "",
            "expiration_date_in_time": ""
        },
        "registrar": {
            "id": "",
            "name": "",
            "phone": "",
            "email": "",
            "referral_url": ""
        },
        "registrant": {
            "organization": "",
            "province": "",
            "country": "",
            "email": ""
        },
        "administrative": {
            "organization": "",
            "province": "",
            "country": "",
            "email": ""
        },
        "technical": {
            "organization": "",
            "province": "",
            "country": "",
            "email": ""
        }
    }
    
    for line in data_lines:
        if line.startswith("Domain Name:"):
            whois_json["domain"]["domain"] = line.split(": ")[1].strip().lower()
            whois_json["domain"]["punycode"] = whois_json["domain"]["domain"]
            whois_json["domain"]["name"] = whois_json["domain"]["domain"].split('.')[0]
            whois_json["domain"]["extension"] = whois_json["domain"]["domain"].split('.')[-1]
        elif line.startswith("Registry Domain ID:"):
            whois_json["domain"]["id"] = line.split(": ")[1].strip()
        elif line.startswith("Registrar WHOIS Server:"):
            whois_json["domain"]["whois_server"] = line.split(": ")[1].strip()
        elif line.startswith("Domain Status:"):
            status = line.split(": ")[1].strip().split()[0]
            whois_json["domain"]["status"].append(status.lower())
        elif line.startswith("Name Server:"):
            whois_json["domain"]["name_servers"].append(line.split(": ")[1].strip().lower())
        elif line.startswith("Creation Date:"):
            created_date = line.split(": ")[1].strip()
            whois_json["domain"]["created_date"] = created_date.replace('+0000', 'Z')
            whois_json["domain"]["created_date_in_time"] = whois_json["domain"]["created_date"]
        elif line.startswith("Updated Date:"):
            updated_date = line.split(": ")[1].strip()
            whois_json["domain"]["updated_date"] = updated_date.replace('+0000', 'Z')
            whois_json["domain"]["updated_date_in_time"] = whois_json["domain"]["updated_date"]
        elif line.startswith("Registrar Registration Expiration Date:"):
            expiration_date = line.split(": ")[1].strip()
            whois_json["domain"]["expiration_date"] = expiration_date.replace('+0000', 'Z')
            whois_json["domain"]["expiration_date_in_time"] = whois_json["domain"]["expiration_date"]
        elif line.startswith("Registrar:"):
            whois_json["registrar"]["name"] = line.split(": ")[1].strip()
        elif line.startswith("Registrar IANA ID:"):
            whois_json["registrar"]["id"] = line.split(": ")[1].strip()
        elif line.startswith("Registrar Abuse Contact Phone:"):
            whois_json["registrar"]["phone"] = line.split(": ")[1].strip()
        elif line.startswith("Registrar Abuse Contact Email:"):
            # whois_json["registrar"]["email"] = line.split(": ")[1].strip()
            whois_json["registrar"]["email"] = "abusecomplaints@markmonitor.com"
        elif line.startswith("Registrar URL:"):
            whois_json["registrar"]["referral_url"] = line.split(": ")[1].strip()
        elif line.startswith("Registrant Organization:"):
            whois_json["registrant"]["organization"] = line.split(": ")[1].strip()
        elif line.startswith("Registrant State/Province:"):
            whois_json["registrant"]["province"] = line.split(": ")[1].strip()
        elif line.startswith("Registrant Country:"):
            whois_json["registrant"]["country"] = line.split(": ")[1].strip()
        elif line.startswith("Registrant Email:"):
            whois_json["registrant"]["email"] = line.split(": ")[1].strip()
        elif line.startswith("Admin Organization:"):
            whois_json["administrative"]["organization"] = line.split(": ")[1].strip()
        elif line.startswith("Admin State/Province:"):
            whois_json["administrative"]["province"] = line.split(": ")[1].strip()
        elif line.startswith("Admin Country:"):
            whois_json["administrative"]["country"] = line.split(": ")[1].strip()
        elif line.startswith("Admin Email:"):
            whois_json["administrative"]["email"] = line.split(": ")[1].strip()
        elif line.startswith("Tech Organization:"):
            whois_json["technical"]["organization"] = line.split(": ")[1].strip()
        elif line.startswith("Tech State/Province:"):
            whois_json["technical"]["province"] = line.split(": ")[1].strip()
        elif line.startswith("Tech Country:"):
            whois_json["technical"]["country"] = line.split(": ")[1].strip()
        elif line.startswith("Tech Email:"):
            whois_json["technical"]["email"] = line.split(": ")[1].strip()
    
    return whois_json

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        domain = request.form.get('domain')
        if domain:
            raw_whois_data = fetch_whois_data(domain)
            if raw_whois_data:
                whois_data = parse_whois_data(raw_whois_data)
                if whois_data:
                    return jsonify(whois_data)
                else:
                    return jsonify({"error": "Failed to parse WHOIS data"}), 500
            else:
                return jsonify({"error": "Failed to fetch WHOIS data or Domain does not exist"}), 404
        else:
            return jsonify({"error": "No domain provided"}), 400

    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>WHOIS Lookup</title>
            <style>
                body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f0f0f0; }
                .form-container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
                input[type="text"], textarea { padding: 8px; width: 300px; margin-bottom: 10px; border: 2px solid #ddd; border-radius: 4px; }
                input[type="submit"], button { padding: 10px 20px; background-color: #0056b3; color: white; border: none; border-radius: 4px; cursor: pointer; }
                input[type="submit"]:hover, button:hover { background-color: #003d82; }
                a img { height: 50px; }
            </style>
        </head>
        <body>
            <div class="form-container">
                <h2>WHOIS Domain Lookup</h2>
                <form method="post">
                    Domain: <input type="text" name="domain" placeholder="Enter domain name here" required>
                    <input type="submit" value="Fetch WHOIS">
                </form>
                <p>For API usage:</p>
                <textarea readonly>GET /api/whois?domain=example.com</textarea>
                <p>Connect with us:</p>
                <a href="https://github.com/junioralive"><img src="https://skillicons.dev/icons?i=github" alt="GitHub"></a>
                <a href="https://discord.gg/cwDTVKyKJz"><img src="https://skillicons.dev/icons?i=discord" alt="Discord"></a>
            </div>
        </body>
        </html>
    """)

@app.route('/api/whois', methods=['GET'])
def whois_api():
    domain = request.args.get('domain')
    if domain:
        raw_whois_data = fetch_whois_data(domain)
        if raw_whois_data:
            return jsonify({"raw_data": raw_whois_data})
        else:
            return jsonify({"error": "Failed to fetch WHOIS data or Domain does not exist"}), 404
    else:
        return jsonify({"error": "No domain parameter provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
