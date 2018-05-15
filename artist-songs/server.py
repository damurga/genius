import http.server
import socketserver
import http.client
import json
import urllib.parse

#Importamos los módulos que vamos a utilizar y definimos el puerto


PORT = 8000



class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)

        #En la siguiente variable escribimos el header que vamos a mandar a la Api con la solicitud GET, junto a "Bearer"
        #escribimos el token de acceso obtenido de la propia web tras habernos hecho una cuenta
        headers = {'Authorization': 'Bearer 77S0tcBxveoZbgHWAdfm1v0zeIwvyhLOepbz2UWanDYyrHcrMrHnDXupeSfHeqtw'}
        #Asi no es necesario usar sys.argv para obtenerlo de la terminal

        def searchartist():

            artist = str(parsed_path.query).split("=")
            #Para realizar la búsqueda debemos sustituir "artist=" por "q=" y obtendremos toda la información de la Api sobre
            #ese artista
            artist[0] = "q="
            url = ("=").join(artist).replace("+", "%20")

            conn = http.client.HTTPSConnection("api.genius.com")

            #Al enviar el header anterior con la cabecera de petición la Api nos autoriza el acceso y la obtención del Json
            #con los datos que solicitemos en la búsqueda
            conn.request("GET", "/search?{}".format(url), None, headers)

            r1 = conn.getresponse()

            print(r1.status, r1.reason)

            label_raw = r1.read().decode("utf-8")

            conn.close()

            labelfull = json.loads(label_raw)

            #Comenzamos la extracción de datos dentro del Json que nos devuelve la Api
            label = labelfull['response']['hits']

            message2 = """<!DOCTYPE HTML>
                                       <html lang="es">
                                       <head>
                                         <title>canciones del artista</title>
                                       </head>
                                       <body style='background-color: #CDE2E6'>
                                         <h1 align="center">CANCIONES DEL ARTISTA</h1>
                                         <hr style="color:red"/><hr style="color:red"/><hr style="color:red"/>"""


            #Iteramos sobre todos los resultados (sobre todas las canciones del artista y sus datos asociados)
            for dic in label:
                #Obtenemos título de cada canción y su imagen representativa
                song = dic['result']['title']
                pic = dic['result']['header_image_url']
                #Introducimos los datos en el mensaje que enviaremos al cliente que haya solicitado los datos
                message2 += "<h2 align=\"center\"><u>{}</u></h2>".format(song)
                message2 += "<div align=\"center\"><img src={} border=\"0\" height=300 width=400 ></div>".format(pic)
                message2 += "<br>" \
                            "<hr>" \
                            "<br>"

            message2 += "</body>" \
                        "</html>"


            #Enviamos la cabecera "200 OK"
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(message2, "utf8"))

            return

#-----------------------------------------------------------------------------------------------------------------------

        message = """<!DOCTYPE HTML>
                            <html lang="es">
                            <head>
                              <title>index</title>
                            </head>
                            <body style='background-color: #65CA6E'>
                              <h1 align="center">INICIO</h1>
                              <hr><hr><hr>
                              <br><br>
                                <h3 align="center"><a href= "searchArtist"><h2>---> Search Your Artist <---</h2></a><h3>
                            </body>
                            </html>"""

        #Si se pide la página principal mandaremos el "message", si se busca un artista "message2" y cualquier otra dirección
        #lanzará un error "404 Not Found"
        if parsed_path.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(message, "utf8"))

        elif parsed_path.path == "/searchArtist":
            if parsed_path.query == "":
                #Si el usuario no ha realizado la petición de artista mostraremos un formulario
                message += " <form method=\"get\">" \
                           "<div align=\"center\">Artist Name<input type = \"text\" name = \"artist=\"></div> " \
                           "<div align=\"center\"><button type=\"submit\">Send your message</button></div>" \
                           "</form>"
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(message, "utf8"))
            elif "artist" in parsed_path.query:
                searchartist()
            else:
                #Controlamos que la dirección introducida sea correcta
                self.send_response(404)
                self.send_error(404, "Not Found")

        else:
            self.send_response(404)
            self.send_error(404, "Not Found")

        print("File served!")
        return



#Definimos el manejador con nuestra clase y lanzamos el servidor
Handler = testHTTPRequestHandler

socketserver.TCPServer.allow_reuse_address = True


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Interrumpido por el usuario")

print("")
print("Servidor parado")


