import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.load_environment import load_cepsim

def visualize_wind(filepath, title="Wind Field"):
    # 日本語フォント設定(macOS用)
    import matplotlib
    matplotlib.rcParams['font.family'] = 'Hiragino Sans'
    metadata, positions, vectors = load_cepsim(filepath)

    step = 5
    idx = np.arange(0, len(positions), step)
    pos = positions[idx]
    vec = vectors[idx]

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.quiver(
        pos[:, 0], pos[:, 1], pos[:, 2],
        vec[:, 0], vec[:, 1], vec[:, 2],
        length=0.05,
        normalize=False,
        color='steelblue',
        alpha=0.6
    )

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f"{title}\n({metadata.get('DataKind', '')})")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("=== wind_updraft の可視化 ===")
    visualize_wind("data/wind_tornado.txt", "竜巻(wind_tornado)")
