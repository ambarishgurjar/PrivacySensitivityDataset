def fuse_main(args, config):
    print("Starting fuse main")
    _, events_channel = get_rabbitmq()
    api = FileAPI(
        account_id=config["accountId"],
        application_key=config["applicationKey"],
        bucket_id=config["bucketId"],
        db_file=config["sqliteFileLocation"],
    )
    cache = Cache(
        cache_folder=args.cache_folder, api=api, events_channel=events_channel
    )
    filesystem = Filesystem(cache)
    FUSE(
        filesystem,
        args.mountpoint,
        nothreads=True,
        foreground=True,
        big_writes=True,
    )


def clean_watcher(args, config):
    print("Starting cleaner")

    api = FileAPI(
        account_id=config["accountId"],
        application_key=config["applicationKey"],
        bucket_id=config["bucketId"],
        db_file=config["sqliteFileLocation"],
    )

    cleaner = Cleaner(cache_folder=args.cache_folder, api=api)
    cleaner.run_watcher()


def delete_watcher(args, config):
    print("Starting deleter")

    api = FileAPI(
        account_id=config["accountId"],
        application_key=config["applicationKey"],
        bucket_id=config["bucketId"],
        db_file=config["sqliteFileLocation"],
    )

    deleter = Deleter(api=api)
    deleter.run_watcher()


def ranker_events_watcher(args, config):
    print("Starting ranker (event watcher)")
    ranker = Ranker(
        db_file=config["sqliteFileLocation"], cache_folder=args.cache_folder
    )
    ranker.watch_events()


def ranker_scanner(args, config):
    print("Starting ranker (scanner)")
    ranker = Ranker(
        db_file=config["sqliteFileLocation"], cache_folder=args.cache_folder
    )
    ranker.scan()
