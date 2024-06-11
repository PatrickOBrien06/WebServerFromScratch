def render_template(filename, *args):
  fin = open("templates/" + filename)
  content = fin.read()
  content = content.format(*args)
  fin.close()
  response = "HTTP/1.0 200 OK\n\n" + content
  return response