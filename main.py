import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("0.0.0.0", 50))
sock.listen(1)

while True:
  client_connection, client_address = sock.accept()

  request = client_connection.recv(1024).decode()
  print(request)

  headers = request.split("\n")
  filename = headers[0].split()[1]

  if filename == "/":
    filename = "index.html"

  elif filename == "/about":
    filename = "about.html"

  try:
    fin = open("htdocs/" + filename)
    content = fin.read()
    fin.close()
    response = "HTTP/1.0 200 OK\n\n" + content
  except FileNotFoundError:

    response = "HTTP/1.0 404 NOT FOUND\n\nFile Not Found 404"
    
  client_connection.sendall(response.encode())
  client_connection.close()




