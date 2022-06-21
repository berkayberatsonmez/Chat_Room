import socket
import threading

host = '127.0.0.1' #host tanimliyoruz
port = 55555 #port tanimliyoruz

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM) #socket olusturuyoruz.(family,type)burada yazdigimiz AF_INET TCP ve UDP icin IPv4 protokolleri icin kullaniliyor, SOCK_STREAM ise TCP in baglanti tipi.
server.bind((host , port)) #tanimladigimiz host ve port u socketimize atiyoruz.
server.listen() #server kanalını dinlemeye başlıyoruz. burada parantez icine yazdigimiz deger kac kisinin baglanabilicegini gosterir.

clients = []
nicknames = [] #arraylerimizi olusturuyoruz

def broadcast(message):
	for client in clients:
		client.send(message) #kullanicilardan gelen mesajlari diger kullanicilarin clientlerine gonderiyoruz.

def handle(client):
	while True:
		try:
			message = client.recv(1024) #burada recv fonksiyonu gelen veriyi okumasini sagliyor ve buffer sizesini belirliyor yani saniyede alıcak maksimum dosya boyutu.
			broadcast(message)
		except: #eger kullanıcı bir şekilde clientten çıkarsa clienti kapatılıyor nicknamesi arrayden siliniyor ve diğer kullanıcılara çıktı bilgisi veriliyor.
			index = clients.index(client) # dizinde yer aldığı sıra numarasını döndürüyor.
			clients.remove(client)
			client.close()
			nickname = nicknames[index]
			broadcast('{} left !'.format(nickname).encode('ascii'))
			nicknames.remove(nickname) # dizinden kaldırıyoruz.
			break

def receive():
	while True:
		client, address = server.accept() #servera baglanan kisinin adress bilgilerini tutuyor, kabul ediyor
		print('connected with {}'.format(str(address))) #serverdaki herkese baglanan kisinin adresini server a bastiriyor kullanicilar gormuyor

		client.send('NICK'.encode('ascii'))
		nickname = client.recv(1024).decode('ascii') #nicknami ascii tablosuna gore decode ediyor.
		nicknames.append(nickname)
		clients.append(client) #burada nicknamei ve clienti olusturdugumuz arraylere ekliyor

		print("Nickname is {}".format(nickname)) #burada servera giren kullanicilarin nicknamesini server kisiminda bastiriyor
		broadcast("{} joined!".format(nickname).encode('ascii')) #server a bagli olan kullanicilara katilan kisinin katildigi bilgisini veriyor
		client.send('Connected to server!'.encode('ascii')) #kullaniciya baglandigina dair mesaj gonderiyor

		thread = threading.Thread(target=handle , args=(client,)) #burada handle fonksiyonun eş zamanlı olarak çalışmasını sağlıyor
		thread.start()

receive()