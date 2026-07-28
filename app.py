from flask import Flask, render_template,send_file
import json
import csv
from config import HONEY_BUCKETNAMES,HONEY_USERNAMES,HONEY_USERS
from collections import Counter

app = Flask(__name__)

@app.route("/")
def dashboard():

    with open("findings.json", "r") as file:
        findings = json.load(file)
    country_counts = Counter( finding["country"]for finding in findings)
    top_countries = country_counts.most_common(5)
    max_country_hits = max(country_counts.values()) if country_counts else 1
    COUNTRY_NAMES = {
    "IN": "India",
    "US": "United States",
    "RU": "Russia",
    "CN": "China",
    "DE": "Germany",
    "SG": "Singapore",
    "GB": "United Kingdom",
    "JP": "Japan"
}
    # Statistics
    total_findings = len(findings)

    critical_count = sum(
        1 for f in findings
        if f["severity"] == "Critical"
    )

    high_count = sum(
        1 for f in findings
        if f["severity"] == "High"
    )

    medium_count = sum(
        1 for f in findings
        if f["severity"] == "Medium"
    )
    latest_finding = findings[-1] if findings else None
    latest_event_time = latest_finding["event_time"] if latest_finding else "No Events"
    honey_users = len(HONEY_USERNAMES)
    honey_buckets = len(HONEY_BUCKETNAMES)
    decoy_files = 0
    for user in HONEY_USERS:
        decoy_files += len(user["files"])
    unique_ips = len(set(f["source_ip"] for f in findings))
    max_abuse_score = max(  (f["abuse_score"] for f in findings),default=0)
    tor_nodes = sum(1 
                    for f in findings
                    if f["is_tor"])
    average_abuse_score = (
        round(
            sum(f["abuse_score"] for f in findings) / len(findings),
            1
        )if findings else 0)
    print("TOR Nodes:", tor_nodes)
    return render_template(
        "index.html",
        total_findings=total_findings,
        critical_count=critical_count,
        high_count=high_count,
        medium_count=medium_count,
        findings=findings,
        latest_finding=latest_finding,
        latest_event_time=latest_event_time,
        honey_users=honey_users,
        honey_buckets=honey_buckets,
        decoy_files=decoy_files,
        top_countries=top_countries,
        max_country_hits=max_country_hits,
        COUNTRY_NAMES=COUNTRY_NAMES,
        unique_ips=unique_ips,
        max_abuse_score=max_abuse_score,
        tor_nodes=tor_nodes,
        average_abuse_score=average_abuse_score
    )


@app.route("/export")
def export_csv():

    with open("findings.json", "r") as file:
        findings = json.load(file)

    with open("findings.csv", "w", newline="") as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow([
            "Severity",
            "Event",
            "Time",
            "User",
            "Source IP",
            "Country",
            "Abuse Score"
        ])

        for f in findings:
            writer.writerow([
                f["severity"],
                f["event_name"],
                f["event_time"],
                f["username"],
                f["source_ip"],
                f["country"],
                f["abuse_score"]
            ])

    return send_file(
        "findings.csv",
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)