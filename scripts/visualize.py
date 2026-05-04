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

def visualize_all(titles=None):
    """
    4種類の環境データを2×2で並べて表示する
    """
    import matplotlib
    matplotlib.rcParams['font.family'] = 'Hiragino Sans'

    files = [
        ("data/wind_updraft.txt",  "上昇気流"),
        ("data/wind_tornado.txt",  "竜巻"),
        ("data/wind_random.txt",   "ランダムな風"),
        ("data/my_tornado.txt",    "自作竜巻"),
    ]

    fig = plt.figure(figsize=(14, 10))
    fig.suptitle("CEPSim 風速場サンプル集", fontsize=14)

    for i, (filepath, title) in enumerate(files):
        metadata, positions, vectors = load_cepsim(filepath)

        # 間引き
        step = 8
        idx = np.arange(0, len(positions), step)
        pos = positions[idx]
        vec = vectors[idx]

        ax = fig.add_subplot(2, 2, i+1, projection='3d')
        ax.quiver(
            pos[:, 0], pos[:, 1], pos[:, 2],
            vec[:, 0], vec[:, 1], vec[:, 2],
            length=0.05,
            normalize=False,
            color='steelblue',
            alpha=0.6
        )
        ax.set_title(title)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_zlim(-1, 11)  # 全グラフでz軸範囲を統一

    plt.tight_layout()
    plt.savefig("data/wind_comparison.png", dpi=150)
    print("画像を保存しました: data/wind_comparison.png")
    plt.show()

if __name__ == "__main__":
    visualize_all()
