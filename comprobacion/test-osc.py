from pythonosc import dispatcher, osc_server

def print_handler(address, *args):
    print(f"{address}: {args}")

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/track/*", print_handler)

server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 9000), dispatcher)
print("Esperando datos OSC en el puerto 8000...")
server.serve_forever()
