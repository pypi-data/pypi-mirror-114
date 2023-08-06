import requests,time
from .agents import getagent
import concurrent.futures
import asyncio
from multiprocessing import Process
from .extractdata import extractinfo,cleantag

class jsreqc:
  def __init__(self,txt,st=200):
    self.text = txt
    self.status_code = st

def load_url(url, pluck):
     resp = requests.get(url,headers=getagent(),timeout=pluck.timeout)
     if pluck.verbose:print(f"Request Status {resp.status_code} :- {url}")
     return resp

def jsreq(csstag,pluck,typ):
  out = {} if pluck.organised else []
  time1 = time.time()
  for url in pluck.urls:
    time.sleep(pluck.sleep)
    data=jsreqc(asyncio.get_event_loop().run_until_complete(pluck.engine.goto(url)))
    try:
       if pluck.organised:out[url] = extractinfo(csstag,data,typ)
       else:out.append(extractinfo(csstag,data,typ))
    except Exception as exc:
       if pluck.verbose:print(str(type(exc)))
    if pluck.database:
          pluck.db.write('data','datafile',{'data':cleantag(out,pluck)})
  time2 = time.time()
  if pluck.verbose:print(f'Took {time2-time1:.2f} s')
  return cleantag(out)

def req(csstag,pluck,typ):
  out = {} if pluck.organised else []
  with concurrent.futures.ThreadPoolExecutor(max_workers=pluck.requests) as executor:
    future_to_url = (executor.submit(load_url, url, pluck) for url in pluck.urls)
    time1 = time.time()
    tls = 0
    for future in concurrent.futures.as_completed(future_to_url):
        if tls == pluck.requests:time.sleep(pluck.sleep);tls=0
        try:
            data = future.result()
            if data.status_code == 200:
             if pluck.organised:out[data.url] = extractinfo(csstag,data,typ)
             else:out.append(extractinfo(csstag,data,typ))
        except Exception as exc:
            if pluck.verbose:print(str(type(exc)))
        tls+=1
        if pluck.database:
          pluck.db.write('data','datafile',{'data':cleantag(out,pluck)})
    time2 = time.time()
  if pluck.verbose:print(f'Took {time2-time1:.2f} s')
  return cleantag(out)