import re

ERRORS = {}

def check_visitor_name(data: dict):
    print("dataaa",data)
    print("visi name",data.get("visitor_name"))
    return bool(data.get("visitor_name"))

def check_client_ip(data: dict):
    return bool(data.get("client_ip"))

def check_location(data: dict):
    return bool(data.get("location"))

def check_name_in_greeting(data: dict):
    return data.get("visitor_name") in data.get("greeting")

def check_greeting(data: dict):  
    return bool(data.get("greeting"))

def validate_visitor(data: dict):
    if not check_visitor_name(data):
        ERRORS["visitor_name"] = "Visitor name is required" 

    if not check_client_ip(data):
        ERRORS["client_ip"] = "Client ip is required" 

    if not check_location(data):
        ERRORS["location"] = "Location is required" 

    if not check_name_in_greeting(data):
        ERRORS["name_in_greeting"] = "Name in greeting is required" 

    if not check_greeting(data):
        ERRORS["greeting"] = "Greeting is required" 

    return bool(ERRORS)


def assign_score(data: dict):
    total_score = 0
    if check_visitor_name(data):
        total_score += 2
    if check_client_ip(data):
        total_score += 2
    if check_location(data):
        total_score += 2
    if check_name_in_greeting(data):
        total_score += 2
    if check_greeting(data):
        total_score += 2
    return total_score

def is_valid_ip(ip: str) -> bool:
    
    # IPv4 pattern
    ipv4_pattern = r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

    # IPv4-mapped IPv6 pattern
    ipv4_mapped_ipv6_pattern = r'::ffff:((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

    # Combined pattern
    combined_pattern = re.compile(
        r'^(' + ipv4_pattern + r'|' + ipv4_mapped_ipv6_pattern + r')$'
    )
    # ip_regex = re.compile(
    #     r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
    #     r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    # )
    return bool(combined_pattern.match(ip))
