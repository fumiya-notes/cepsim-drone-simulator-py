# scripts/drone_in_field.py
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.rcParams['font.family'] = 'Hiragino Sans'

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.load_environment import load_cepsim


def get_wind_at_position(position, positions_grid, vectors_grid):
    """
    現在位置に最も近いグリッド点の風速を返す
    (簡易版: 最近傍探索)
    """
    distances = np.linalg.norm(positions_grid - position, axis=1)
    nearest_idx = np.argmin(distances)
    return vectors_grid[nearest_idx]


def simulate_in_field(env_filepath, initial_position, initial_velocity):
    """
    CEPSim形式の風速場の中でドローンを飛ばす
    """
    # 風速場を読み込み
    metadata, positions_grid, vectors_grid = load_cepsim(env_filepath)
    print(f"風速場を読み込み: {env_filepath}")
    print(f"  データ点数: {len(positions_grid)}")

    # 物理パラメータ
    g = 9.8
    mass = 0.5
    drag_coeff = 0.3

    # 初期状態
    position = np.array(initial_position, dtype=float)
    velocity = np.array(initial_velocity, dtype=float)

    # 時間設定
    dt = 0.01
    t_max = 10.0

    # 記録用
    positions_log = []

    t = 0.0
    while t < t_max and position[2] > 0:
        positions_log.append(position.copy())

        # 力を計算
        force = np.array([0.0, 0.0, 0.0])

        # 重力
        force[2] += -mass * g

        # 風の力(現在位置の風速を取得)
        wind_velocity = get_wind_at_position(
            position, positions_grid, vectors_grid)
        relative_velocity = velocity - wind_velocity
        wind_force = -drag_coeff * relative_velocity
        force += wind_force

        # 更新
        acceleration = force / mass
        velocity = velocity + acceleration * dt
        position = position + velocity * dt

        t += dt

    return np.array(positions_log), positions_grid, vectors_grid


def visualize_field_and_trajectory(trajectory, positions_grid, vectors_grid, title):
    """
    風速場とドローンの軌跡を一緒に描画
    """
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    # 風速場(間引き)
    step = 15
    idx = np.arange(0, len(positions_grid), step)
    pos = positions_grid[idx]
    vec = vectors_grid[idx]

    ax.quiver(
        pos[:, 0], pos[:, 1], pos[:, 2],
        vec[:, 0], vec[:, 1], vec[:, 2],
        length=0.05, normalize=False,
        color='lightsteelblue', alpha=0.4
    )

    # ドローンの軌跡
    ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2],
            color='crimson', linewidth=2.5, label='ドローン軌跡')
    ax.scatter(*trajectory[0], color='green', s=150,
               label='開始', zorder=5)
    ax.scatter(*trajectory[-1], color='red', s=150,
               label='終了', zorder=5)

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title(title)
    ax.legend()

    return fig


if __name__ == "__main__":
    # 竜巻の中にドローンを置く
    trajectory, pos_grid, vec_grid = simulate_in_field(
        env_filepath="data/wind_tornado.txt",
        initial_position=[3.0, 0.0, 8.0],
        initial_velocity=[0.0, 0.0, 5.0]
    )

    print(f"開始位置: {trajectory[0]}")
    print(f"終了位置: {trajectory[-1]}")

    fig = visualize_field_and_trajectory(
        trajectory, pos_grid, vec_grid,
        title="竜巻の中のドローン軌跡"
    )

    plt.tight_layout()
    plt.savefig('imgs/drone_in_tornado.png', dpi=150)
    print("画像を保存しました: imgs/drone_in_tornado.png")
    plt.show()