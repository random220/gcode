#!/usr/bin/env python3
import requests
import os, sys
import shutil
import json
import re

confroot          = os.environ['HOME']+'/.jira'
default_conf_file = confroot + '/conf'
saved_env_confs   = confroot + '/confs'
qdir              = confroot + '/queries'
os.makedirs(saved_env_confs, exist_ok = True)
os.makedirs(qdir, exist_ok = True)

JIRA = {
    'url' : None,
    'token_file' : None,
    'token' : None,
}

def main():
    os.umask(0o077)
    #issue_key = 'SPARTA-18102'
    #print_issue(issue_key)

    if len(sys.argv) == 1:
        print_help()
        sys.exit(0)

    if sys.argv[1] == 'env':
        do_env_setup()
        sys.exit(0)

    readenv()
    if JIRA['url'] is None:
        make_new_env(None)

    if sys.argv[1] == 'q':
        do_query()
        sys.exit(0)
    elif sys.argv[1] == 'cm':
        do_comment()
        sys.exit(0)


def print_help():
    print("""
# j env                   # List known envs
# j env .                 # Show current default env
# j env +                 # Create a new env. Ask for name
# j env +apple            # Create a new named env
# j env + pear            # Create a new named env
# j env mango             # Use a named env
# j env /some/path/mango  # Use a named env from path
# j q                     # list saved queries
# j q <query name>        # Execute named query
# j q last                # Execute last query
# j q q:<'QUERY TEXT'>    #
# j cm|com issue          # add comment
# ---
# j c irp2323             # create issue with label "manual-rehab"
# j l                     # list open issues with label "manual-rehab"
# j a issue who           # assign
# j cl issue              # close
# j lb issue label        # add label
"""
    )


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
    # j q                     # list saved queries
    if sys.argv[1] == 'q' and len(sys.argv) == 2:
        os.system(f'find "{qdir}"/*')
        sys.exit(0)

    # j q <query name>        # Execute named query
    # j q last                # Execute last query
    # j q q:<'QUERY TEXT'>    #
    elif sys.argv[1] == 'q' and len(sys.argv) == 3:
        m = re.search(r'^q:(.+)', sys.argv[2])
        if m:
            jql = normalize_query(m.group(1))
        else:
            qname = sys.argv[2]
            qfile = qname
            if not os.path.isfile(qfile):
                qfile = f'{qdir}/{qname}'
            if not os.path.isfile(qfile):
                print(f'File not found {qfile}')
                sys.exit(1)
            f = open(qfile, 'r')
            jql = normalize_query(f.read())
            f.close()
        
        last_query_file = f'{qdir}/last'
        f = open(last_query_file, 'w')
        f.write(jql)
        f.write('\n')
        f.close()
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

def make_new_env(envname):
    JIRA['token_file'] = None
    print('URL: something like https://production.jira.site.com')
    JIRA['url'] = input().strip()
    print('Jira token:')
    JIRA['token'] = input().strip()
    writeenv(envname)

def writeenv(envname):
    os.makedirs(confroot, exist_ok = True)
    if envname is None:
        conf_file = default_conf_file
    else:
        conf_file = f'{saved_env_confs}/{envname}'
    f = open(conf_file, 'w')
    f.write(json.dumps(JIRA, indent=4, sort_keys=True))
    f.write('\n')
    
def readenv():
    os.makedirs(os.path.dirname(default_conf_file), exist_ok = True)
    if os.path.isfile(default_conf_file):
        f = open(default_conf_file, 'r')
        j = json.load(f)
        f.close()

        for key in j:
            JIRA[key] = j[key]

def do_env_setup():
    # j env  # List saved envs
    if len(sys.argv) == 2:
        os.system(f'find "{saved_env_confs}"/*')
        sys.exit(0)
    elif len(sys.argv) >= 3:
        # j env +
        # j env +apple
        # j env + pear
        envname = ''
        if sys.argv[2] == '.':
            os.system(f'cat {default_conf_file}')
            sys.exit(0)

        if sys.argv[2] == '+':
            if len(sys.argv) == 4:
                envname = sys.argv[3]           # j env + pear
            else:                               # j env +
                print("New env name?")
                envname = input().strip()
            make_new_env(envname)
            return

        m = re.search(r'^\+(.*)', sys.argv[2])  # j env +apple
        if m:
            envname = m.group(1)
            if envname == '':
                print('This should not happen !!!')
                print(sys.argv)
                sys.exit(1)
            make_new_env(envname)
            return

        # j env mango
        # j env /some/path/mango
        saved_conf_file = sys.argv[2]
        if not os.path.isfile(saved_conf_file):
            saved_conf_file = f'{saved_env_confs}/{sys.argv[2]}'
        if not os.path.isfile(saved_conf_file):
            print('Conf file not found')
            sys.exit(1)

        shutil.copy2(saved_conf_file, default_conf_file)
        readenv()
        sys.exit(0)


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
    newdata = ['Updated', 'Created', 'Issue', 'Type', 'Status', 'Summary']
    out_data.append(newdata)
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

            _key = issue['key']
            _type = 'XXXX'
            if 'issuetype' in issue['fields']:
                _type = issue['fields']['issuetype']['name']
            _status = issue['fields']['status']['name']
            _summary = issue['fields']['summary']
            _created = issue['fields']['created']
            _created = re.sub(r'T.*', '', _created)
            _updated = issue['fields']['updated']
            _updated = re.sub(r'T.*', '', _updated)

            newdata = [_updated, _created, _key, _type, _status, _summary]
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

    if len(lengths) == 0:
        return

    # Add two more spaces to the right over the max width of fields
    for i in lengths:
        lengths[i] += 2

    formatline = f'{{zero: <{lengths[0]}}} {{one: <{lengths[1]}}} {{two: <{lengths[2]}}} {{three: <{lengths[3]}}} {{four: <{lengths[4]}}} {{five}}'
    for data in out_data:
        print(formatline.format(zero=data[0], one=data[1], two=data[2], three=data[3], four=data[4], five=data[5]))


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
        'fields': ['summary', 'status', 'assignee', 'issuetype', 'created', 'updated']  # Specify the fields you want to retrieve
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
