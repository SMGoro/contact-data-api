# -*- coding: UTF-8 -*-
import requests
import re
import json
from http.server import BaseHTTPRequestHandler
from bs4 import BeautifulSoup

def github_json(user,repo,branch,groups):
    if user =='':
        user = 'smgoro'
        # result = 'The user cannot be none!'
    else:
        try:
            if repo =='':
                repo = 'contact-data'
            if branch =='':
                branch = 'output'
            if groups =='':
                groups = 'friends'
            # requests_path = 'https://github.com/' + user + '/' +repo + '/blob/' +branch + '/v2/' +groups+'.json'
            requests_path = 'https://github.com/SMGoro/contact-data/blob/output/v2/friends.json'
            r = requests.get(requests_path)
            r.encoding = 'utf-8'
            gitpage = r.text
            soup = BeautifulSoup(gitpage, 'html.parser')
            main_content = soup.find('td',id = 'LC1').text
            result = json.loads(main_content)
        except:
            result = 'Incorrect user parameter!Please check!'
    return result

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        path = path.replace("'", '"')
        repo_reg = re.compile(r'repo="(.*?)"')
        user_reg = re.compile(r'user="(.*?)"')
        branch_reg = re.compile(r'branch="(.*?)"')
        groups_reg = re.compile(r'groups="(.*?)"')
        if user_reg.findall(path):
            user = user_reg.findall(path)[0]
        else:
            user = 'smgoro'
        if repo_reg.findall(path):
            repo = repo_reg.findall(path)[0]
        else:
            repo = 'contact-data'
        if branch_reg.findall(path):
            branch = branch_reg.findall(path)[0]
        else:
            branch = 'output'
        if groups_reg.findall(path):
            groups = groups_reg.findall(path)[0]
        else:
            groups = 'friends'
        data = github_json(user,repo,branch,groups)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
        return
