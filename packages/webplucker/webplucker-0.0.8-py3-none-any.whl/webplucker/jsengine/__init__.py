from pyppeteer import launch
from pyppeteer.network_manager import NetworkManager

class engine():
 def __init__(self):
     pass

 def logit(self,event):
    req = event._request
    print("{0} - {1}".format(req.url, event._status))

 async def start(self):
     self.browser = await launch({'headless': False})
     self.page = await self.browser.newPage()
     self.page._networkManager.on(NetworkManager.Events.Response, self.logit)
 
 async def goto(self,url):
  await self.page.goto(url)
  #await print(dir(self.page))
  return await self.page.content()

 async def close(self):
  await self.browser.close()