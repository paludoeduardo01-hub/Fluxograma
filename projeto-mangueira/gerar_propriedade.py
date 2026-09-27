import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from mangueira_lib import desenhar_mangueira

rng = np.random.default_rng(7)

fig, ax = plt.subplots(figsize=(13, 9), dpi=200)
fig.patch.set_facecolor("#eef2e4")
ax.set_facecolor("#eef2e4")

W, H = 180.0, 120.0

# pasto de fundo
ax.add_patch(mpatches.Rectangle((-10, -10), W+20, H+20,
                                 facecolor="#cfe0ac", edgecolor="none", zorder=0))
# textura leve de pasto (listras)
for i in range(-10, int(W)+10, 6):
    ax.plot([i, i-25], [-10, H+10], color="#c3d69c", linewidth=10, alpha=0.35, zorder=0)

# cerca da sede (area do conjunto casa + pomar + mangueira)
sede = mpatches.FancyBboxPatch((2, 2), W-4, H-4,
                                boxstyle="round,pad=0,rounding_size=3",
                                fill=False, edgecolor="#5a4a30", linewidth=2.5,
                                linestyle=(0, (10, 4)), zorder=1)
ax.add_patch(sede)
ax.text(6, H-2, "Sede da propriedade (ilustrativo) — Fazenda Largo Fechado, ≈1015 ha",
        fontsize=10, color="#5a4a30", va="bottom")

# ---------------- CASA ----------------
casa_x, casa_y, casa_w, casa_h = 14, 82, 22, 16
ax.add_patch(mpatches.Rectangle((casa_x-2.5, casa_y-2.5), casa_w+5, casa_h+5,
                                 facecolor="#e4d9b0", edgecolor="none", zorder=1.5))  # quintal
ax.add_patch(mpatches.Rectangle((casa_x, casa_y), casa_w, casa_h,
                                 facecolor="#c1543a", edgecolor="#5a2a1c", linewidth=2, zorder=2))
ax.plot([casa_x, casa_x+casa_w], [casa_y+casa_h/2, casa_y+casa_h/2],
        color="#5a2a1c", linewidth=1.6, zorder=3)  # cumeeira do telhado
ax.add_patch(mpatches.Rectangle((casa_x+casa_w*0.62, casa_y+casa_h*0.15),
                                 casa_w*0.12, casa_h*0.12,
                                 facecolor="#7a7a7a", edgecolor="#4a4a4a", zorder=3))  # chamine
ax.text(casa_x+casa_w/2, casa_y-3.5, "Casa", ha="center", va="top",
        fontsize=12, fontweight="bold", color="#3a2a15")

# ---------------- POMAR ----------------
pom_x0, pom_y0, pom_x1, pom_y1 = 10, 22, 62, 68
ax.add_patch(mpatches.Rectangle((pom_x0-2, pom_y0-2), (pom_x1-pom_x0)+4, (pom_y1-pom_y0)+4,
                                 facecolor="#d9e8bd",
                                 edgecolor="#7a8f52", linewidth=1.8, linestyle="--", zorder=1))
cols = np.arange(pom_x0+4, pom_x1-2, 7.0)
rows = np.arange(pom_y0+4, pom_y1-2, 7.0)
for cy in rows:
    for cx in cols:
        jitter_x = rng.uniform(-0.6, 0.6)
        jitter_y = rng.uniform(-0.6, 0.6)
        r = rng.uniform(2.3, 2.9)
        ax.add_patch(plt.Circle((cx+jitter_x, cy+jitter_y), r,
                                 facecolor="#5f9a4a",
                                 edgecolor="#3f6b30", linewidth=0.8, zorder=2))
        ax.add_patch(plt.Circle((cx+jitter_x, cy+jitter_y), r*0.18,
                                 facecolor="#4a3320", edgecolor="none", zorder=2.1))
ax.text((pom_x0+pom_x1)/2, pom_y1+3.5, "Pomar", ha="center", va="bottom",
        fontsize=12, fontweight="bold", color="#3a5a25")

# ---------------- MANGUEIRA ----------------
mx0, my0 = 96, 18
desenhar_mangueira(ax, mx0, my0, 60, 40, 8.0, simples=True)
ax.text(mx0+30, my0-5.5, "Mangueira (curral de manejo)", ha="center", va="top",
        fontsize=12, fontweight="bold", color="#3a2a15")

# ---------------- ESTRADA INTERNA ----------------
estrada_x = [casa_x+casa_w+2, casa_x+casa_w+2, mx0+30, mx0+30]
estrada_y = [casa_y, 50, 50, my0+40]
ax.plot(estrada_x, estrada_y, color="#a9895a", linewidth=6, solid_capstyle="round",
        zorder=1.2, alpha=0.9)
ax.plot(estrada_x, estrada_y, color="#c9ac78", linewidth=2.2, linestyle=(0, (3, 3)),
        zorder=1.3)

# ---------------- ROSA DOS VENTOS ----------------
nx, ny = W-14, H-18
ax.annotate("", xy=(nx, ny+8), xytext=(nx, ny-8),
            arrowprops=dict(arrowstyle="-|>", color="#3a2a15", lw=2))
ax.text(nx, ny+10, "N", ha="center", va="bottom", fontsize=13, fontweight="bold",
        color="#3a2a15")

# titulo
ax.text(W/2, H+9, "Vista aérea esquemática da propriedade",
        ha="center", va="bottom", fontsize=18, fontweight="bold", color="#2b2210")
ax.text(W/2, H+4.5, "Casa + pomar + mangueira (60 m x 40 m, 6 divisões + brete central)",
        ha="center", va="bottom", fontsize=11.5, color="#5a4a30")

ax.set_xlim(-8, W+8)
ax.set_ylim(-8, H+16)
ax.set_aspect("equal")
ax.axis("off")

plt.tight_layout()
out = "/tmp/claude-0/-home-user-Fluxograma/cde058c5-bd08-59c4-827a-76fac67e8999/scratchpad/propriedade_aerea.png"
plt.savefig(out, facecolor=fig.get_facecolor())
print("salvo em", out)
