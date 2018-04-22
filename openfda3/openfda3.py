import http.server
import json
import socketserver

IP = 'localhost'
PORT = 8000

# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        headers = {'User-Agent': 'http-client'}

        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?limit=10", None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        drugs_raw = r1.read().decode("utf-8")
        conn.close()
        #WITH THIS .LOADS FUNCTION WE DECODE THE JAVA SCRIPT OBJECT NOTATION IN ORDER TO BE ABLE TO APPEND ON AN EMPTY LIST THE ID OF EACH DRUG CONTAINED IN JSON
        drugs = json.loads(drugs_raw)['results']
        print(drugs)

        list=[]

        for drug in drugs:
            list.append(drug['id'])

        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()
        #IN ORDER TO CREATE THE HTML DOCUMENT WITH THE DRUGS WE WRITE THIS:
        intro = "<!doctype html>" + "\n" + "<html>" + "\n" + "<body>" + "\n" "<ol>" + "\n"
        end = "</ol>" + "\n" + "</body>" + "\n" + "</html>"
        #IN ORDER TO IMPLEMENT THE ID OF THE DRUG THAT WE APPEND ON THE EMPTY LIST WE CREATE A FOR LOOP AND USE THE FUNCTION .WRITE
        with open("drugs.html",'w') as f:
            f.write(intro)
            for element in list:
                f.write( "<br>" + element +  "</br>")
            f.write(end)
        with open('drugs.html','r') as f:
            file = f.read()
            self.wfile.write(bytes(file, "utf8"))
        return

Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()

# https://github.com/joshmaker/simple-python-webserver/blob/master/server.py
