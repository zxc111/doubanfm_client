# -*- coding: UTF-8 -*-
import wx
import threading,time
import pymedia.muxer as muxer, pymedia.audio.acodec as acodec, pymedia.audio.sound as sound
import time,urllib2,json

class Frame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self,None,-1,u'播放器',size=(300,100))
		self.panel = wx.Panel(self, -1)
		self.button=wx.Button(self.panel,-1,u"开始",(10,10))
		self.button1=wx.Button(self.panel,-1,u"暂停",(80,10))
		self.button2=wx.Button(self.panel,-1,u"继续",(150,10))
		self.Bind(wx.EVT_BUTTON,self.OnClick1,self.button)
		self.Bind(wx.EVT_BUTTON,self.OnClick2,self.button1)
		self.Bind(wx.EVT_BUTTON,self.OnClick3,self.button2)
		self.Bind(wx.EVT_CLOSE,self.OnClose)
		self.button.SetDefault()
		self.status=0
		
	def OnClick1(self,event):
		#wx.StaticText(self.panel,-1,"test",(100,10))
		if self.status==0:
			self.status=1
			self.music=main()
			self.music.setDaemon(True)
			self.music.start()
		
	def OnClick2(self,event):
		self.music.pause()
		
	def OnClick3(self,event):
		self.music.unpause()
		
	def OnClose(self,event):
		ret=wx.MessageBox(u"是否退出",'123',wx.OK|wx.CANCEL)
		if ret==wx.OK:
			#self.music.join()
			wx.Exit()



class main(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		#self.status=0
		
	def run(self):
		self.status=1
		self.aplayer( 0, 1, -1 )
		
	def aplayer( self, card, rate, tt ):
	  dm= muxer.Demuxer( "mp3" )
	  snds= sound.getODevices()
	  get=urllib2.urlopen("http://douban.fm/j/mine/playlist")
	  data=get.read()
	  s=json.loads(data)
	  url=s["song"][1]["url"]
	  if card not in range( len( snds ) ):
		raise 'Cannot play sound to non existent device %d out of %d' % ( card+ 1, len( snds ) )
	  #f=urllib2.urlopen("http://zxc111.net/1.mp3")
	  f=urllib2.urlopen(url)
	  #f= open( name, 'rb' )
	  self.snd= resampler= dec= None
	  s= f.read(1024)
	  t= 0
	  while len( s ):
		frames= dm.parse( s )
		if frames:
		  for fr in frames:
			# Assume for now only audio streams

			if dec== None:
			  print dm.getInfo(), dm.streams
			  dec= acodec.Decoder( dm.streams[ fr[ 0 ] ] )
			
			r= dec.decode( fr[ 1 ] )
			if r and r.data:
			  if self.snd== None:
				print 'Opening sound with %d channels -> %s' % ( r.channels, snds[ card ][ 'name' ] )
				self.snd= sound.Output( int( r.sample_rate* rate ), r.channels, sound.AFMT_S16_LE, card )
				if rate< 1 or rate> 1:
				  resampler= sound.Resampler( (r.sample_rate,r.channels), (int(r.sample_rate/rate),r.channels) )
				  print 'Sound resampling %d->%d' % ( r.sample_rate, r.sample_rate/rate )
			  
			  data= r.data
			  if resampler:
				data= resampler.resample( data )
			  EMULATE=0
			  if EMULATE:
				# Calc delay we should wait to emulate self.snd.play()

				d= len( data )/ float( r.sample_rate* r.channels* 2 )
				time.sleep( d )
				if int( t+d )!= int( t ):
				  print 'playing: %d sec\r' % ( t+d ),
				t+= d
			  else:
				self.snd.play( data )
		if tt> 0:
		  if snd and self.snd.getPosition()> tt:
			break
		
		s= f.read( 512 )

	  while self.snd.isPlaying():
		time.sleep( .05 )
			
	def pause(self):
		self.snd.pause()
	
	def unpause(self):
		self.snd.unpause()
		
if __name__=='__main__':
	app=wx.PySimpleApp()
	frame=Frame()
	frame.Show()
	app.MainLoop()