import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
import numpy as np

# ---------- Parametros gerais ----------
LARGO = 60.0   # comprimento (eixo X) - lado "60"
ALTO  = 40.0   # largura   (eixo Y) - lado "40" (onde os cantos devem ser arredondados)
N_DIV = 6      # numero de divisoes/piquetes
R     = 8.0    # raio de arredondamento dos cantos (nas pontas de 40m)

x0, y0 = 0.0, 0.0
x1, y1 = LARGO, ALTO

def arco(cx, cy, r, a_ini, a_fim, n=40):
    ang = np.linspace(np.radians(a_ini), np.radians(a_fim), n)
    return cx + r*np.cos(ang), cy + r*np.sin(ang)

# Contorno externo (retangulo com os 4 cantos arredondados)
xs, ys = [], []
def add(px, py):
    xs.extend(np.atleast_1d(px)); ys.extend(np.atleast_1d(py))

add(x0+R, y0)
add(x1-R, y0)
ax_, ay_ = arco(x1-R, y0+R, R, -90, 0);      add(ax_, ay_)
add(x1, y1-R)
ax_, ay_ = arco(x1-R, y1-R, R, 0, 90);       add(ax_, ay_)
add(x0+R, y1)
ax_, ay_ = arco(x0+R, y1-R, R, 90, 180);     add(ax_, ay_)
add(x0, y0+R)
ax_, ay_ = arco(x0+R, y0+R, R, 180, 270);    add(ax_, ay_)

contorno = np.array(list(zip(xs, ys)))

# ---------- Figura ----------
fig, ax = plt.subplots(figsize=(12, 8.5), dpi=200)
fig.patch.set_facecolor("#f5f1e6")
ax.set_facecolor("#f5f1e6")

# chao / area verde de fundo (pasto)
ax.add_patch(mpatches.Rectangle((x0-6, y0-6), LARGO+12, ALTO+12,
                                 facecolor="#dce8c8", edgecolor="none", zorder=0))

# cerca externa (contorno arredondado)
cerca = mpatches.Polygon(contorno, closed=True, fill=True,
                          facecolor="#e9dfc4", edgecolor="#4a3b28", linewidth=4, zorder=2)
ax.add_patch(cerca)

# divisorias internas (retas), separando os 6 piquetes
passo = LARGO / N_DIV
gate_w = 1.6   # abertura das porteiras
for k in range(1, N_DIV):
    xk = x0 + k*passo
    # porteira no meio de cada divisoria interna
    ax.plot([xk, xk], [y0, ALTO/2 - gate_w/2], color="#4a3b28", linewidth=3.5, zorder=3)
    ax.plot([xk, xk], [ALTO/2 + gate_w/2, y1], color="#4a3b28", linewidth=3.5, zorder=3)
    # simbolo da porteira (retangulo fino)
    ax.add_patch(mpatches.Rectangle((xk-0.9, ALTO/2 - gate_w/2), 1.8, gate_w,
                                     facecolor="#8a6d3b", edgecolor="#4a3b28", linewidth=1.2, zorder=4))

# numeracao dos piquetes
for k in range(N_DIV):
    cx = x0 + (k+0.5)*passo
    ax.text(cx, ALTO/2, f"{k+1}", fontsize=22, fontweight="bold",
            ha="center", va="center", color="#4a3b28", alpha=0.55, zorder=5)

# seta de fluxo do gado, contornando as pontas arredondadas
def seta_fluxo():
    # entra pelo canto inferior esquerdo, segue reto, contorna a ponta direita arredondada
    t = np.linspace(0, 1, 200)
    path_x = x0 + 4 + t*(LARGO - 8)
    path_y = np.full_like(path_x, ALTO*0.28)
    ax.plot(path_x, path_y, color="#b23b23", linewidth=2.2, linestyle=(0,(6,3)), zorder=6)
    # curva na ponta direita (contornando o arredondado) subindo para o outro corredor
    ang = np.linspace(-70, 70, 60)
    cx_, cy_ = arco(x1-R-0.5, ALTO/2, R+0.5+ (ALTO*0.28-ALTO/2)*0, 200, 200)  # placeholder unused
    curva_x, curva_y = arco(x1-6, ALTO/2, ALTO*0.22, -55, 55)
    ax.plot(curva_x, curva_y, color="#b23b23", linewidth=2.2, linestyle=(0,(6,3)), zorder=6)
    path_x2 = x0 + 4 + t*(LARGO - 8)
    path_y2 = np.full_like(path_x2, ALTO*0.72)
    ax.plot(path_x2[::-1], path_y2, color="#b23b23", linewidth=2.2, linestyle=(0,(6,3)), zorder=6)
    ax.annotate("", xy=(x0+10, ALTO*0.28), xytext=(x0+16, ALTO*0.28),
                arrowprops=dict(arrowstyle="-|>", color="#b23b23", lw=2.2), zorder=6)
    ax.annotate("", xy=(x0+16, ALTO*0.72), xytext=(x0+10, ALTO*0.72),
                arrowprops=dict(arrowstyle="-|>", color="#b23b23", lw=2.2), zorder=6)

seta_fluxo()

# cotas (dimensoes)
def cota_horizontal(y, x_ini, x_fim, texto):
    ax.annotate("", xy=(x_fim, y), xytext=(x_ini, y),
                arrowprops=dict(arrowstyle="<->", color="#222", lw=1.4))
    ax.text((x_ini+x_fim)/2, y-3.2, texto, ha="center", va="top", fontsize=13, color="#222")

def cota_vertical(x, y_ini, y_fim, texto):
    ax.annotate("", xy=(x, y_fim), xytext=(x, y_ini),
                arrowprops=dict(arrowstyle="<->", color="#222", lw=1.4))
    ax.text(x-3.0, (y_ini+y_fim)/2, texto, ha="right", va="center", fontsize=13,
            rotation=90, color="#222")

cota_horizontal(-4.5, x0, x1, "60 m")
cota_vertical(-4.5, y0, y1, "40 m")

# legenda dos cantos arredondados
ax.annotate("cantos arredondados\n(facilita o giro do gado)",
            xy=(x1-2, ALTO-2), xytext=(x1+3, ALTO+6),
            fontsize=10.5, color="#4a3b28",
            arrowprops=dict(arrowstyle="->", color="#4a3b28", lw=1.2))
ax.annotate("", xy=(x0+2, ALTO-2), xytext=(x0+3, ALTO+6),
            arrowprops=dict(arrowstyle="->", color="#4a3b28", lw=1.2))

# titulo e info da fazenda
ax.text(LARGO/2, ALTO+13, "Projeto de Mangueira — 60 m x 40 m — 6 divisões",
        ha="center", va="bottom", fontsize=17, fontweight="bold", color="#2b2210")
ax.text(LARGO/2, ALTO+9.3, "Fazenda Largo Fechado  •  Área total ≈ 1015 ha",
        ha="center", va="bottom", fontsize=11.5, color="#5a4a30")

ax.set_xlim(x0-14, x1+14)
ax.set_ylim(y0-14, y1+22)
ax.set_aspect("equal")
ax.axis("off")

plt.tight_layout()
out = "/tmp/claude-0/-home-user-Fluxograma/cde058c5-bd08-59c4-827a-76fac67e8999/scratchpad/mangueira_60x40.png"
plt.savefig(out, facecolor=fig.get_facecolor())
print("salvo em", out)
