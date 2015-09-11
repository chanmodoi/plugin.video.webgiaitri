import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmc
import json
import urllib2
import httplib 
from lib import requests
from lib import CMDTools
from lib import CommonFunctions

base_url = sys.argv[0]
web_name="GIOITRE.NET"
web_url = "http://gioitre.net/" 

#xbmc.log(r.text)

def get_Web_Name():
	return web_name
def get_img_thumb_url():
	return CMDTools.get_path_img('resources/media/gioitre.png')
def view():	

	addon_handle = int(sys.argv[1])

	addon       = xbmcaddon.Addon()
	addonname   = addon.getAddonInfo('name')
	
	args = urlparse.parse_qs(sys.argv[2][1:])

	xbmcplugin.setContent(addon_handle, 'movies')
	common = CommonFunctions

	cat=args.get('cat', None)
	page = args.get('page', None)
	link = args.get('link', None)
	
	catalogues=[{'label':'Video','id':'video'},
				{'label':'Girl Xinh','id':'girl-xinh'}]
	#play link
	if link!=None:
		type = args.get('type', None)
		if type[0]=='girl-xinh':
			r = requests.get('http://gioitre.net'+link[0])
			html = r.text
			div_contentDeatil=common.parseDOM(html, name="div", attrs = {"class":"contentDeatil"})
			p_styles=common.parseDOM(html, name="p", attrs = {"class":"separator"})
			
			play_list=xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
			play_list.clear()
			for p in p_styles:
				#xbmc.log("p_styles:"+str(p).encode('utf-8'))				
				img=common.parseDOM(p, name="a", ret="href")
				if len(img)>0:
					play_list.add(img[0])
			#xbmc.Player().play(play_list)
			#xbmc.SlideShow(play_list)
			
			xbmc.executebuiltin('SlideShow(['+'http://3.bp.blogspot.com/-DyIzIopGp5w/VemhuSNYjKI/AAAAAAAAVvw/z7F8brm2eF4/s1600/10424304_509281719224464_5377204222107731550_n.jpg'+'])')
		elif type[0]=='video':
			xbmc.Player().play("plugin://plugin.video.youtube/play/?video_id="+link[0])
		return
	#Load cats
	if cat==None:
		for cat in catalogues:
			li = xbmcgui.ListItem(cat['label'])
			urlList = CMDTools.build_url(base_url,{'web':get_Web_Name(), 'cat':cat['id']})
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=urlList, listitem=li, isFolder=True)	
		xbmc.executebuiltin('Container.SetViewMode(501)')		 			
		xbmcplugin.endOfDirectory(addon_handle)
		return
	#Load noi dung cat
	if cat!=None:
		if page==None:
			page=1
		else:
			page=int(page[0])
		r = requests.get(web_url+cat[0]+'?page='+str(page))
		html = r.text

		data_list=common.parseDOM(html, name="div", attrs = {"class":"listLage"})	
		data=common.parseDOM(data_list,name='li')
		#load item menu
		for item in data:
			img_alt=common.parseDOM(item,name='img', ret='alt')
			img_src=common.parseDOM(item,name='img', ret='src')
			
			li = xbmcgui.ListItem(img_alt[0])
			
			li.setThumbnailImage(img_src[0])
			
			if cat[0]=='video':			
				urlList = CMDTools.build_url(base_url,{'web':get_Web_Name(), 'link':img_src[0][26:-6], 'type':cat[0]})
			elif cat[0]=='girl-xinh':	
				img_src=common.parseDOM(item,name='a', ret='href')
				urlList = CMDTools.build_url(base_url,{'web':get_Web_Name(), 'link':img_src[0], 'type':cat[0]})
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=urlList, listitem=li)			
		
		#Tao nut next	
		li = xbmcgui.ListItem("Next")	
		urlList=CMDTools.build_url(base_url,{'web':web_name, 'cat':cat[0],'page': page+1});
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=urlList, listitem=li, isFolder=True)	
		
		xbmc.executebuiltin('Container.SetViewMode(501)')		 
		xbmcplugin.endOfDirectory(addon_handle)
		return
					
	xbmcplugin.endOfDirectory(addon_handle)