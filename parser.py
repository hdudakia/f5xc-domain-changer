import sys
import requests
from difflib import unified_diff

def get_lb_json(api_url, api_token):
    headers = {'Authorization': f'APIToken {api_token}'}
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.json()

def modify_json(data, domains_file):
    print(f"DEBUG: domains_file = {domains_file}")  # Add this line for debug
    with open(domains_file, 'r') as file:
        domains = [line.strip() for line in file.readlines()]

    data['spec']['domains'] = domains
    return data

def put_lb_json(api_url, api_token, data):
    headers = {'Authorization': f'APIToken {api_token}', 'Content-Type': 'application/json'}
    response = requests.put(api_url, headers=headers, json=data)
    response.raise_for_status()

def print_domain_diff(original_domains, modified_domains):
    diff = unified_diff(original_domains, modified_domains)
    print("Domain Differences:")
    for line in diff:
        print(line)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python modify_json.py <api_url> <api_token> <domains_file>")
        sys.exit(1)

    api_url = sys.argv[1]
    api_token = sys.argv[2]
    domains_file = sys.argv[3]

    # Get the original state of LB domains
    lb_json = get_lb_json(api_url, api_token)
    original_domains = lb_json['spec']['domains']

    # Modify the LB JSON
    modified_data = modify_json(lb_json, domains_file)

    # PUT the modified LB JSON
    put_lb_json(api_url, api_token, modified_data)

    # Print the differences
    print_domain_diff(original_domains, modified_data['spec']['domains'])
