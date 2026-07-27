from deployer.deploy_honey import deploy_honey_users
from monitor.cloudtrail_monitor import (get_recent_events,monitor_events)
import time
deploy_honey_users()
while True:
    events=get_recent_events()
    monitor_events(events)
    time.sleep(30)