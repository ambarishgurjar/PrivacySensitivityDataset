
class LinkedIn:

    def __init__(self):
        self.s = requests.Session()
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 OPR/67.0.3575.97"
            }

    
    def login(self,email,password):
        # creates a session
        try:
            sc = self.s.get("https://www.linkedin.com/login", headers=self.headers).text
        except:
            return False
        csrfToken = sc.split('csrfToken" value="')[1].split('"')[0]
        sid = sc.split('sIdString" value="')[1].split('"')[0]
        pins = sc.split('pageInstance" value="')[1].split('"')[0]
        lcsrf = sc.split('loginCsrfParam" value="')[1].split('"')[0]
        data = {
            'csrfToken': csrfToken,
            'session_key': email,
            'ac': '2',
            'sIdString': sid,
            'parentPageKey': 'd_checkpoint_lg_consumerLogin',
            'pageInstance': pins,
            'trk': 'public_profile_nav-header-signin',
            'authUUID': '',
            'session_redirect': 'https://www.linkedin.com/feed/',
            'loginCsrfParam': lcsrf,
            'fp_data': 'default',
            '_d': 'd',
            'showGoogleOneTapLogin': 'true',
            'controlId': 'd_checkpoint_lg_consumerLogin-login_submit_button',
            'session_password': password,
            'loginFlow': 'REMEMBER_ME_OPTIN'
            }
        try:
            after_login = self.s.post("https://www.linkedin.com/checkpoint/lg/login-submit",headers=self.headers,data=data).text
        except:
            return False
        is_logged_in = after_login.split('<title>')[1].split('</title>')[0]
        if is_logged_in == "LinkedIn":
            return True
        else:
            return False

    def bulkScan(self, profiles):

        all_emails = []
        for profile in profiles:
            profile = profile + "/detail/contact-info/"
            sc = self.s.get(profile, headers=self.headers, allow_redirects=True).text
            emails_found = re.findall(r'[a-zA-Z0-9\.\-\_i]+@[\w.]+',sc)
            all_emails.extend(emails_found)
        return all_emails

    def singleScan(self, profile):

        profile = profile + "/detail/contact-info/"
        sc = self.s.get(profile, headers=self.headers, allow_redirects=True).text
        emails_found = re.findall(r'[a-zA-Z0-9\.\-\_i]+@[\w.]+',sc)
        return emails_found

    def saveRecord(self, data):
        with open('leads.csv', mode='a+', encoding='utf-8', newline='') as csvFile:
            fieldnames = ["Profile Link", "Full Name", "Headline", "Country"]
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            if os.stat('leads.csv').st_size == 0:
                writer.writeheader()
            writer.writerow({"Profile Link":data[0], "Full Name":data[1], "Headline":data[2], "Country":data[3]})

    def saveEmail(self, email):
        with open('emails.csv', mode='a+', encoding='utf-8') as emFile:
            if os.stat('emails.csv').st_size == 0:
                emFile.write("Email\n")
            emFile.write(email + "\n")



    def listProfiles(self, company_id, page_no, need_count=False):
        resp = self.s.get('https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%22{}%22%5D&origin=COMPANY_PAGE_CANNED_SEARCH&page={}'.format(company_id, page_no), headers=self.headers).text
        token = self.s.cookies.get_dict().get('JSESSIONID').replace('"','')
        headers = {
            'csrf-token': token,
            'referer': 'https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%22{}%22%5D&origin=COMPANY_PAGE_CANNED_SEARCH&page={}'.format(company_id, page_no),
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
        resp = self.s.get('https://www.linkedin.com/voyager/api/search/blended?count=10&filters=List(currentCompany-%3E{},resultType-%3EPEOPLE)&origin=COMPANY_PAGE_CANNED_SEARCH&q=all&queryContext=List(spellCorrectionEnabled-%3Etrue)&start={}'.format(company_id,(int(page_no)-1) * 10), headers=headers).json()
        profiles = resp.get('elements')[0].get('elements')
        all_profile_links = []
        if need_count:
            page_count = resp.get('paging').get('total')
        for profile in profiles:
            person_name = profile.get('title').get('text')
            profile_link = profile.get('navigationUrl')
            headline = profile.get('headline').get('text')
            country = profile.get('subline').get('text')
            print("Profile Link: {}".format(profile_link))