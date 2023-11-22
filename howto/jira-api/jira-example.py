#!/usr/bin/env python3
import requests
import os, sys
import shutil
import json
import re

confroot   = os.environ['HOME']+'/.jira'
conf_file  = confroot + '/conf'
savedconfs = confroot + '/confs'
qdir       = confroot + '/queries'
os.makedirs(savedconfs, exist_ok = True)
os.makedirs(qdir, exist_ok = True)

JIRA = {
    'url' : None,
    'token_file' : None,
    'token' : None,
}

def main():
    os.umask(0o077)
    readenv()
    if JIRA['url'] is None:
        set_jira('test')
        writeenv()
    #issue_key = 'SPARTA-18102'
    #print_issue(issue_key)

    if len(sys.argv) == 1:
        print_help()
        sys.exit(0)

    if sys.argv[1] == 'q':
        do_query()
        sys.exit(0)
    elif sys.argv[1] == 'set':
        do_setup()
        sys.exit(0)
    elif sys.argv[1] == 'cm':
        do_comment()
        sys.exit(0)

def do_comment():
    comment = ''
    if sys.argv[1] == 'cm' and len(sys.argv) == 2:
        print("Need issue")
        sys.exit(1)
    elif sys.argv[1] == 'cm' and len(sys.argv) == 3:
        issue_key = sys.argv[2]
        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break
        comment = '\n'.join(lines)
    elif sys.argv[1] == 'cm' and len(sys.argv) == 4:
        issue_key = sys.argv[2]
        comment = sys.argv[3]
    add_comment(issue_key, comment)

def add_comment(issue_key, comment_text):
    # Define the Jira search API endpoint
    jira_url = JIRA['url']
    access_token = JIRA['token']
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Set the Jira API endpoint for adding comments to an issue
    comment_url = f'{jira_url}/rest/api/2/issue/{issue_key}/comment'

    # Create a payload with the comment text
    payload = {
        'body': comment_text
    }

    # Make a POST request to add a comment to the issue
    response = requests.post(comment_url, headers=headers, json=payload)

    # Check if the request was successful (HTTP status code 201 for created)
    if response.status_code == 201:
        print("Comment added successfully.")
    else:
        print(f"Failed to add comment. Status code: {response.status_code}")
        print(response.text)


def do_query():
    if sys.argv[1] == 'q' and len(sys.argv) == 2:
        os.system(f'find "{qdir}"/*')
        sys.exit(0)
    elif sys.argv[1] == 'q' and len(sys.argv) == 3:
        m = re.search(r'^n:(.+)', sys.argv[2])
        if m:
            qname = m.group(1)
            qfile = qname
            if not os.path.isfile(qfile):
                qfile = f'{qdir}/{qname}'
            if not os.path.isfile(qfile):
                print(f'File not found {qfile}')
                sys.exit(1)
            f = open(qfile, 'r')
            jql = normalize_query(f.read())
            f.close()
        else:
            jql = normalize_query(sys.argv[2])
        
        # people = 'omm,omandal'
        # people = 'omm,omandal,xxx'
        # people = '"'+people.replace(',', '","')+'"'
        # jql = f'assignee in ({people}) and status not in (Resolved,Closed,Blocked,Done,Released)'
        # jql = f'assignee in ({people}) and status not in (Resolved,Closed,Done)'
        # print(jql)
        run_jql(jql)

def normalize_query(q):
    q = re.sub(r'\s+', ' ', q, count=0, flags=re.S)
    return q

def print_help():
    print("""
# j set               # get url and token
# j q                 # list saved queries
# j q <'QUERY TEXT'>  #
# j q n:<query name>  # Execute named query
# j cm|com issue      # add comment
# ---
# j c irp2323         # create issue with label "manual-rehab"
# j l                 # list open issues with label "manual-rehab"
# j a issue who       # assign
# j cl issue          # close
# j lb issue label    # add label
"""
    )

def writeenv():
    os.makedirs(confroot, exist_ok = True)
    f = open(conf_file, 'w')
    f.write(json.dumps(JIRA, indent=4, sort_keys=True))
    f.write('\n')
    
def readenv():
    os.makedirs(os.path.dirname(conf_file), exist_ok = True)
    if os.path.isfile(conf_file):
        f = open(conf_file, 'r')
        j = json.load(f)
        f.close()

        for key in j:
            JIRA[key] = j[key]

def do_setup():
    # j set
    if len(sys.argv) == 2:
        os.system(f'find "{savedconfs}"/*')
        sys.exit(0)
    elif len(sys.argv) == 3:
        # j set test
        saved_conf_file = f'{savedconfs}/{sys.argv[2]}'
        if os.path.isfile(saved_conf_file):
            shutil.copy2(saved_conf_file, conf_file)
            readenv()
            sys.exit(0)
        else:
            print(f"File not found {saved_conf_file}")
            sys.exit(1)
    else:
        JIRA['token_file'] = None
        print('URL: something like https://production.jira.site.com')
        JIRA['url'] = input().strip()
        print('Jira token:')
        JIRA['token'] = input().strip()

    writeenv()

def set_jira(env):

    if env == 'prod':
        JIRA['url'] = 'https://production.jira.site.com'
        JIRA['token_file'] = os.environ['HOME']+'/.ssh/token-jira-prod'
    elif env == 'test':
        JIRA['url'] = 'http://0.0.0.0:8080'
        JIRA['token_file'] = os.environ['HOME']+'/.ssh/token-jira-8080'
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

def run_jql(jql_query):
    startAt = 0
    maxResults = 1000
    total = 0
    out_data = []
    lengths = {}
    while True:
        results_dict = fetch_query_results(startAt, maxResults, jql_query)
        
        # Print issue details from the search results
        for issue in results_dict['issues']:
            # print(f"Issue Key: {issue['key']}")
            # print(f"Summary: {issue['fields']['summary']}")
            # print(f"Status: {issue['fields']['status']['name']}")
            # print(f"Assignee: {issue['fields']['assignee']['displayName'] if issue['fields']['assignee'] else 'Unassigned'}")
            # print("------")

            issue_key = issue['key']
            issue_type = 'XXXX'
            if 'issuetype' in issue['fields']:
                issue_type = issue['fields']['issuetype']['name']
            issue_status = issue['fields']['status']['name']
            issue_summary = issue['fields']['summary']

            newdata = [issue_key, issue_type, issue_status, issue_summary]
            out_data.append(newdata)
            i = -1
            for data in newdata:
                i += 1
                if i not in lengths:
                    lengths[i] = 0
                if len(data) > lengths[i]:
                    lengths[i] = len(data)

        total = results_dict['total']
        startAt = startAt + maxResults
        if startAt >= total:
            break

    for i in lengths:
        lengths[i] += 2

    formatline = f'{{zero: <{lengths[0]}}} {{one: <{lengths[1]}}} {{two: <{lengths[2]}}} {{three}}'
    for data in out_data:
        print(formatline.format(zero=data[0], one=data[1], two=data[2], three=data[3]))


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
