import socket,threading
import pyaudio
import time,os,sys
from multiprocessing import Process
class server:
	host = '192.168.43.240'  #IP地址
	port=9092
	p = pyaudio.PyAudio()
	CHUNK = 1024   #1024B 1KB缓冲区帧数
	FORMAT = pyaudio.paInt16  #大小格式
	CHANNELS = 2     #声道为双声道
	RATE = 44100     #录音的采样率为44.1KHz
	RECORD_SECONDS = 5  #采样的时间
	count=0
	def acceptaudio(self):	
		#接受来自服务器端的音频
		global count
		socketserver = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
		#绑定地址(包括ip地址和端口号)
		socketserver.bind((server.host,server.port))
		p=pyaudio.PyAudio()
		#打开数据流
		stream = p.open(format=server.FORMAT,
		                channels=server.CHANNELS,
		                rate=server.RATE,
		                output=True,
		                frames_per_buffer=server.CHUNK)
		accepteddata,addr=socketserver.recvfrom(1024)
		socketserver.sendto('ok'.encode(),addr)
		print("正在请求语音匹配客户端的ip地址为:"+accepteddata.decode())	
		while True:
			accepteddata,addr=socketserver.recvfrom(1024)				
			#播放
			stream.write(accepteddata)
			#接收成功，返回客户端信息'ok'						
			socketserver.sendto('ok'.encode(),addr)
			#print('已接受'+str(server.count))
			server.count+=1
			#socketserver.close()
	def record(self):
		p = pyaudio.PyAudio()
		stream = p.open(format=server.FORMAT,
		                channels=server.CHANNELS,
		                rate=server.RATE,
		                input=True,
		                frames_per_buffer=server.CHUNK)
		print("* recording")
		frames = []
		for i in range(0, int(server.RATE / server.CHUNK * server.RECORD_SECONDS)):
		    data = stream.read(CHUNK) #将1KB的数据读出赋给data
		    frames.append(data)       #将数据不断添加到数据组末尾
		print("* done recording")
		stream.stop_stream()
		stream.close()
		p.terminate()
		data=b''.join(frames)
		return data	
	def playback(self):
		"声音回放"
		CHUNK = 1024
		WIDTH = 2
		CHANNELS = 2
		RATE = 44100
		RECORD_SECONDS = 5
		p = pyaudio.PyAudio()
		stream = p.open(format=p.get_format_from_width(WIDTH),
		                channels=CHANNELS,
		                rate=RATE,
		                input=True,
		                output=True,
		                frames_per_buffer=CHUNK)

		print("* recording")

		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		    data = stream.read(CHUNK)
		    stream.write(data, CHUNK)
		print("* done")
		stream.stop_stream()
		stream.close()
		p.terminate()
	def server(self):
		global count
		accept_thred=threading.Thread(target=self.acceptaudio)		
		accept_thred.start()
		print('当前count的值为:',server.count)
	def getclient():
	#获取计算机名称
	hostname=socket.gethostname()
	#获取本机IP
	ip=socket.gethostbyname(hostname)
	print(ip)	
	def main(self):
		p=Process(target=self.server,name='server')
		p.start()
		print('开启进程成功!')
		p.join()
if __name__ == '__main__':
	s=server()
	s.main()
