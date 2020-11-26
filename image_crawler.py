import urllib.request
import json, time, random, os

class AppURLopener(urllib.request.FancyURLopener):
  version = "Mozilla/5.0"
  
  def urlretrieve(self, url, filename):
    with self.open(url) as res, open(filename, "wb") as file:
      file.write(res.read())

def download_asiansister(code, length, title):
  opener = AppURLopener()
  host = "https://asiansister.com/"
  if not os.path.isdir(title):
    os.mkdir(title)
  
  for i in range(length):
    url = "https://asiansister.com/viewImg.php?code={}&id={}".format(code, str(i))
    with opener.open(url) as res:
      res_lines = res.read().decode("utf-8").split("\n")
      for line in res_lines:
        if('document.getElementById("img01").src' in line):
          line_array = line.split("\"")
          if len(line_array) >= 4:
            _, ext = line_array[3].split(".")
            filename = os.path.join(title,"{}_{}.{}".format(code, i, ext))
            opener.urlretrieve(os.path.join(host,line_array[3]), filename)
            print(filename, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
          
    random_sleep = random.randint(0,2)
    time.sleep(random_sleep)
  
def download_xiannvtu(code, length, title):
  opener = AppURLopener()
  if not os.path.isdir(title):
    os.mkdir(title)
  
  for i in range(length):
    url = "https://img.jinghaihuishou.com/img/{}/{:0>2d}.jpg".format(code, i+1)
    ext = url.split(".")
    filename = os.path.join(title,"{}_{:0>2d}.{}".format(code, i+1, ext[-1]))
    opener.urlretrieve(url, filename)
    print(filename, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
          
    random_sleep = random.randint(0,2)
    time.sleep(random_sleep)
  
def download_tujigu(code, length, title):
  opener = AppURLopener()
  if not os.path.isdir(title):
    os.mkdir(title)
  
  for i in range(length):
    url = "https://tjg.hywly.com/a/1/{}/{}.jpg".format(code, i+1)
    ext = url.split(".")
    filename = os.path.join(title,"{}_{:0>2d}.{}".format(code, i+1, ext[-1]))
    opener.urlretrieve(url, filename)
    print(filename, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
          
    random_sleep = random.randint(0,2)
    time.sleep(random_sleep)
  
if __name__ == "__main__":
  # headers = {"Host": "asiansister.com",
             # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0",
             # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
             # "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3",
             # "Accept-Encoding": "gzip, deflate, br",
             # "Referer": "https://asiansister.com/search.php?q=%E7%B1%B3%E7%B7%9A%E7%B7%9A&page=1",
             # "DNT": "1",
             # "Connection": "keep-alive",
             # "Cookie": "__cfduid=dbf42ef249f060b18ce3245d9286cd97b1604593106; PHPSESSID=60248206bc047607e3eb4ac900f03cf2; view_i=1975%2F1882",
             # "Upgrade-Insecure-Requests": "1",
             # "Cache-Control": "max-age=0",
             # "TE": "Trailers"}
  # headers = bytes(json.dumps(headers), encoding="utf-8")
  # req = urllib.request.Request(url, headers)
  # res = urllib.request.urlopen(req)
  
  titles = []
  codes = []
  length = []
  
  download_tujigu(codes[0], length[0], titles[0]);
  
  
