import threading,pyaudio,socket
import wave
#创建一个客户端的socket对象
CHUNK = 16   #1024B 1KB缓冲区帧数
FORMAT = pyaudio.paInt16  #大小格式
CHANNELS = 2     #声道为双声道
RATE = 44100     #录音的采样率为44.1KHz
RECORD_SECONDS = 50 #采样的时间
def sendauido():
	"发送数据"
	count=0
	#发送数据，以二进制的形式发送数据，所以需要进行编码
	client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	#设置服务端的ip地址
	host='192.168.43.240'
	#设置端口
	port = 9092
	#连接服务端
	p=pyaudio.PyAudio()
	stream=p.open(format=FORMAT,
				  channels=CHANNELS,
				  rate=RATE,
				  input=True,
				  frames_per_buffer=CHUNK)
	print("*recording")
	client.sendto(getip().encode(),(host,port))
	recvdata,addr = client.recvfrom(1024)
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data=stream.read(CHUNK,exception_on_overflow=False)#缓冲阻塞不中断
		if i==0:
			client.sendto(data,(host,port))
			#print('已发送'+str(count))
			count+=1
			recvdata,addr = client.recvfrom(1024)
		else:
			if str(recvdata)=="b'ok'":
				client.sendto(data,(host,port))
				#print('已发送'+str(count))
				count+=1
				recvdata,addr = client.recvfrom(1024)				
			else:
				print("信息传输有误!")
	print("* done recording")
	stream.stop_stream()
	stream.close()
	p.terminate()
def getip():
	#获取计算机名称
	hostname=socket.gethostname()
	#获取本机IP
	ip=socket.gethostbyname(hostname)
	return ip
sendauido()
