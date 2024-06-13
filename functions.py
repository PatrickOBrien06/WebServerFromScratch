def render_template(filename, *args):
  fin = open("templates/" + filename)
  content = fin.read()
  content = content.format(*args)
  fin.close()
  response = "HTTP/1.1 200 OK\n\n" + content
  return response

def handle_post_request(headers):
  dict = {}
  inputs = headers[-1].split("&")[0:]
  for pair in inputs:
    key, value = pair.split("=")
    dict[key] = value
  
  return dict

def redirect(location, permanent=False, *args):
    status_code = "301 Moved Permanently" if permanent else "302 Found"
    response = f"HTTP/1.1 {status_code}\r\nLocation: {location}\r\nConnection: close\r\n\r\n"
    return response, *args