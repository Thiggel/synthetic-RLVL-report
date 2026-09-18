import matplotlib, sys
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np
fd = sys.argv[1]
for w in ("Regular","Medium","SemiBold"):
    fm.fontManager.addfont(f"{fd}/Inter-{w}.ttf")
plt.rcParams.update({"font.family":"Inter","font.size":8,"axes.edgecolor":"#555","axes.linewidth":0.6,
                     "xtick.color":"#333","ytick.color":"#333","pdf.fonttype":42})
labels=["ProofWriter d3","FOLIO","BBH-chain","GPQA-quant","BranchProof"]
ctrl=[39.3,51.4,62.2,22.8,0.3]; formal=[50.0,57.8,67.6,27.9,99.3]; eng=[53.2,55.0,66.4,30.1,100.0]
cols={"ctrl":"#bdbdbd","formal":"#a8dcb0","eng":"#f5b98f"}
edge={"ctrl":"#8a8a8a","formal":"#5aa86a","eng":"#d98a52"}
fig,ax=plt.subplots(figsize=(2.35,3.55))
y=np.arange(len(labels))[::-1]; h=0.26
for i,(k,v) in enumerate([("ctrl",ctrl),("formal",formal),("eng",eng)]):
    yy=y+(1-i)*h
    ax.barh(yy,v,height=h,color=cols[k],edgecolor=edge[k],linewidth=0.5,zorder=3)
    for yi,vi in zip(yy,v):
        ax.text(vi+1.5,yi,f"{vi:.1f}",va="center",ha="left",fontsize=6.2,color="#333")
ax.set_yticks(y); ax.set_yticklabels(labels,fontsize=7.5)
ax.set_xlim(0,118); ax.set_xticks([0,25,50,75,100]); ax.tick_params(axis="x",labelsize=7,length=2.5)
ax.tick_params(axis="y",length=0)
ax.set_xlabel("accuracy (%)",fontsize=7.5)
ax.grid(axis="x",color="#e6e6e6",linewidth=0.5,zorder=0)
for s in ("top","right"): ax.spines[s].set_visible(False)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor=cols["ctrl"],edgecolor=edge["ctrl"],label="Control"),
                   Patch(facecolor=cols["formal"],edgecolor=edge["formal"],label="Formal 5%"),
                   Patch(facecolor=cols["eng"],edgecolor=edge["eng"],label="English 10%")],
          fontsize=6.5,frameon=False,loc="lower center",bbox_to_anchor=(0.42,1.0),ncol=3,columnspacing=0.8,handlelength=1.0,handletextpad=0.4)
fig.tight_layout(pad=0.3)
fig.savefig("figures/headline.pdf")
