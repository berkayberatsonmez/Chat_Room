import socket
import threading

nickname = input("Nickname: ") #kullanicidan diger insanlarin gore bilecegi bir nickname istiyoruz.

client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
client.connect(('127.0.0.1' , 55555)) #socketimizi serveririmiza bagliyoruz.

def receive():
	while True:
		try:
			message = client.recv(1024).decode('ascii') #gonderdigimiz mesajlari ascii tablosuna uygunlugunu kontrol ediyoruz.
			if message == 'NICK':
				client.send(nickname.encode('ascii')) #eger mesaj olarak NICK yazarsak bizim adimizi yaziyor.
			else:
				print(message)
		except:
			print("Error") #eger ascii tablosuna uymuyor ise clienti kapatiyor
			client.close()
			break


def write():
	while True:
		message = '{}: {}'.format(nickname , input('')) #server a bagli kisilerden gelen mesajlari bastiriyor.
		client.send(message.encode('ascii')) #gelen mesajlari encode ederek ascii tablosuna uygun bir sekilde yaziyor.

receive_thread = threading.Thread(target=receive) #receive fonksiyonunu paralel olarak calistirmasini sagliyor bu sayede surekli mesaj yazabiliyoruz.
receive_thread.start()

write_thread = threading.Thread(target=write) #write fonksiyonunu paralel olarak calismasini sagliyor bu sayede serverdaki kullanicilardan surekli mesaj alabiliyoruz ve sürekli mesaj yazabiliyoruz.
write_thread.start()		