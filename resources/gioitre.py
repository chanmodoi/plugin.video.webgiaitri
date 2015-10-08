import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmc
import requests
import CommonFunctions
from bs4 import BeautifulSoup 
from lib import CMDTools



base_url = sys.argv[0]
web_name="GIOITRE.NET"
web_url = "http://gioitre.net/" 

def get_Web_Name():
	return web_name
def get_img_thumb_url():
	return CMDTools.get_path_img('resources/media/gioitre.png')
def show_photos(url):	
	common = CommonFunctions
	r = requests.get('http://gioitre.net'+url)
	html = r.text
	div_contentDeatil=common.parseDOM(html, "div", attrs = {"class":"contentDeatil"})	
	imgs=common.parseDOM(div_contentDeatil, "img", ret='src')
	for img in imgs:				
		xbmc.log("---------------------------------2"+str(img))
		img_src=img
		li = xbmcgui.ListItem(label="",thumbnailImage=img_src) 
		li.setInfo(type='image', infoLabels={'Title': ''})
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=img_src,listitem=li,isFolder=False)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

    
def view():	
	#xbmc.executebuiltin("SlideShow(,,notrandom)")
	addon_handle = int(sys.argv[1])

	addon       = xbmcaddon.Addon()
	addonname   = addon.getAddonInfo('name')
	
	args = urlparse.parse_qs(sys.argv[2][1:])

	xbmcplugin.setContent(addon_handle, 'movies')

	common = CommonFunctions
	#get args
	cat=args.get('cat', None)
	page = args.get('page', None)
	link = args.get('link', None)
	show=args.get('show', None)
	
	catalogues=[{'label':'Video','id':'video'},
				{'label':'Girl Xinh','id':'girl-xinh'},
				{'label':'\xC4\x90\xE1\xBA\xB9\x70'.decode('utf-8'),'id':'dep'}]
	if (show!=None):
		show_photos(show[0])
		return
	#play link
	if link!=None:
		type = args.get('type', None)
		if type[0]!='video':			
			xbmc.executebuiltin("SlideShow(%s,recursive,notrandom)" % CMDTools.build_url(base_url,{'web':get_Web_Name(), 'show':link[0]}))
		elif type[0]=='video':
			xbmc.Player().play("plugin://plugin.video.youtube/play/?video_id="+link[0])
		return
	#Load cats
	if cat==None:
		for cat in catalogues:
			li = xbmcgui.ListItem(cat['label'])
			urlList = CMDTools.build_url(base_url,{'web':get_Web_Name(), 'cat':cat['id']})
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=urlList, listitem=li, isFolder=True)			
		return
	#Load noi dung cat
	if cat!=None:
		if page==None:
			page=1
		else:
			page=int(page[0])
		r = requests.get(web_url+cat[0]+'?page='+str(page))
		html = r.text		
	
		data_list=common.parseDOM(html, "div", attrs = {"class":"listLage"})
		if len(data_list)==0:
			data_list=common.parseDOM(html, "div", attrs = {"class":"listItemnews"})
		
		data=common.parseDOM(data_list[0],'li')
		#load item menu
		for item in data:			
			img_alt=common.parseDOM(item,'img',ret='alt')
			if len(img_alt)>0:
				img_alt=img_alt[0]
			else:
				img_alt=''
			img_src=common.parseDOM(item,'img',ret='src')
			if len(img_src)>0:
				img_src=img_src[0]
			else:
				img_src=''
			
			li = xbmcgui.ListItem(img_alt)			
			li.setThumbnailImage(img_src)
			li.setInfo(type='image',infoLabels="")
			
			if cat[0]=='video':			
				urlList = CMDTools.build_url(base_url,{'web':get_Web_Name(), 'link':img_src[26:-6], 'type':cat[0]})
			else:	
				img_link=common.parseDOM(item,'a',ret='href')
				if len(img_alt)>0:
					img_link=img_link[0]
				else:
					img_link=''
				urlList = CMDTools.build_url(base_url,{'web':get_Web_Name(), 'link':img_link, 'type':cat[0]})
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=urlList, listitem=li)			
		
		#Tao nut next	
		li = xbmcgui.ListItem("Next")	
		urlList=CMDTools.build_url(base_url,{'web':web_name, 'cat':cat[0],'page': page+1});
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=urlList, listitem=li, isFolder=True)			
		return	