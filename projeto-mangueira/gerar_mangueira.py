import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from mangueira_lib import desenhar_mangueira

LARGO, ALTO, R = 60.0, 40.0, 8.0

fig, ax = plt.subplots(figsize=(12, 8.5), dpi=200)
fig.patch.set_facecolor("#f5f1e6")
ax.set_facecolor("#f5f1e6")

ax.add_patch(mpatches.Rectangle((-6, -6), LARGO+12, ALTO+12,
                                 facecolor="#dce8c8", edgecolor="none", zorder=0))

x0, y0, x1, y1 = desenhar_mangueira(ax, 0, 0, LARGO, ALTO, R, simples=False)

CORREDOR_H = 4.0
cy0 = ALTO/2 - CORREDOR_H/2
cy1 = ALTO/2 + CORREDOR_H/2
linha_h = ALTO/2 - CORREDOR_H/2

# seta de fluxo do gado: percorre a fileira de cima e a de baixo, e desce/sobe
# pelo portao central para o corredor de manejo
def seta(x_ini, x_fim, y, cor="#b23b23"):
    ax.annotate("", xy=(x_fim, y), xytext=(x_ini, y),
                arrowprops=dict(arrowstyle="-|>", color=cor, lw=2.0,
                                 linestyle=(0, (6, 3))))

def seta_v(x, y_ini, y_fim, cor="#b23b23"):
    ax.annotate("", xy=(x, y_fim), xytext=(x, y_ini),
                arrowprops=dict(arrowstyle="-|>", color=cor, lw=2.0,
                                 linestyle=(0, (6, 3))))

seta(4, 56, cy1 + linha_h/2)          # fileira de cima: esquerda -> direita
seta(56, 4, y0 + linha_h/2)           # fileira de baixo: direita -> esquerda
seta_v(LARGO/2, cy1 + linha_h*0.35, cy1 + 0.3)   # desce da fileira de cima p/ o corredor
seta_v(LARGO/2, y0 + linha_h*0.65, cy0 - 0.3)    # sobe da fileira de baixo p/ o corredor


# cotas
def cota_h(y, xi, xf, texto):
    ax.annotate("", xy=(xf, y), xytext=(xi, y),
                arrowprops=dict(arrowstyle="<->", color="#222", lw=1.4))
    ax.text((xi+xf)/2, y-3.2, texto, ha="center", va="top", fontsize=13, color="#222")

def cota_v(x, yi, yf, texto):
    ax.annotate("", xy=(x, yf), xytext=(x, yi),
                arrowprops=dict(arrowstyle="<->", color="#222", lw=1.4))
    ax.text(x-3.0, (yi+yf)/2, texto, ha="right", va="center", fontsize=13,
            rotation=90, color="#222")

cota_h(-4.5, x0, x1, "60 m")
cota_v(-4.5, y0, y1, "40 m")

ax.annotate("cantos arredondados\n(facilita o giro do gado)",
            xy=(x1-2, ALTO-2), xytext=(x1+3, ALTO+9),
            fontsize=10.5, color="#4a3b28",
            arrowprops=dict(arrowstyle="->", color="#4a3b28", lw=1.2))
ax.annotate("", xy=(x0+2, ALTO-2), xytext=(x0+3, ALTO+9),
            arrowprops=dict(arrowstyle="->", color="#4a3b28", lw=1.2))

ax.text(LARGO/2, ALTO+16, "Projeto de Mangueira — 60 m x 40 m — 3 divisões em cima e 3 embaixo + brete central",
        ha="center", va="bottom", fontsize=15.5, fontweight="bold", color="#2b2210")
ax.text(LARGO/2, ALTO+12.3, "Fazenda Largo Fechado  •  Área total ≈ 1015 ha",
        ha="center", va="bottom", fontsize=11.5, color="#5a4a30")

ax.set_xlim(-14, LARGO+14)
ax.set_ylim(-14, ALTO+25)
ax.set_aspect("equal")
ax.axis("off")

plt.tight_layout()
out = "/tmp/claude-0/-home-user-Fluxograma/cde058c5-bd08-59c4-827a-76fac67e8999/scratchpad/mangueira_60x40.png"
plt.savefig(out, facecolor=fig.get_facecolor())
print("salvo em", out)
