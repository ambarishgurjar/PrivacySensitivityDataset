# Add missing param
try:
    vars(args)["action"] = sys.argv[1]
except IndexError as e:
    logger.error("Please, add an option to execute")
    parser.print_help()
    sys.exit()

if args.action == "scrape":
    if args.proxies:
        set_proxy_list()
    start_scrapping(args.email, args.quiet)

elif args.action == "generate":
    if not re.match("^[0-9X]{10}", args.mask):
        logger.error(
            "%sYou need to pass a US phone number masked as in: 555XXX1234", RED, ENDC)
        exit()
    if args.proxies:
        set_proxy_list()
    possible_phone_number = get_possible_phone_numbers(args.mask)
    if args.file:
        with open(args.file, 'w') as f:
            f.write('\n'.join(possible_phone_number))
        logger.info("%sDictionary created successfully at %s %s",
                    GREEN, os.path.realpath(f.name), ENDC)
        f.close()
    else:
        logger.info("%sThere are %s possible numbers %s", GREEN,
                    str(len(possible_phone_number)), ENDC)
        logger.info("%s %s %s", GREEN, str(possible_phone_number), ENDC)

elif args.action == "bruteforce":
    if args.email and not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", args.email):
        logger.error("%sEmail is invalid", RED, ENDC)
        exit()
    if (args.mask and args.file) or (not args.mask and not args.file):
        logger.error(
            "%sYou need to provide a masked number or a file with numbers to try %s", RED, ENDC)
        exit()
    if args.mask and not re.match("^[0-9X]{10}", args.mask):
        logger.error(
            "%sYou need to pass a 10-digit US phone number masked as in: 555XXX1234 %s", RED, ENDC)
        exit()
    if args.file and not os.path.isfile(args.file):
        logger.error("%sYou need to pass a valid file path %s", RED, ENDC)
        exit()

    logger.info("Looking for the phone number associated to %s ...", args.email)
    if args.mask:
        possiblePhoneNumbers = get_possible_phone_numbers(args.mask)
    else:
        f = open(args.file, "r")
        if not f.mode == 'r':
            f.close()
            logger.error("%sCould not read file %s %s", RED, args.file, ENDC)
            exit()
        file_content = f.read()
        file_content = filter(None, file_content)  # Remove last \n if needed
        possiblePhoneNumbers = file_content.split("\n")
        f.close()
    if args.proxies:
        set_proxy_list()
    start_brute_force(possiblePhoneNumbers, args.email,
                      args.quiet, args.verbose)
else:
    logger.error("%sAction not recognized", RED, ENDC)
    exit()
