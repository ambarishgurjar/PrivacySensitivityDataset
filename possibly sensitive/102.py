        self.prefix = prefix
        self.suffix = suffix
        self.ignore = ignore
        self.company = company.replace(" ", "_")

    def parse_source(self, path):
        try:
            source = open(path)
            soup = BeautifulSoup(source, 'html.parser')
            results = soup.find(id='results')
            links = results.find_all("li", {"class": "mod"})
            for person in links:
                link = person.find('a', {"class": "result-image"})
                ind = {'name': "Not Found",
                       'picture': "Not Found",
                       'email': "Not Found",
                       'job': "Not Found"}
                if link:
                    # img = link.img
                    img = link
                if img:
                    # ind['picture'] = img.get('src')
                    ind['picture'] = img
                name = person.find('a', {"class": "title main-headline"})
                if name:
                    ind['name'] = name.text
                job = person.find('p', {"class": "title"})
                if not job:
                    job = person.find('div', {"class": "description"})
                if job:
                    ind['job'] = job.text
                # print ind['name']
                self.employees.append(ind)
        except Exception, e:
            print "Encountered error parsing file: {}".format(path)
            traceback.print_exc(e)

    def print_employees(self):
        # pprint(self.employees)
        body = ""
        csv = []
        header = "<table>" \
                 "<thead>" \
                 "<tr>" \
                 "<td>Picture</td>" \
                 "<td>Name</td>" \
                 "<td>Possible Email:</td>" \
                 "<td>Job</td>" \
                 "</tr>" \
                 "</thead>"
        for emp in self.employees:
            if ',' in emp['name']:
                print "user's name contains a comma, might not display properly: {}".format(emp['name'])
            name = emp['name'].split(',')[0]
            emp['name'] = name

            parts = name.split()
            if emp['name'] != 'LinkedIn Member':
                if len(parts) == 2:
                    fname = parts[0]
                    mname = '?'
                    lname = parts[1]
                elif len(parts) == 3:
                    fname = parts[0]
                    mname = parts[1]
                    lname = parts[2]
                fname = re.sub('[^A-Za-z]+', '', fname)
                mname = re.sub('[^A-Za-z]+', '', mname)
                lname = re.sub('[^A-Za-z]+', '', lname)
                if self.prefix == 'full':
                    user = '{}{}{}'.format(fname, mname, lname)
                if self.prefix == 'firstlast':
                    user = '{}{}'.format(fname, lname)
                if self.prefix == 'firstmlast':
                    user = '{}{}{}'.format(fname, mname[0], lname)
                if self.prefix == 'flast':
                    user = '{}{}'.format(fname[0], lname)
                if self.prefix == 'first.last':
                    user = '{}.{}'.format(fname, lname)
                if self.prefix == 'fmlast':
                    user = '{}{}{}'.format(fname[0], mname[0], lname)

                emp['email'] = '{}@{}'.format(user, self.suffix)

            if not self.ignore or (self.ignore and emp['name'] != 'LinkedIn Member'):
                body += "<tr>" \
                        "<td>{picture}</td>" \
                        "<td>{name}</td>" \
                        "<td>{email}</td>" \
                        "<td>{job}</td>" \
                        "<td>".format(**emp)
                csv.append('{name},{email},"{job}"'.format(**emp))
            else:
                print "ignoring user: {} - {}".format(emp['name'], emp['job'])
        foot = "</table>"
        f = open('{}/employees.html'.format(self.company), 'wb')
        f.write(header)
        f.write(body)
        f.write(foot)