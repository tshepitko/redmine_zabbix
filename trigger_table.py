from optparse import OptionParser
from pyzabbix import ZabbixAPI
import time
import datetime
import requests

def arguments():
   usage = "usage: %prog -t <api_token> -n <pagename> -r <redmine_hostname> -z <zabbix_hostname> -u <zabbix_user> -p <zabbix_user_password> -s <start_time> -e <end_time>"
   parser = OptionParser(usage)
   parser.add_option("-t", "--token", action="store", type="str", dest="token", help="api token for redmine")
   parser.add_option("-n", "--pagename", action="store", type="str", dest="page_name", help="wiki page name")
   parser.add_option("-r", "--redmine_hostname", action="store", type="str", dest="redmine_hostname", help="redmine hostname")
   parser.add_option("-z", "--zabbix_hostname", action="store", type="str", dest="zabbix_hostname", help="zabbix hostname")
   parser.add_option("-u", "--zabbix_user", action="store", type="str", dest="zabbix_user", help="zabbix web user")
   parser.add_option("-p", "--zabbix_password", action="store", type="str", dest="zabbix_password", help="redmine web user password")
   parser.add_option("-s", "--start_time", action="store", type="str", dest="start_time", help="start time kind of %d/%m/%Y")
   parser.add_option("-e", "--end_time", action="store", type="str", dest="end_time", help="end time kind of %d/%m/%Y")
   (options, args) = parser.parse_args()
   if options.token is None:
       parser.error("No token")
   if options.page_name is None:
       parser.error("No wiki page name")
   if options.redmine_hostname is None:
       parser.error("No redmine hostname")
   if options.zabbix_hostname is None:
       parser.error("No zabbix hostname")
   if options.zabbix_user is None:
       parser.error("No zabbix user")
   if options.zabbix_password is None:
       parser.error("No zabbix user password")
   if options.start_time is None:
       parser.error("No start time")
   if options.end_time is None:
       parser.error("No end time")
   return options

def get_zabbix_token():
    options = arguments()
    zabbix_url, zabbix_user, zabbix_password = options.zabbix_hostname, options.zabbix_user, options.zabbix_password
    if 'http' not in zabbix_url:
        zabbix_url = 'http://'+zabbix_url
    try:
        zabbix = ZabbixAPI(zabbix_url,user=zabbix_user,password=zabbix_password)
    except:
        print('Invalid zabbix hostname or credentials')
    else:
        return(zabbix)

def get_zabbix_alerts():
    options = arguments()
    start_time = str(time.mktime(datetime.datetime.strptime(options.start_time, "%d/%m/%Y").timetuple())).split('.')[0]
    end_time = str(time.mktime(datetime.datetime.strptime(options.end_time, "%d/%m/%Y").timetuple())).split('.')[0]
    zabbix = get_zabbix_token()
    if zabbix != None:
        alerts = sorted(zabbix.alert.get(userids='7',mediatypeids=['3','4'],time_from=start_time,tim_till=end_time), key=lambda x: x['subject']) #Select alerts for user with userid=7 with mediatypeids=[3,4] (3- SMS, 4- Telegram) since start_time until end_time
        uniq_sorted_alerts = sorted(set([i['subject'] for i in alerts if 'PROBLEM' in i['subject']]))
        return(uniq_sorted_alerts)

if __name__ == "__main__":
    alerts = get_zabbix_alerts()
    options = arguments()
    token, rm , page_name = options.token, options.redmine_hostname, options.page_name
    text = '|=.*Trigger subject*|=.*User1*|=.*User2*|=.*User3*|=.*User4*|'
    for alert in alerts:
        text=text+ '\n|'+alert+'|||||'
    put_xml = '<wiki_page><text>'+text+'</text></wiki_page>'
    r = requests.put('http://' + rm + page_name + '?key=' + token, data=put_xml, headers={"Content-Type":"application/xml"})
    if r.status_code != 200:
        print("Something went wrong. Server status : " + str(r.status_code) + ". Server answer : " + r.text)
