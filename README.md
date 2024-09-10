# [WHOIS REST API 🌍](https://whois.com/whois/)

The WHOIS REST API is an unofficial tool that offers users the ability to perform WHOIS lookups for domain names. This API fetches raw WHOIS data and parses it into a structured JSON format, simplifying the integration of domain lookup features into your own applications.

## Features ✨

- Fetch and parse WHOIS data for any domain. 🌐
- Simple and clear JSON responses. 📄
- Interactive web interface for manual domain lookups. 🖥️
- Unofficial RESTful service built with Flask. 🛠️

## Vercel
Host your own instance of the crt.sh REST API on Vercel with a simple click using the button below.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%junioralive%2Fwhois)

## Installation 🛠️

Before you can run the WHOIS REST API, you need to ensure you have Python and Flask installed on your system. Follow these steps to set up the project on your local machine.

### Prerequisites

- Python 3.6+ 🐍
- pip 📦
- Flask 🌶️

### Clone the Repository

```bash
git clone https://github.com/junioralive/whois
cd whois-rest-api
```

### Install Dependencies

```bash
pip install flask requests beautifulsoup4
```

### Running the Application

Execute the following command to start the Flask server:

```bash
python app.py
```

The server will start running on `http://localhost:5000/`. You can navigate to this URL in a web browser to access the application.

## Usage 🚀

### Web Interface

Visit `http://localhost:5000/` in your browser to perform a WHOIS lookup via the web interface. Just enter the domain name and submit. 🔍

### API Endpoint

To use the API programmatically, send a GET request to the `/api/whois` endpoint with the domain parameter.

#### Example Request

```bash
curl "http://localhost:5000/api/whois?domain=example.com"
```

#### Response

The API will return the raw WHOIS data in JSON format. 📊

## **📞 Contact:**

[![Discord Server](https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/cwDTVKyKJz)
[![GitHub Project](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/junioralive)
[![Email](https://img.shields.io/badge/Email-D44638?style=for-the-badge&logo=gmail&logoColor=white)](mailto:support@junioralive.in)

## Disclaimer

Please note: This project is an independent endeavor and is not associated with any official WHOIS databases or services. The information provided is for informational purposes only and should not be used as a sole source for critical decisions. 🛑🔍
