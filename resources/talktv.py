import sys
import urllib, urllib2
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmc
import requests
import webbrowser
from bs4 import BeautifulSoup 
from lib import CMDTools
import datetime
import thread, threading
import time
import os



base_url = sys.argv[0]
web_name="TALKVN.VN"
web_url = "http://talktv.vn/" 
addon_handle = int(sys.argv[1])
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')

args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')


def get_Web_Name():
	return web_name
def get_img_thumb_url():
	return CMDTools.get_path_img('resources/media/talktv.png')
def convertToFileName(filename):
	return "".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ']).rstrip()
def rename_unicode_files(path):
    # returns a list of names (with extension, without full path) of all files 
    # in folder path
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            files.append(name)
	#test list:	
	#%C3%9At+%C3%9A+Nu+774+3-25.11.2015-16.55.15
	for f in files:
		try:
			os.rename(path+f, path+urllib.unquote_plus(f).decode('utf-8'))
		except:	
			xbmc.log("Error rename file: "+f)
	#end test		
    return 
def view_calendar(channel):	
	r = requests.get("http://api.cctalk.vn/calendar/today-ajax/?room_id=%s" % channel)
	json_data = r.json()
	list_calendar=[]
	for item in json_data:
		text_item=item["start_time"]+"-"+item["end_time"]+": "+item["anchor_name"]			
		list_calendar.append(text_item)		
	dialog = xbmcgui.Dialog()
	retSl = dialog.select('Calendar Room %s' % channel, list_calendar)	
	if retSl>=0:
		retYn = dialog.yesno('Download?', 'Do you want to Download?')	
		if retYn>0:			
			xbmc.log(str(json_data[retSl]['start_time']))
			downloadLinkRoomIdol(channel=channel, idolName=convertToFileName(json_data[retSl]['anchor_name']), start_time=json_data[retSl]['start_time'], end_time=json_data[retSl]['end_time']) 
			
	#view_calendar(calendar[0])		
	return
def getLinkRoomIdol(channel):
	link_get_url="http://49.213.74.237/"+channel
	r = requests.get(link_get_url)				
	json_data = r.json()
	link_video=json_data["TALK_LIVE_URL"].split(";")
	return link_video
#Download	
def downloadLinkRoomIdol(channel, idolName, start_time=None, end_time=None):
	xbmc.log("Downloading")
	link_get_url="http://49.213.74.237/"+channel
	
	listDownloading=xbmcgui.Window(10000).getProperty(web_name+".Downloading")
	if listDownloading==None:
		listDownloading=""
	#Set ID download
	dt=datetime.datetime.now()
	idDownload=idolName.encode('utf-8')+"-"+str(dt.day)+"."+str(dt.month)+"."+str(dt.year)+"-"+str(dt.hour)+"."+str(dt.minute)+"."+str(dt.second)
	
	xbmcgui.Window(10000).setProperty(web_name+".Downloading",listDownloading+";"+idDownload)
	xbmcgui.Window(10000).setProperty(idDownload,"True")
	
	if start_time==None:			
		thread.start_new_thread(downloadTalk,(channel, idolName, xbmcaddon.Addon().getSetting("file"), idDownload, ))					
	else:			
		xbmc.log(start_time[0])
		dtn=datetime.datetime.now()
		stt=start_time.split(":")
		count=60*60*int(stt[0])+60*int(stt[1])-60*60*dtn.hour-60*dtn.minute
		t = threading.Timer(count, downloadTalk,(channel, idolName, xbmcaddon.Addon().getSetting("file"), idDownload, end_time, ))
		t.start()
		xbmc.executebuiltin(u'XBMC.Notification("%s", "%s", %s)' % ("Download Sau: ", str(count/60), "Xong"))
		xbmc.log(str(count))					
	return
def view_Downloading():
	listDownloading=xbmcgui.Window(10000).getProperty(web_name+".Downloading")
	if listDownloading!=None:
		items=listDownloading.split(";")
		dialog = xbmcgui.Dialog()
		list=[]
		for item in items:
			if item!="":
				if xbmcgui.Window(10000).getProperty(item)=="True":			
					list.append(item)					
					#li = xbmcgui.ListItem(item)
					#li.addContextMenuItems([('Stop Download', 'XBMC.RunPlugin(%s)' % CMDTools.build_url(base_url,{'web':get_Web_Name(), 'command':'stopDownload', 'idDownload':item}),)])
					#xbmcplugin.addDirectoryItem(handle=addon_handle, url="", listitem=li, isFolder=True)	
		retSelect = dialog.select('Downloading', list)
		if retSelect>=0:
			retYn = dialog.yesno('Stop Download?', 'Do you want to Stop Download?')	
			if retYn>0:
				xbmcgui.Window(10000).setProperty(list[retSelect],"False")
			view_Downloading()
	return
def view():		
	cat=args.get('cat', None)
	command=args.get('command', None)
	page = args.get('page', None)
	link = args.get('link', None)	
	calendar = args.get('calendar', None)
	download = args.get('download', None)
	catalogues=[{'label':'\x44\x61\x6E\x68\x20\x73\xC3\xA1\x63\x68\x20\x63\xC3\xA1\x63\x20\x6B\xC3\xAA\x6E\x68\x20\xC4\x91\x61\x6E\x67\x20\x63\x68\x69\xE1\xBA\xBF\x75'.decode('utf-8'),'id':'http://talktv.vn/browse/channels'},
	{'label':'\x47\x69\xE1\xBA\xA3\x69\x20\x54\x72\xC3\xAD'.decode('utf-8'),'id':'http://talktv.vn/browse/channels/151/Gi%E1%BA%A3i%20Tr%C3%AD'},
	{'label':'\x4C\x69\xC3\xAA\x6E\x20\x4D\x69\x6E\x68\x20\x48\x75\x79\xE1\xBB\x81\x6E\x20\x54\x68\x6F\xE1\xBA\xA1\x69'.decode('utf-8'),'id':'http://talktv.vn/browse/channels/112/Li%C3%AAn%20Minh%20Huy%E1%BB%81n%20Tho%E1%BA%A1i'},
	{'label':'\x56\x69\x64\x65\x6F\x20\x54\x75\xE1\xBA\xA7\x6E'.decode('utf-8'),'id':'http://talktv.vn/browse/videos/ajax-get-videos/page/week'},
	{'label':'\x56\x69\x64\x65\x6F\x20\x54\x68\xC3\xA1\x6E\x67'.decode('utf-8'),'id':'http://talktv.vn/browse/videos/ajax-get-videos/page/month'},
	{'label':'\x54\xE1\xBA\xA5\x74\x20\x63\xE1\xBA\xA3\x20\x56\x69\x64\x65\x6F'.decode('utf-8'),'id':'http://talktv.vn/browse/videos/ajax-get-videos/page/all'}]

	if command!=None:
		if command[0]=='download':
			xbmc.log(args.get('title', None)[0])
			downloadLinkRoomIdol(args.get('channel', None)[0], convertToFileName(args.get('title', None)[0].decode('utf-8')))
		elif command[0]=='downloading':
			view_Downloading()
			return
		elif command[0]=='stopDownload':
			idDownload=args.get('idDownload', None)
			xbmcgui.Window(10000).setProperty(idDownload[0],"False")
			return
		elif command[0]=='view_calendar':
			channel=args.get('channel', None)
			view_calendar(channel[0])		
			return	
		elif command[0]=='rename_unicode_files':
			path_files=xbmcaddon.Addon().getSetting("file")
			rename_unicode_files(path_files)
			return
	#play link
	if link!=None:		
		xbmc.log("--------------------:"+link[0])
		link_video=link[0]
		if (link_video.startswith('http://talktv.vn/video')):
			link_get_url=link_video
			r = requests.get(link_get_url)
			html_data = r.text			
			start_pos = html_data.find('loadVideo.mp4')
			start_pos = html_data.find('\"',start_pos)+1
			end_pos = html_data.find('\"',start_pos)-len(html_data)
			link_video=html_data[start_pos:end_pos]
			#xbmc.log("@@@"+link_video.encode('utf-8'))
			#link_video=json_data["manifestUrl"]
			xbmc.Player().play(link_video)			
		elif (link_video.startswith('http://talktv.vn/')):
			channel=link_video[len(web_url):]
			if channel.isdigit():	
				if channel=='2222':
					channel='30001'
				links=getLinkRoomIdol(channel)				
				xbmc.Player().play(links[0])
			else:
				link_get_url="http://talktv.vn/streaming/play/get-stream-data/channel/"+channel+"/limit/1"
				r = requests.get(link_get_url)
				json_data = r.json()
				link_video=json_data["manifestUrl"]
				xbmc.Player().play(link_video)
		return
	#Load cats
	if cat==None:
		for cat in catalogues:
			li = xbmcgui.ListItem(cat['label'])
			li.addContextMenuItems([
				('Rename to Unicode', 'XBMC.RunPlugin(%s)' % CMDTools.build_url(base_url,{'web':get_Web_Name(), 'command':'rename_unicode_files'}),)])
			urlList = CMDTools.build_url(base_url,{'web':get_Web_Name(), 'cat':cat['id']})
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=urlList, listitem=li, isFolder=True)
		return
		
	#Load noi dung cat
	if cat!=None:
		if page==None:
			page=0
		else:
			page=int(page[0])
			
		r = requests.get(cat[0].replace('page',str(page)))
		html = r.text				
		soup = BeautifulSoup(html)
		data_List=soup.findAll('div',attrs={'class':'cellitem'})
		
		#load item menu
		for item in data_List:			
			link_item=item.find('a', attrs={'class':'cellthumb'}).get('href')
			img_item=item.find('img').get('data-src')
			img_avt=item.find('a', attrs={'class':'profileavt'}).find('img').get('src')
			text_item=item.find('p', attrs={'class':'txtname'}).find('strong').getText()
			
			channel=link_item[len(web_url):]			
			li = xbmcgui.ListItem(text_item)
			if channel.isdigit():
				li.setLabel(channel+": "+text_item)
				if channel=='2222':
					channel='30001'									
				li.setThumbnailImage(img_avt)
				#if page>0:
				#Them menu Download, Calendar
				li.addContextMenuItems([
				('Download', 'XBMC.RunPlugin(%s)' % CMDTools.build_url(base_url,{'web':get_Web_Name(), 'command':'download','channel':channel, 'title':text_item.encode('utf-8')}),), 
				('Calendar', 'XBMC.RunPlugin(%s)' % CMDTools.build_url(base_url,{'web':get_Web_Name(), 'command':'view_calendar','channel':channel}),), 
				('All Downloading', 'XBMC.RunPlugin(%s)' % CMDTools.build_url(base_url,{'web':get_Web_Name(), 'command':'downloading'}),)
				])
			else:
				li.setThumbnailImage(img_item)
			li.setInfo(type='image',infoLabels=text_item)				
			urlList = CMDTools.build_url(base_url,{'web':get_Web_Name(), 'link':link_item.encode('utf-8'), 'type':cat[0], 'page':str(page), 'channel':channel.encode('utf-8')})
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=urlList, listitem=li)
		#Tao nut next	
		li = xbmcgui.ListItem("Next")	
		urlList=CMDTools.build_url(base_url,{'web':web_name, 'cat':cat[0],'page': page+1})
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=urlList, listitem=li, isFolder=True)	
		return
#Tai file 		
def downloadTalk(channel, filename, path, idDownload, end_time=None):	
	xbmc.log("Download: " + urllib.quote_plus(filename.encode('utf-8')))	
	#xbmc.log("Download: " + urllib.unquote_plus(urllib.quote_plus(filename.encode('utf-8'))))
	while True:
		try:
			isContinue=xbmcgui.Window(10000).getProperty(idDownload)
			if isContinue=="False":
				break
			#get link
			links=getLinkRoomIdol(channel)
			
			#dat ten file
			dt=datetime.datetime.now()
			#filename.encode('ascii', 'ignore')
			
			pathfile=path+urllib.quote_plus(filename.encode('utf-8'))+" - ("+str(dt.day)+"."+str(dt.month)+"."+str(dt.year)+"-"+str(dt.hour)+"."+str(dt.minute)+"."+str(dt.second)+").flv"		
			u = urllib2.urlopen(links[0])
			xbmc.executebuiltin(u'XBMC.Notification("%s", "%s", %s)' % ("Bat dau download", filename.encode('ascii', 'ignore'),"Bat dau"))			

			f = open(pathfile, 'wb')
			#meta = u.info()
			#file_size = int(meta.getheaders("Content-Length")[0])
			#print "Downloading: %s Bytes: %s" % (filename, file_size)

			file_size_dl = 0
			block_sz = 8192
			while True:
				#Kiem tra neu download bi tat
				isContinue=xbmcgui.Window(10000).getProperty(idDownload)
				if isContinue=="False":					
					break
				#Tien hanh download	
				buffer = u.read(block_sz)
				if not buffer:				
					break
				file_size_dl += len(buffer)
				f.write(buffer)
				#status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
				#status = status + chr(8)*(len(status)+1)
				#print str(file_size_dl)				
			f.close()
			xbmc.executebuiltin(u'XBMC.Notification("%s", "%s", %s)' % ("Download Xong", filename.encode('ascii', 'ignore'), "Xong"))			
		except:			
			if end_time!=None:
				dtn=datetime.datetime.now()
				et=end_time.split(":")
				count=60*60*int(et[0])+60*int(et[1])-60*60*dtn.hour-60*dtn.minute
				if count<=0:
					xbmc.log("__End Time___")		
					xbmcgui.Window(10000).setProperty(idDownload,"False")
					break
			xbmc.log("__Sleep___")		
			time.sleep(5)
			xbmc.log("__Continue___")		