import socket
import sys


def consultar_hora(puerto: int) -> float:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.settimeout(5.0)
        cliente.connect(("127.0.0.1", puerto))
        cliente.sendall(b"GET_TIME")
        respuesta = cliente.recv(1024).decode("utf-8").strip()
        return float(respuesta)


def enviar_ajuste(puerto: int, delta: float) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.settimeout(5.0)
        cliente.connect(("127.0.0.1", puerto))
        cliente.sendall(f"ADJUST:{delta}".encode("utf-8"))
        cliente.recv(1024)


def main():
    if len(sys.argv) != 5:
        print("Uso: python coordinador.py <reloj_coord> <puerto_nodo2> <puerto_nodo3> <umbral_max>")
        sys.exit(1)

    reloj_coord = float(sys.argv[1])
    puerto_nodo2 = int(sys.argv[2])
    puerto_nodo3 = int(sys.argv[3])
    umbral_max = float(sys.argv[4])

    nodos = [
        {"nombre": "Coordinador (PC1)", "puerto": None, "hora": reloj_coord},
        {"nombre": "Nodo 2 (PC2)", "puerto": puerto_nodo2, "hora": consultar_hora(puerto_nodo2)},
        {"nombre": "Nodo 3 (PC3)", "puerto": puerto_nodo3, "hora": consultar_hora(puerto_nodo3)},
    ]

    print("\n--- Horas leídas ---")
    for n in nodos:
        n["diff"] = n["hora"] - reloj_coord
        n["valido"] = abs(n["diff"]) <= umbral_max
        estado = "OK" if n["valido"] else "DESCARTADO (fuera de umbral)"
        print(f"{n['nombre']}: reloj={n['hora']:.2f}s | diff={n['diff']:+.2f}s | {estado}")

    validos = [n["diff"] for n in nodos if n["valido"]]
    delta_promedio = sum(validos) / len(validos)

    print(f"\nDelta promedio (sobre {len(validos)} nodos válidos): {delta_promedio:+.2f}s")
    print("--- Aplicando ajustes ---")

    for n in nodos:
        if not n["valido"]:
            print(f"{n['nombre']}: no se ajusta por estar descartado.")
            continue

        ajuste = delta_promedio - n["diff"]
        if n["puerto"] is None:
            reloj_nuevo = reloj_coord + ajuste
            print(
                f"{n['nombre']}: ajuste={ajuste:+.2f}s | "
                f"Reloj: {reloj_coord:.2f}s -> {reloj_nuevo:.2f}s"
            )
            reloj_coord = reloj_nuevo
        else:
            enviar_ajuste(n["puerto"], ajuste)


if __name__ == "__main__":
    main()