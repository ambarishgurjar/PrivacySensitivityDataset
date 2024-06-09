    def every_day_tasks(self):
        if int(self.elapsed_time/3600. % 24.) == 23:

            if self.twentyfour_hour_trigger:
                if hasattr(self,'driver'):
                    self.seed_links()
                    # restart the driver
                    self.quit_driver()
                    self.open_driver()
                else:
                    self.open_driver()
                    self.decimate_links(total_frac=0.667, decimate_frac=0.1)
                    self.seed_links()
                    if self.quit_driver_every_call: self.quit_driver()
                self.twentyfour_hour_trigger = False
        else:
            self.twentyfour_hour_trigger = True

    def every_two_weeks_tasks(self):
        if self.elapsed_time > 3600.*24*14:

            self.start_time = time.time()
            self.data_usage = 0
            self.decimate_links(total_frac=0.49, decimate_frac=0.333)
            self.get_blacklist(update_flag=True)  # reload the latest blacklists

    def decimate_links(self, total_frac=0.81, decimate_frac=0.1, log_sampling=False):

        if self.link_count() > int(np.ceil(total_frac * self.max_links_cached)):
            for url in self.draw_links(n=int(np.ceil(self.link_count()*decimate_frac)),log_sampling=log_sampling):
                self.remove_link(url)

    def set_user_agent(self):
        self.draw_user_agent()

        self.open_driver()

    def draw_user_agent(self,max_draws=10000):

        global ua_parse_flag, user_agent
        if not ua_parse_flag:
            self.user_agent = self.fake_ua.random if npr.random() < 0.95 else user_agent
            return

        property_pvals = self.property_pvals
        k = 0
        while k < max_draws:
            uap = ua.parse(self.fake_ua.random)

            p_browser = property_pvals['browser']['noneoftheabove']
            for ky in property_pvals['browser']:
                if bool(re.findall(ky, uap.browser.family, flags=re.IGNORECASE)):
                    p_browser = property_pvals['browser'][ky]
                    break
            p_os = property_pvals['os']['noneoftheabove']
            for ky in property_pvals['os']:
                if bool(re.findall(ky, uap.os.family, flags=re.IGNORECASE)):
                    p_os = property_pvals['os'][ky]
                    break
            p_pc = property_pvals['is_pc'][uap.is_pc]
            p_touch_capable = property_pvals['is_touch_capable'][uap.is_touch_capable]
            if npr.uniform() <= p_browser \
                    and npr.uniform() <= p_os \
                    and npr.uniform() <= p_pc \
                    and npr.uniform() <= p_touch_capable: break
            k += 1
        self.user_agent = uap.ua_string

    def draw_link(self,log_sampling=True):

        return self.draw_links(n=1,log_sampling=log_sampling)[0]

    def draw_links(self,n=1,log_sampling=False):

        urls = []
        domain_array = np.array([dmn for dmn in self.domain_links])
        domain_count = np.array([len(self.domain_links[domain_array[k]]) for k in range(domain_array.shape[0])])
        p = np.array([np.float(c) for c in domain_count])
        count_total = p.sum()
        if log_sampling:  
            p = np.fromiter((np.log1p(x) for x in p), dtype=p.dtype)
        if count_total > 0:
            p = p/p.sum()
            cnts = npr.multinomial(n, pvals=p)
            if n > 1:
                for k in range(cnts.shape[0]):
                    domain = domain_array[k]
                    cnt = min(cnts[k],domain_count[k])
                    for url in random.sample(self.domain_links[domain],cnt):
                        urls.append(url)
            else:
                k = int(np.nonzero(cnts)[0])
                domain = domain_array[k]
                url = random.sample(self.domain_links[domain],1)[0]
                urls.append(url)
        return urls

    def draw_domain(self,log_sampling=False):
