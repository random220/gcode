#!/usr/bin/env python3
import requests
import os, sys
import json

JIRA = {
    'url' : None,
    'token_file' : None,
    'token' : None,
}

def main():
    #set_jira('test')
    #issue_key = 'TESTPROJ-11'
    #print_issue(issue_key)

    set_jira('prod')
    #issue_key = 'SPARTA-18102'
    #print_issue(issue_key)
    #print("\n\n\n\n\n\n")

    people = 'omm,omandal'
    people = '"'+people.replace(',', '","')+'"'
    jql = f'assignee in ({people}) and status not in (Resolved,Closed,Blocked,Done,Released)'
    print_jql(jql)


def set_jira(env):
    if env == 'prod':
        JIRA['url'] = 'https://production.jira.site.com'
        JIRA['token_file'] = os.environ['HOME']+'/.ssh/token-jira-prod'
    elif env == 'test':
        JIRA['url'] = 'http://0.0.0.0:8080'
        JIRA['token_file'] = os.environ['HOME']+'/.ssh/token-jira-test'
    elif env == 'test9':
        JIRA['url'] = 'http://0.0.0.0:9090'
        JIRA['token_file'] = os.environ['HOME']+'/.ssh/token-jira-9090'
    else:
        print('Unknown env: '+env)
        sys.exit(1)
    if os.path.isfile(JIRA['token_file']):
        f = open(JIRA['token_file'], 'rt')
        JIRA['token'] = f.readline().strip()
        f.close()
    else:
        print('File not found '+JIRA['token_file'])
        sys.exit(1)

def print_issue(issue_key):
    # Set the headers with the access token for authentication
    access_token = JIRA['token']
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Make a request to get information about an issue (replace 'ISSUE-123' with your actual issue key)
    jira_url = JIRA['url']
    issue_url = f'{jira_url}/rest/api/2/issue/{issue_key}'
    #print(issue_url)
    response = requests.get(issue_url, headers=headers, verify=False)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        issue_data = response.json()
        print(f"Issue summary: {issue_data['fields']['summary']}")
    else:
        print(f"Failed to retrieve issue. Status code: {response.status_code}")
        print(response.text)

def print_jql(jql_query):
    startAt = 0
    maxResults = 1000
    total = 0
    while True:
        results_dict = fetch_query_results(startAt, maxResults, jql_query)
        
        # Print issue details from the search results
        for issue in results_dict['issues']:
            # print(f"Issue Key: {issue['key']}")
            # print(f"Summary: {issue['fields']['summary']}")
            # print(f"Status: {issue['fields']['status']['name']}")
            # print(f"Assignee: {issue['fields']['assignee']['displayName'] if issue['fields']['assignee'] else 'Unassigned'}")
            # print("------")
            if 'issuetype' in issue['fields']:
                print(f"{issue['key']}   {issue['fields']['issuetype']['name']}   {issue['fields']['status']['name']}   {issue['fields']['summary']}")
            else:
                print(f"{issue['key']}   XXXX   {issue['fields']['status']['name']}   {issue['fields']['summary']}")

        total = results_dict['total']
        startAt = startAt + maxResults
        if startAt >= total:
            break


def fetch_query_results(startAt, maxResults, jql_query):
    # Set the JQL query (replace 'your-jql-query' with your actual JQL query)
    #jql_query = 'project = "YOUR_PROJECT" AND status = "To Do"'

    # Define the Jira search API endpoint
    jira_url = JIRA['url']
    access_token = JIRA['token']
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    search_url = f'{jira_url}/rest/api/2/search'

        
    # Define the payload with the JQL query
    payload = {
        'jql': jql_query,
        'startAt': startAt,
        'maxResults': maxResults,  # You can adjust this based on your needs
        'fields': ['summary', 'status', 'assignee', 'issuetype']  # Specify the fields you want to retrieve
    }

    # Make a request to search for issues using the specified JQL query
    response = requests.post(search_url, headers=headers, json=payload, verify=False)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        search_results = response.json()
        return search_results;
    else:
        print(f"Failed to execute JQL query. Status code: {response.status_code}")
        print(response.text)
        sys.exit(1)

main()
print("    # ./example.py |sort|sed 's/-.*//'|uniq -c|sort -nr >projects.txt")
