import socket

class DNSQuery:
  def __init__(self, data):
    self.data=data
    self.dominio=''

    tipo = (ord(data[2]) >> 3) & 15   # 4bits de tipo de consulta
    if tipo == 0:                     # Standard query
      ini=12
      lon=ord(data[ini])
      while lon != 0:
        self.dominio+=data[ini+1:ini+lon+1]+'.'
        ini+=lon+1
        lon=ord(data[ini])

  def respuesta(self, ip):
    packet=''
    if self.dominio:
      packet+=self.data[:2] + "\x81\x80"
      packet+=self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'   # Numero preg y respuestas
      packet+=self.data[12:]                                         # Nombre de dominio original
      packet+='\xc0\x0c'                                             # Puntero al nombre de dominio
      packet+='\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'             # Tipo respuesta, ttl, etc
      packet+=str.join('',map(lambda x: chr(int(x)), ip.split('.'))) # La ip en hex
    return packet

if __name__ == '__main__':
  ip='192.168.0.254'
  print ('pyminifakeDNS:: dom.query. 60 IN A %s' % ip)

  udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  udps.bind(('',53))
  
  try:
    while 1:
      data,addr = udps.recvfrom(1024) 
      #addr = udps.recvfrom(1024)
      #print('data=%s' % data)
      #dataok = data[0]
      #print(data)
      #print(data[2])
      #print(type(data))
      #print(ord(data[2])) 
      p=DNSQuery(data)
      udps.sendto(p.respuesta(ip), addr)
      print ('Respuesta: %s -> %s' % (p.dominio, ip))
  except KeyboardInterrupt:
    print ('Finalizando')
    udps.close()