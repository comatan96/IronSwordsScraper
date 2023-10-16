import re


class NotificationPatterns:
    notification_header = re.compile(r'🚨\s+\*\*(.*?) \[(.*?)\] (\d+:\d+)\*\*')
    notification_area = re.compile(r'\*\*אזור (.*?)\*\*')
    city = re.compile('(.*?) \(.+\)')