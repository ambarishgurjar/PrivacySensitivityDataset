
m3u8InputFilePath = "D:/input/m3u8_input.txt"

saveRootDirPath = "D:/output"

errorM3u8InfoDirPath = "D:/output/error.txt"

m3u8TryCountConf = 10

processCountConf = 50



taskThreadPool = None

m3u8Url = None

rootUrlPath = None

title = None

sumCount = 0

doneCount = 0

cachePath = saveRootDirPath + "/cache"

logPath = cachePath + "/log.log"

logFile = None

downloadedBytes = 0

downloadSpeed = 0


def getM3u8Info():
    global m3u8Url
    global logFile
    global rootUrlPath
    tryCount = m3u8TryCountConf
    while True:
        if tryCount < 0:
            print("\t{0}下载失败！".format(m3u8Url))
            logFile.write("\t{0}下载失败！".format(m3u8Url))
            return None
        tryCount = tryCount - 1
        try:
            response = requests.get(m3u8Url, headers=headers, timeout=20)
            if response.status_code == 301:
                nowM3u8Url = response.headers["location"]
                print("\t{0}重定向至{1}！".format(m3u8Url, nowM3u8Url))
                logFile.write("\t{0}重定向至{1}！\n".format(m3u8Url, nowM3u8Url))
                m3u8Url = nowM3u8Url
                rootUrlPath = m3u8Url[0:m3u8Url.rindex('/')]
                continue

            contentLength = response.headers.get('Content-Length')
            if contentLength:
                expected_length = int(contentLength)
                actual_length = len(response.content)
                if expected_length > actual_length:
                    raise Exception("m3u8下载不完整")

            print("\t{0}下载成功！".format(m3u8Url))
            logFile.write("\t{0}下载成功！".format(m3u8Url))
            rootUrlPath = m3u8Url[0:m3u8Url.rindex('/')]
            break
        except:
            print("\t{0}下载失败！正在重试".format(m3u8Url))
            logFile.write("\t{0}下载失败！正在重试".format(m3u8Url))

    m3u8Info = m3u8.loads(response.text)

    if m3u8Info.is_variant:
        print("\t{0}为多级码流！".format(m3u8Url))
        logFile.write("\t{0}为多级码流！".format(m3u8Url))
        for rowData in response.text.split('\n'):

            if rowData.endswith(".m3u8"):
                scheme = urlparse(m3u8Url).scheme
                netloc = urlparse(m3u8Url).netloc
                m3u8Url = scheme + "://" + netloc + rowData
                rootUrlPath = m3u8Url[0:m3u8Url.rindex('/')]

                return getM3u8Info()

        print("\t{0}响应未寻找到m3u8！".format(response.text))
        logFile.write("\t{0}响应未寻找到m3u8！".format(response.text))
        return None
    else:
        return m3u8Info


def getKey(keyUrl):
    global logFile
    tryCount = m3u8TryCountConf
    while True: