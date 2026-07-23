import boto3
import json
from config import HONEY_USERNAME
from intelligence.threat_intelligence import get_ip_reputation
from monitor.findings import create_finding
from alerts.notifier import print_alert



cloudtrail=boto3.client("cloudtrail")
def get_recent_events():
    response=cloudtrail.lookup_events(MaxResults=5)
    return response["Events"]



def monitor_events(events):
    for event in events:
        event_detail=extract_event_details(event)
        if event_detail['username'] in HONEY_USERNAME:
             reputation=get_ip_reputation(event_detail['source_ip'])
             finding=create_finding(event_detail,reputation)
             if finding:
                  print_alert(finding)
        


def extract_event_details(event):
        event_detail={}
        event_data=json.loads(event["CloudTrailEvent"])
        user_details=event_data.get('userIdentity',{})
        event_detail['event_name']=event['EventName']
        event_detail['event_time']=event['EventTime']
        event_detail['source_ip']=event_data.get('sourceIPAddress')
        event_detail['username']=user_details.get('userName',"Unknown")
        event_detail["event_source"] = event_data.get("eventSource")
        return event_detail


