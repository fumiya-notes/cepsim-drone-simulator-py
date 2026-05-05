# scripts/drone_3d.py
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.rcParams['font.family'] = 'Hiragino Sans'

def simulate_3d():
    """
    3次元のドローン物理シミュレーション
    一定方向の風を受けて飛ぶ
    """
    # 物理パラメータ
    g = 9.8
    mass = 0.5
    drag_coeff = 0.3

    # 環境: 3D風速ベクトル
    wind_velocity = np.array([3.0, 2.0, 0.0])  # x方向3, y方向2, z方向0

    # 初期状態(x, y, z)
    position = np.array([0.0, 0.0, 50.0])
    velocity = np.array([0.0, 0.0, 5.0])  # 上向きに5m/sの初速

    # 時間設定
    dt = 0.01
    t_max = 8.0

    # 記録用
    positions_log = []

    t = 0.0
    while t < t_max and position[2] > 0:
        positions_log.append(position.copy())

        # 力を計算
        force = np.array([0.0, 0.0, 0.0])

        # 重力(z方向のみ)
        force[2] += -mass * g

        # 風の力
        relative_velocity = velocity - wind_velocity
        wind_force = -drag_coeff * relative_velocity
        force += wind_force

        # 更新
        acceleration = force / mass
        velocity = velocity + acceleration * dt
        position = position + velocity * dt

        t += dt

    return np.array(positions_log)


if __name__ == "__main__":
    trajectory = simulate_3d()

    print(f"開始位置: {trajectory[0]}")
    print(f"終了位置: {trajectory[-1]}")

    # 3D描画
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2],
            color='steelblue', linewidth=2)
    ax.scatter(*trajectory[0], color='green', s=100,
               label='開始', zorder=5)
    ax.scatter(*trajectory[-1], color='red', s=100,
               label='終了', zorder=5)

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('3Dドローン軌跡(一定方向の風)')
    ax.legend()

    plt.tight_layout()
    plt.savefig('imgs/drone_3d.png', dpi=150)
    print("画像を保存しました: imgs/drone_3d.png")
    plt.show()