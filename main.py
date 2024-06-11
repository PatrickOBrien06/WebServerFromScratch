import socket, multiprocessing, secrets, string
from render_template import render_template

def run():

  # Config server to a socket it doesn't matter what the socket is
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind(("0.0.0.0", 50))
  sock.listen(1)

  # Accept incoming connections from client
  while True:
    client_connection, client_address = sock.accept()

    # Run the client process
    client_process = multiprocessing.Process(target=handle_client, args=(client_connection, client_address))
    client_process.start()
  

# Handle client connections and URLs
def handle_client(client_connection, client_address):

  # Receive and decode
  request = client_connection.recv(1024).decode()
  print(request)

  # Split header to obtain URL
  headers = request.split("\n")
  filename = headers[0].split()[1]
  method = headers[0].split()[0]

  # If URL does not exist then show 404 error page
  try:
    if filename == "/":
      alphabet = string.ascii_uppercase
      code = ''.join(secrets.choice(alphabet) for i in range(6))

      response = render_template("index.html", code)
    
    elif filename == "/about":
      response = render_template("about.html")


  except FileNotFoundError:
    response = "HTTP/1.0 404 NOT FOUND\n\nFile Not Found 404"

  # Send data from the URL to the client
  client_connection.sendall(response.encode())
  client_connection.close()
  

if __name__ == "__main__":
  run()