def create_finding(event_details,reputation):
    if reputation is None:
        return None
    abuse_score=reputation['abuse_score']
    if abuse_score>=75:
        severity="Critical"
    elif abuse_score>=25 :
        severity="High"
    else:
        severity="Medium"
    return {
        "severity":severity,
        "event_name":event_details["event_name"],
        "event_time":event_details["event_time"],
        "username":event_details["username"],
        "source_ip":event_details["source_ip"],
        "country":reputation['country'],
        "isp":reputation['isp'],
        "abuse_score":reputation['abuse_score'],
        "is_tor":reputation['is_tor']
    }