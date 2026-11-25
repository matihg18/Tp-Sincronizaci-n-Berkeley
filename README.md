# Sincronización de Relojes con el Algoritmo de Berkeley (3 Nodos)

Implementación del **algoritmo de Berkeley** para sincronizar los relojes de **3 computadoras** en un sistema distribuido mediante sockets TCP en Python, sin depender de una fuente de tiempo externa.

## Funcionamiento

- **Coordinador (`coordinador.py`):** consulta los relojes mediante `GET_TIME`, calcula las diferencias relativas respecto a su propio reloj, filtra desfases que superan un umbral máximo, calcula el promedio de las diferencias válidas y envía el ajuste correspondiente (`ADJUST:<delta>`).
- **Nodos (`nodo.py`):** escuchan en un puerto TCP local, mantienen un reloj simulado, responden su hora actual ante `GET_TIME` y aplican el ajuste recibido ante `ADJUST:<delta>`.

### Cálculo de deltas y ajustes

- Diferencia respecto al coordinador: $\Delta_i = t_i - t_{\text{coord}}$
- Promedio de diferencias válidas ($\vert{}\Delta_i\vert{} \le \text{umbral}$): $\Delta_{\text{prom}} = \frac{\sum \Delta_{\text{válidos}}}{N_{\text{válidos}}}$
- Ajuste para cada nodo válido: $\text{ajuste}_i = \Delta_{\text{prom}} - \Delta_i$

## Ejecución (3 terminales)

1. **Nodo 2:**

```bash
python nodo.py Nodo2 5001 105
```

2. **Nodo 3:**

```bash
python nodo.py Nodo3 5002 95
```

3. **Coordinador:**

```bash
python coordinador.py 100 5001 5002 50
```

## Salida obtenida

```text
--- Horas leídas ---
Coordinador (PC1): reloj=100.00s | diff=+0.00s | OK
Nodo 2 (PC2): reloj=105.00s | diff=+5.00s | OK
Nodo 3 (PC3): reloj=95.00s | diff=-5.00s | OK

Delta promedio (sobre 3 nodos válidos): +0.00s
--- Aplicando ajustes ---
Coordinador (PC1): ajuste=+0.00s | Reloj: 100.00s -> 100.00s
```