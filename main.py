import socket
import multiprocessing

# Handle client connections and URLs
def handle_client(client_connection, client_address):

  # Receive and decode
  request = client_connection.recv(1024).decode()
  print(request)

  # Split header to obtain URL
  headers = request.split("\n")
  filename = headers[0].split()[1]
  method = headers[0].split()[0]

  print(headers)

  if filename == "/":
    if method == "POST":
      print("POST")
    filename = "index.html"
    

  elif filename == "/about":
    filename = "about.html"


  # If URL does not exist then show 404 error page
  try:
    fin = open("templates/" + filename)
    content = fin.read()
    fin.close()
    response = "HTTP/1.0 200 OK\n\n" + content

  except FileNotFoundError:

    response = "HTTP/1.0 404 NOT FOUND\n\nFile Not Found 404"


  # Send data from the URL to the client
  client_connection.sendall(response.encode())
  client_connection.close()


def main():

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind(("0.0.0.0", 50))
  sock.listen(1)

  while True:
    client_connection, client_address = sock.accept()

    client_proccess = multiprocessing.Process(target=handle_client, args=(client_connection, client_address))
    client_proccess.start()
  

if __name__ == "__main__":
  main()