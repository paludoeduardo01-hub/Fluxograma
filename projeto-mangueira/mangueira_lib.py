import numpy as np
import matplotlib.patches as mpatches


def arco(cx, cy, r, a_ini, a_fim, n=40):
    ang = np.linspace(np.radians(a_ini), np.radians(a_fim), n)
    return cx + r*np.cos(ang), cy + r*np.sin(ang)


def contorno_arredondado(x0, y0, x1, y1, r):
    """Retorna os vertices de um retangulo com os 4 cantos arredondados."""
    xs, ys = [], []

    def add(px, py):
        xs.extend(np.atleast_1d(px)); ys.extend(np.atleast_1d(py))

    add(x0+r, y0)
    add(x1-r, y0)
    a, b = arco(x1-r, y0+r, r, -90, 0);   add(a, b)
    add(x1, y1-r)
    a, b = arco(x1-r, y1-r, r, 0, 90);    add(a, b)
    add(x0+r, y1)
    a, b = arco(x0+r, y1-r, r, 90, 180);  add(a, b)
    add(x0, y0+r)
    a, b = arco(x0+r, y0+r, r, 180, 270); add(a, b)
    return np.array(list(zip(xs, ys)))


def desenhar_mangueira(ax, ox=0.0, oy=0.0, largo=60.0, alto=40.0, r=8.0,
                        n_div=6, corredor_w=4.0, simples=False, zbase=2):
    """Desenha a mangueira (curral) em planta, com origem (ox, oy) no canto
    inferior esquerdo. Se `simples=True`, omite rotulos/cotas/setas (usado
    na vista aerea da propriedade)."""
    x0, y0 = ox, oy
    x1, y1 = ox+largo, oy+alto

    contorno = contorno_arredondado(x0, y0, x1, y1, r)
    cerca = mpatches.Polygon(contorno, closed=True, fill=True,
                              facecolor="#e9dfc4", edgecolor="#4a3b28",
                              linewidth=3 if simples else 4, zorder=zbase)
    ax.add_patch(cerca)

    # corredor central de manejo (corta do lado de baixo ao lado de cima)
    cx0 = ox + largo/2 - corredor_w/2
    cx1 = ox + largo/2 + corredor_w/2
    ax.add_patch(mpatches.Rectangle((cx0, y0), corredor_w, alto,
                                     facecolor="#c9a34e", edgecolor="#4a3b28",
                                     linewidth=2, zorder=zbase+1))
    # bretezinho (tronco de contencao) dentro do corredor
    tronco_h = alto*0.18
    ax.add_patch(mpatches.Rectangle((cx0+corredor_w*0.15, y0+alto/2-tronco_h/2),
                                     corredor_w*0.7, tronco_h,
                                     facecolor="#8a6d3b", edgecolor="#4a3b28",
                                     linewidth=1.4, zorder=zbase+2))

    # 6 piquetes: 3 de cada lado do corredor central
    lado_w = (largo/2 - corredor_w/2)
    passo = lado_w / (n_div/2)
    gate_w = alto*0.055

    def divisorias(x_ini, n):
        for k in range(1, n):
            xk = x_ini + k*passo
            ax.plot([xk, xk], [y0, y0+alto/2-gate_w/2], color="#4a3b28",
                    linewidth=2.6 if simples else 3.5, zorder=zbase+1)
            ax.plot([xk, xk], [y0+alto/2+gate_w/2, y1], color="#4a3b28",
                    linewidth=2.6 if simples else 3.5, zorder=zbase+1)

    divisorias(x0, 3)
    divisorias(x0+lado_w+corredor_w, 3)

    # portais ligando os piquetes 3 e 4 ao corredor central
    for xk, side in [(cx0, -1), (cx1, 1)]:
        ax.plot([xk, xk], [y0+alto/2-gate_w*1.6, y0+alto/2+gate_w*1.6],
                color="#8a6d3b", linewidth=5 if not simples else 3, zorder=zbase+2)

    if not simples:
        # numeracao dos piquetes
        for k in range(3):
            cxp = x0 + (k+0.5)*passo
            ax.text(cxp, oy+alto/2, f"{k+1}", fontsize=20, fontweight="bold",
                    ha="center", va="center", color="#4a3b28", alpha=0.55, zorder=zbase+3)
        for k in range(3):
            cxp = x0+lado_w+corredor_w + (k+0.5)*passo
            ax.text(cxp, oy+alto/2, f"{k+4}", fontsize=20, fontweight="bold",
                    ha="center", va="center", color="#4a3b28", alpha=0.55, zorder=zbase+3)
        ax.text(ox+largo/2, oy+alto+2.2, "Curral de manejo\n(brete central)",
                ha="center", va="bottom", fontsize=10, color="#5a4110", fontweight="bold")

    return x0, y0, x1, y1
