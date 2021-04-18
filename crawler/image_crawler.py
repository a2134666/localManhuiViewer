import urllib.request
import json, time, random, os
import argparse

prefix = os.path.dirname(__file__)
prefix = os.path.join(prefix, "albums")

class AppURLopener(urllib.request.FancyURLopener):
  version = "Mozilla/5.0"
  
  def urlretrieve(self, url, filename):
    with self.open(url) as res, open(filename, "wb") as file:
      file.write(res.read())

def download_asiansister(code, length, title):
  opener = AppURLopener()
  host = "https://asiansister.com/"
  dir_path = os.path.join(prefix, title)
  if not os.path.isdir(dir_path):
    os.mkdir(dir_path)
  
  for i in range(length):
    url = "https://asiansister.com/viewImg.php?code={}&id={}".format(code, str(i))
    with opener.open(url) as res:
      res_lines = res.read().decode("utf-8").split("\n")
      for line in res_lines:
        if('document.getElementById("img01").src' in line):
          line_array = line.split("\"")
          if len(line_array) >= 4:
            _, ext = line_array[3].split(".")
            filename = os.path.join(dir_path, "{}_{}.{}".format(code, i, ext))
            opener.urlretrieve(os.path.join(host,line_array[3]), filename)
            print(filename, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
          
    random_sleep = random.random() * 2
    time.sleep(random_sleep)
  
def download_xiannvtu(code, length, title):
  opener = AppURLopener()
  dir_path = os.path.join(prefix, title)
  if not os.path.isdir(dir_path):
    os.mkdir(dir_path)
  
  for i in range(length):
    url = "https://img.jinghaihuishou.com/img/{}/{:0>2d}.jpg".format(code, i+1)
    ext = url.split(".")
    filename = os.path.join(dir_path, "{}_{:0>2d}.{}".format(code, i+1, ext[-1]))
    opener.urlretrieve(url, filename)
    print(filename, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
          
    random_sleep = random.random() * 2
    time.sleep(random_sleep)
  
def download_tujigu(code, length, title):
  opener = AppURLopener()
  dir_path = os.path.join(prefix, title)
  if not os.path.isdir(dir_path):
    os.mkdir(dir_path)
  
  for i in range(length):
    url = "https://tjg.hywly.com/a/1/{}/{}.jpg".format(code, i+1)
    ext = url.split(".")
    filename = os.path.join(dir_path, "{}_{:0>2d}.{}".format(code, i+1, ext[-1]))
    opener.urlretrieve(url, filename)
    print(filename, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
          
    random_sleep = random.random() * 2
    time.sleep(random_sleep)
      
  
def is_integer(n):
  try:
    float(n)
  except ValueError:
    return False
  else:
    return float(n).is_integer()
  

support_sites = {"asiansister":download_asiansister, "xiannvtu":download_xiannvtu, "tujigu":download_tujigu}
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
  
  # required argement
  parser = argparse.ArgumentParser("image_crawler")
  parser.add_argument("resource", help="The file in csv format. Each line contains the title, code, and number of pictures.")
  parser.add_argument("site", help="Support sites: " + ", ".join(support_sites.keys()))
  args = parser.parse_args()
  
  titles = []
  codes = []
  length = []
  
  try:
    # check site of image source
    if args.site in support_sites.keys():
      print("Image source: " + args.site)
      download = support_sites[args.site]
    else:
      # array index
      if is_integer(args.site) and int(args.site) < len(support_sites):
        print("Image source: " + list(support_sites)[int(args.site)])
        download = list(support_sites.values())[int(args.site)]
      else:
        print("Unsupport image source: " + args.site)
        exit()
    #print(download.__name__)
    
    with open(args.resource, "r", encoding="utf-8") as f:
      print("Start to read album entries......")
      lines = f.readlines()
      for i,line in enumerate(lines):
        entry = line.rstrip().split(",")
        
        if not len(entry) == 3:
          print("Unavaliable format: " + line)
          continue
        if not is_integer(entry[2]):
          print("Unavaliable length: " + entry[2])
          continue
        
        entry[0] = os.path.normpath(entry[0])
        entry[2] = int(entry[2])
        print("Entry {}: title= {}, code= {}, length= {}".format(i+1, *entry))
        
        titles.append(entry[0])
        codes.append(entry[1])
        length.append(entry[2])
          
  except FileNotFoundError:
    print("檔案不存在")
  except IsADirectoryError:
    print("該路徑為目錄")
  
  # start to download images
  for i in range(len(titles)):
    download(codes[i], length[i], titles[i]);
  
  
