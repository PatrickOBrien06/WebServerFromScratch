import socket, multiprocessing, secrets, string
from functions import render_template, handle_post_request, redirect

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
  
  if filename == "/":
    filename = "index.html"

    response = render_template(filename)

    if method == "POST":
      # Store form data in a dict for fast retreival times
      dict = handle_post_request(headers)
      room_code = dict["room-code"]

      with open("info.txt", "r") as file:
        line1 = file.readlines(1)[0].split("\n")[0]
        print(line1)
        print(room_code)
        if line1 == room_code:
          print("access granted")
          response = redirect("/main")
        else:
          print("access denied")


  elif filename == "/host":
    filename = "host.html"
    alphabet = string.ascii_uppercase
    code = ''.join(secrets.choice(alphabet) for i in range(6))

    with open("info.txt", "a") as file:
      file.write(f"{code}\n")

    response = render_template(filename, code)

  elif filename == "/main":
    filename = "main.html"

    response = render_template(filename, name)
  
  else:
    filename = "404.html"
    response = render_template(filename)
    
    
  # Send data from the URL to the client
  client_connection.sendall(response.encode())
  client_connection.close()
  

if __name__ == "__main__":
  run()