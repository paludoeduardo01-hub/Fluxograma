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
                        n_div=6, corredor_h=4.0, simples=False, zbase=2):
    """Desenha a mangueira (curral) em planta, com origem (ox, oy) no canto
    inferior esquerdo. O corredor central de manejo e horizontal, cortando
    a mangueira de um lado ao outro e deixando 3 piquetes em cima e 3
    embaixo. Se `simples=True`, omite rotulos/cotas/setas (usado na vista
    aerea da propriedade)."""
    x0, y0 = ox, oy
    x1, y1 = ox+largo, oy+alto

    contorno = contorno_arredondado(x0, y0, x1, y1, r)
    cerca = mpatches.Polygon(contorno, closed=True, fill=True,
                              facecolor="#e9dfc4", edgecolor="#4a3b28",
                              linewidth=3 if simples else 4, zorder=zbase)
    ax.add_patch(cerca)

    # corredor central de manejo (corta da esquerda a direita)
    cy0 = oy + alto/2 - corredor_h/2
    cy1 = oy + alto/2 + corredor_h/2
    ax.add_patch(mpatches.Rectangle((x0, cy0), largo, corredor_h,
                                     facecolor="#c9a34e", edgecolor="#4a3b28",
                                     linewidth=2, zorder=zbase+1))
    # bretezinho (tronco de contencao) dentro do corredor
    tronco_w = largo*0.12
    ax.add_patch(mpatches.Rectangle((ox+largo/2-tronco_w/2, cy0+corredor_h*0.15),
                                     tronco_w, corredor_h*0.7,
                                     facecolor="#8a6d3b", edgecolor="#4a3b28",
                                     linewidth=1.4, zorder=zbase+2))

    # 6 piquetes: 3 em cima e 3 embaixo do corredor central
    linha_h = (alto/2 - corredor_h/2)
    passo = largo / (n_div/2)
    gate_w = largo*0.045

    def divisorias_linha(y_ini, y_fim, n):
        for k in range(1, n):
            xk = x0 + k*passo
            ax.plot([xk, xk], [y_ini, y_fim], color="#4a3b28",
                    linewidth=2.6 if simples else 3.5, zorder=zbase+1)

    divisorias_linha(y0, cy0, 3)          # linha de baixo
    divisorias_linha(cy1, y1, 3)          # linha de cima

    # portais ligando cada piquete ao corredor central (um por piquete)
    for k in range(3):
        xk = x0 + (k+0.5)*passo
        ax.plot([xk-gate_w, xk+gate_w], [cy0, cy0],
                color="#8a6d3b", linewidth=5 if not simples else 3, zorder=zbase+2)
        ax.plot([xk-gate_w, xk+gate_w], [cy1, cy1],
                color="#8a6d3b", linewidth=5 if not simples else 3, zorder=zbase+2)

    if not simples:
        # numeracao dos piquetes: 1-3 em cima (esq->dir), 4-6 embaixo (esq->dir)
        for k in range(3):
            cxp = x0 + (k+0.5)*passo
            ax.text(cxp, cy1+linha_h/2, f"{k+1}", fontsize=20, fontweight="bold",
                    ha="center", va="center", color="#4a3b28", alpha=0.55, zorder=zbase+3)
        for k in range(3):
            cxp = x0 + (k+0.5)*passo
            ax.text(cxp, y0+linha_h/2, f"{k+4}", fontsize=20, fontweight="bold",
                    ha="center", va="center", color="#4a3b28", alpha=0.55, zorder=zbase+3)
        ax.text(ox+largo+2.5, oy+alto/2, "Curral de manejo\n(brete central)",
                ha="left", va="center", fontsize=10, color="#5a4110", fontweight="bold")

    return x0, y0, x1, y1
