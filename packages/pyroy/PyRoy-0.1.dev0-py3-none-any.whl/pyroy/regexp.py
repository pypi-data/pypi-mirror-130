import re

_IPV4 = (
    r'^(?:(?:25[0-5]|2[0-4][\d]|[01]?[\d][\d]?)\.){3}'
    r'(?:25[0-5]|2[0-4][\d]|[01]?[\d][\d]?)$'
)
IPV4 = re.compile(_IPV4, flags=re.IGNORECASE)
IPV4_BINARY = re.compile(_IPV4.encode('ASCII'), flags=re.IGNORECASE)

_IPV6 = (
    r'^(?:(?:(?:[A-F\d]{1,4}:){6}|(?=(?:[A-F\d]{0,4}:){0,6}'
    r'(?:[\d]{1,3}\.){3}[\d]{1,3}$)(([A-F\d]{1,4}:){0,5}|:)'
    r'((:[A-F\d]{1,4}){1,5}:|:)|::(?:[A-F\d]{1,4}:){5})'
    r'(?:(?:25[0-5]|2[0-4][\d]|1[\d][\d]|[1-9]?[\d])\.){3}'
    r'(?:25[0-5]|2[0-4][\d]|1[\d][\d]|[1-9]?[\d])|(?:[A-F\d]{1,4}:){7}'
    r'[A-F\d]{1,4}|(?=(?:[A-F\d]{0,4}:){0,7}[A-F\d]{0,4}$)'
    r'(([A-F\d]{1,4}:){1,7}|:)((:[A-F\d]{1,4}){1,7}|:)|(?:[A-F\d]{1,4}:){7}'
    r':|:(:[A-F\d]{1,4}){7})$'
)
IPV6 = re.compile(_IPV6, flags=re.IGNORECASE)
IPV6_BINARY = re.compile(_IPV6.encode('ASCII'), flags=re.IGNORECASE)

_UUID4 = r'^[a-f\d]{8}-[a-f\d]{4}-[1-5][a-f\d]{3}-[89ab][a-f\d]{3}-[a-f\d]{12}$'
UUID4 = re.compile(_UUID4, flags=re.IGNORECASE)
UUID4_BINARY = re.compile(_UUID4.encode('ASCII'), flags=re.IGNORECASE)
