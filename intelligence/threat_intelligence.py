import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY=os.getenv("ABUSEIPDB_API_KEY")

URL = "https://api.abuseipdb.com/api/v2/check"

def get_ip_reputation(ip):
    if not API_KEY:
        raise ValueError(
            "ABUSEIPDB_API_KEY not found in environment variables."
        )
    headers={
        "Key":API_KEY,
        "Accept":"application/json"
    }
    params={
        "ipAddress":ip,
        "maxAgeInDays":90
    }
    try:
        response=requests.get(
            URL,
            headers=headers,
            params=params,
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Threat intelligence lookup failed: {e}")
        return None
    data=response.json()['data']
    return{
        "ip":data["ipAddress"],
        "country": data.get("countryCode"),
        "isp": data.get("isp"),
        "domain": data.get("domain"),
        "usage_type": data.get("usageType"),
        "abuse_score": data.get("abuseConfidenceScore"),
        "total_reports": data.get("totalReports"),
        "is_tor": data.get("isTor"),
        "is_whitelisted": data.get("isWhitelisted"),
        "last_reported": data.get("lastReportedAt"),
        "is_malicious": data.get("abuseConfidenceScore", 0) >= 50
    }

