def format_alert(finding):
    return f"""
========================================
🚨 HoneyCloud Security Alert
========================================

Severity     : {finding["severity"]}

User         : {finding["username"]}

Action       : {finding["event_name"]}

Source IP    : {finding["source_ip"]}

Country      : {finding["country"]}

ISP          : {finding["isp"]}

Abuse Score  : {finding["abuse_score"]}

Tor Exit     : {"Yes" if finding["is_tor"] else "No"}

Event Time   : {finding["event_time"]}

========================================
"""

def print_alert(finding):
    message=format_alert(finding)
    print(message)