import os
import re

reload(sys)
sys.setdefaultencoding('utf8')

class LinkedinProfiles():
    def __init__(self, company):
        self.base_url = "https://www.linkedin.com"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.employees = []
        self.company = company
        self.scompany = company.replace(" ", "_")
        if not os.path.isdir(self.scompany):
            os.mkdir(self.scompany)

    def init_driver(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.username = raw_input('linkedin username:')
        self.password = raw_input('linkedin password:')


    # specified in the company variable
    def get_linkedin_profiles(self):
        self.init_driver()
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("login-email").clear()
        driver.find_element_by_id("login-email").send_keys(self.username)
        driver.find_element_by_id("login-password").clear()
        driver.find_element_by_id("login-password").send_keys(self.password)
        driver.find_element_by_id("login-submit").click()

        # driver.find_element_by_name("submit").click()
        driver.find_element_by_id("main-search-box").clear()
        driver.find_element_by_id("main-search-box").send_keys(self.company)
        # Create the search URL
        search = "https://www.linkedin.com/ta/federator"
        params = {'orig': 'GLHD',
                  'verticalSelector': 'all',
                  'query': self.company}
        # search = "https://www.linkedin.com/ta/federator?orig=GLHD&verticalSelector=all&query={}&tracking=true&refTarId=1468332198550"
        search_url = "{}?{}".format(search, urlencode(params))
        driver.get(search_url)
        # Parse the results from our search
        soup = BeautifulSoup(driver.page_source)
        j = json.loads(soup.find("pre").text)

        for item in j['resultList']:
            # Select the first company in the results list
            if item['sourceID'] == 'company':
                comp_id = item['id']
                break
        if comp_id:
            # Create the URL for getting the company's employee page
            employees_page = "https://www.linkedin.com/vsearch/p?f_CC={}&trk=rr_connectedness".format(comp_id)
        else:
            print "Couldn't find a company link with that name! Quitting..."
            quit()
        driver.get(employees_page)
        # driver.find_element_by_xpath('//*[@id="results"]/li[1]/div/h3/a').click()
        # driver.find_element_by_link_text("See all").click()
        previous = ""
        for i in range(0, 99):
            sleep(5)
            f = open("{}/{}{}_source.html".format(self.scompany, self.scompany, i), 'wb')
            source = driver.page_source

            if previous == source:
                break
            previous = source
            encoded = source.encode('utf-8').strip()
            f.write(source)
            f.close()
            # self.parse_source(source)
            # TODO: if there is no "Next" button, end the loop
            try:
                driver.find_element_by_link_text("Next >").click()
            except Exception, e:
                # traceback.print_exc(e)
                print "Pulled {} pages".format(i+1)
                break
        # driver.find_element_by_link_text("Next >").click()
        # driver.find_element_by_link_text("Next >").click()

class ParseProfiles():
    def __init__(self, suffix, prefix, ignore, company):
        self.employees = []
        self.prefix = prefix
        self.suffix = suffix
        self.ignore = ignore
        self.company = company.replace(" ", "_")

    def parse_source(self, path):
        try: