import requests

class Session:

    def __init__(self, username, password, base_url):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.authentication()

    def authentication(self):
        ###############################
        ### Create Session ############
        ###############################

        self.session = requests.session()

        ###############################
        ### Get Request ###############
        ###############################

        r = self.session.get(self.base_url)

        ###############################
        ### Check Cookies #############
        ###############################

        assert (len(self.session.cookies.items()) == 1)

        ###############################
        ### Get CSRF Token from Cookies
        ###############################

        csrftoken = self.session.cookies.get('XSRF-TOKEN')

        ###############################
        ### Store Token in Headers ####
        ###############################

        self.session.headers['Cookie'] = 'XSRF-TOKEN=' + csrftoken
        self.session.headers['X-XSRF-TOKEN'] = csrftoken

        ###############################
        ### Username/Password #########
        ###############################

        login_data = {'username': self.username, 'password': self.password}

        ###############################
        ### Post Request ##############
        ###############################

        r = self.session.post(self.base_url + '/api/v1/proxy/auth/token', json=login_data)

        ###############################
        ### Check Cookies #############
        ###############################

        assert (len(self.session.cookies.items()) == 2)

        ###############################
        ### Get API Token from Cookies#
        ###############################

        apitoken = self.session.cookies.get('LOGICGATE_API_QA')

        ###############################
        ### Store Token in Headers ####
        ###############################

        self.session.headers['Cookie'] = 'LOGICGATE_API_QA=' + apitoken + '; XSRF-TOKEN=' + csrftoken

        ###############################
        ### Save Status ###############
        ###############################

        self.authentication_status = r.status_code

    def account_endpoint(self):
        return self.session.get(self.base_url + '/api/v1/account/')

    def applications_endpoint(self):
        return self.session.get(self.base_url + '/api/v1/applications')
