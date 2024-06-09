    assert_bookmarks_equal(
        bmk[0],
        (
            datetime.datetime(
                2021,
                2,
                9,
                9,
                37,
                32,
                tzinfo=datetime.timezone(datetime.timedelta(seconds=19800), "IST"),
            ),
            "https://github.com/pesos/browser-history",
            "Browser-history",
            "bookmark_bar/github",
        ),
    )
    h_profs = f.profiles(f.history_file)
    b_profs = f.profiles(f.bookmarks_file)
    his_path = f.history_path_profile(h_profs[0])
    bmk_path = f.bookmarks_path_profile(b_profs[0])
    assert his_path in [
        Path.home() / ".config/chromium/Default/History",
        Path.home() / ".config/chromium/Profile/History",
    ]
    assert bmk_path in [
        Path.home() / ".config/chromium/Default/Bookmarks",
        Path.home() / ".config/chromium/Profile/Bookmarks",
    ]
    his = f.history_profiles(h_profs).histories
    assert len(his) == 2
    assert_histories_equal(
        his[0],
        (
            datetime.datetime(
                2020,
                10,
                15,
                15,
                34,
                30,
                tzinfo=datetime.timezone(datetime.timedelta(seconds=7200), "CEST"),
            ),
            "www.github.com",
        ),
    )


def test_firefox_windows(become_windows, change_homedir):  
    f = browser_history.browsers.Firefox()
    h_output = f.fetch_history()
    b_output = f.fetch_bookmarks()
    his = h_output.histories
    bmk = b_output.bookmarks
    assert len(his) == 8
    assert len(bmk) == 14
    profs = f.profiles(f.history_file)
    assert len(profs) == 2

    assert_histories_equal(
        his[0],
        (
            datetime.datetime(
                2020,
                10,
                1,
                11,
                43,
                35,
                tzinfo=datetime.timezone(
                    datetime.timedelta(seconds=10800), "E. Africa Standard Time"
                ),
            ),
            "https://www.youtube.com/",
        ),
    )
    assert_bookmarks_equal(
        bmk[0],
        (
            datetime.datetime(
                2018,
                12,
                8,
                0,
                33,
                27,
                tzinfo=datetime.timezone(datetime.timedelta(seconds=19800), "IST"),
            ),
            "http://dl.dlb3d.xyz/S/",
            "Index of /S/",
            "unfiled",
        ),
    )
    assert_histories_equal(
        his[-1],
        (
            datetime.datetime(
                2020,
                10,