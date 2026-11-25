import socket
import sys


def main():
    if len(sys.argv) != 4:
        print("Uso: python nodo.py <nombre_nodo> <puerto> <reloj_inicial>")
        sys.exit(1)

    nombre = sys.argv[1]
    puerto = int(sys.argv[2])
    reloj = float(sys.argv[3])

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("127.0.0.1", puerto))
    servidor.listen(5)

    print(f"[{nombre}] Escuchando en 127.0.0.1:{puerto} | Reloj inicial: {reloj:.2f}s")

    while True:
        conexion, _ = servidor.accept()
        with conexion:
            mensaje = conexion.recv(1024).decode("utf-8").strip()

            if mensaje == "GET_TIME":
                conexion.sendall(f"{reloj}".encode("utf-8"))

            elif mensaje.startswith("ADJUST:"):
                delta = float(mensaje.split(":", 1)[1])
                reloj_anterior = reloj
                reloj += delta
                print(
                    f"[{nombre}] Ajuste recibido: {delta:+.2f}s | "
                    f"Reloj: {reloj_anterior:.2f}s -> {reloj:.2f}s"
                )
                conexion.sendall(b"OK")


if __name__ == "__main__":
    main()