# redmine_zabbix

It creates alerts table at redmine from zabbix since start_time (like %d/%m/%Y) untill end_time (like %d/%m/%Y) for hardcoded user (userid=7) and mediatypeids (mediatypeid 3 is SMS, and mediatypeid 4 is Telegram notification).

Usage is triger_table.py -t <redmine_token> -n <wiki_page_name> -r <redmine_hostname> -z <zabbix_hostname> -u <zabbix_web_user> -p <zabbix_user_password> -s <start_time> -e <end_time>


