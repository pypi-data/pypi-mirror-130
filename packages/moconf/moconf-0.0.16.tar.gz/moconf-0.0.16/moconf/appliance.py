import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class morphAppliance(object):
    def __init__(self, app_name, app_hostname, account_name, user_name, password, email, first_name, access_token, license_key):
        self.app_name = app_name
        self.app_hostname = app_hostname
        self.account_name = account_name
        self.user_name = user_name
        self.password = password
        self.email = email
        self.first_name = first_name
        self.access_token = access_token
        self.licence_key = license_key
    
    def applianceSetup(self):
        url = str("https://%s" % (self.app_hostname))
        setup_url = str("https://%s/api/setup/init" % (self.app_hostname))
        headers={'Content-Type': 'application/json',"Accept":"application/json"}
        body={ "applianceName": self.app_name, "applianceUrl": url, "accountName": self.account_name, "username": self.user_name, "password": self.password, "email": self.email, "firstName": self.first_name }
        b = json.dumps(body)
        response = requests.post(setup_url, headers=headers, data=b, verify=False)
        data = response.json()
        print(data)   
    
    def getApiToken(self):
        url = str("https://%s/oauth/token?grant_type=password&scope=write&client_id=morph-api" % (self.app_hostname))
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        body = {"username": self.user_name, "password": self.password}
        response = requests.post(url, headers=headers, data=body, verify=False)
        data = response.json()
        return data['access_token']
        
    def applyLicense(self):
        url = str("https://%s/api/license" % (self.app_hostname))
        headers={'Content-Type': 'application/json',"Authorization": "BEARER " + (self.access_token)}
        body = {"license": self.licence_key}
        b = json.dumps(body)
        response = requests.post(url, headers=headers, data=b, verify=False)
        data = response.json()
        
    def checkAppliancePing(self):
        reply = ""
        url = str("https://%s/ping" % (self.app_hostname))
        headers={'Content-Type': 'application/json',"Accept":"application/json"}
        try:
            response = requests.get(url, headers=headers, verify=False)
            reply = response.text
        except:
            pass
        return reply
    
    def checkApplianceSetupStatus(self):
        url = str("https://%s/api/ping" % (self.app_hostname))
        headers={'Content-Type': 'application/json',"Accept":"application/json"}
        response = requests.get(url, headers=headers, verify=False)
        data = response.json()
        return data["setupNeeded"]