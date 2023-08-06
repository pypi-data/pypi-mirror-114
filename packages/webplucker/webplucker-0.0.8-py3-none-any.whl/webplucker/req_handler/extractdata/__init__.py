from lxml.cssselect import CSSSelector
from lxml.html import fromstring
from cssselect import GenericTranslator, SelectorError
from .config import e_symbol
from lxml.etree import tostring

def cleantag(data,pluck=''):
   if isinstance(data,list):
      if pluck != '' and not pluck.duplicate:data = list(tuple(data))
      if len(data)==1:return data[0]
      else:return data
   return data

def extractxpath(xpath,req):
 output,tag,get = {},'',False
 if isinstance(xpath,dict):
  for x in xpath:
   if e_symbol in xpath[x]:get,tag=xpath[x].split(e_symbol)[-1],xpath[x].split(e_symbol)[0]
   try:
    if get:
      if get=='html':output[x] = tostring(fromstring(req.text).xpath(tag)[0]).decode("utf-8")
      else:output[x] = fromstring(req.text).xpath(tag)[0].text_content() if get=='text' else fromstring(req.text).xpath(tag)[0].get(get)
    else:output[x] = fromstring(req.text).xpath(xpath[x])[0]
   except:output[x]=''
  return output
 else:
  try:
   if e_symbol in xpath:get,xpath=xpath.split(e_symbol)[-1],xpath.split(e_symbol)[0]
   if get:
    if get=='html':return tostring(fromstring(req.text).xpath(xpath)[0]).decode("utf-8")
    else:return fromstring(req.text).xpath(xpath)[0].text_content() if get=='text' else fromstring(req.text).xpath(xpath)[0].get(get)
   else:return fromstring(req.text).xpath(xpath)[0]
  except:return ''

def extractcss(csstag,req):
 output,tag,get = {},'',False
 if isinstance(csstag,dict):
  for x in csstag:
   tag = csstag[x]
   if e_symbol in csstag[x]:get,tag=csstag[x].split(e_symbol)[-1],csstag[x].split(e_symbol)[0]
   try:sel = CSSSelector(tag)
   except:output[x]='';continue
   if get:
     if get=='html':output[x] = cleantag([tostring(e,encoding='UTF-8').decode("utf-8") for e in sel(fromstring(req.content.decode("utf-8")))])
     else:output[x] = cleantag([e.text_content() if get=='text' else e.get(get) for e in sel(fromstring(req.text))])
   else:output[x] = cleantag([e for e in sel(fromstring(req.text))])
  return output  
 else:
  if e_symbol in csstag:get,csstag=csstag.split(e_symbol)[-1],csstag.split(e_symbol)[0]
  try:sel = CSSSelector(csstag)
  except:return ['']
  if get:
    if get=='html':return cleantag([tostring(e).decode("utf-8") for e in sel(fromstring(req.text))])
    else:return cleantag([e.text_content() if get=='text' else e.get(get) for e in sel(fromstring(req.text))])
  else:return cleantag([e for e in sel(fromstring(req.text))])

def extractall(req):
 try:return fromstring(req.text)
 except:return req.text

def extractinfo(csstag,req,typ):
    if typ=='css':return extractcss(csstag,req)
    elif typ=='xpath':return extractxpath(csstag,req)
    elif typ=='None':return extractall(req)
 
  