# scripts/drone_with_wind.py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'Hiragino Sans'

def simulate_with_wind():
    """
    水平方向に風を受けて流される物体のシミュレーション
    2次元(x: 水平、z: 垂直)で考える
    """
    # 物理パラメータ
    g = 9.8           # 重力加速度
    mass = 0.5        # ドローンの質量(kg)
    drag_coeff = 0.3  # 空気抵抗係数

    # 環境パラメータ
    wind_x = 5.0      # 水平方向の風速(m/s、右向き)

    # 初期状態(x, z)
    position = np.array([0.0, 50.0])  # 高度50mから開始
    velocity = np.array([0.0, 10.0])

    # 時間設定
    dt = 0.01
    t_max = 5.0

    # 記録用
    positions_log = []

    t = 0.0
    while t < t_max and position[1] > 0:
        positions_log.append(position.copy())

        # 力を計算
        force = np.array([0.0, 0.0])

        # 重力(下向き)
        force[1] += -mass * g

        # 風の力: F = -drag × (v_drone - v_wind)
        wind_velocity = np.array([wind_x, 0.0])
        relative_velocity = velocity - wind_velocity
        wind_force = -drag_coeff * relative_velocity
        force += wind_force

        # 加速度・速度・位置の更新
        acceleration = force / mass
        velocity = velocity + acceleration * dt
        position = position + velocity * dt

        t += dt

    return np.array(positions_log)


if __name__ == "__main__":
    trajectory = simulate_with_wind()

    print(f"シミュレーション完了")
    print(f"開始位置: ({trajectory[0, 0]:.1f}, {trajectory[0, 1]:.1f})")
    print(f"終了位置: ({trajectory[-1, 0]:.1f}, {trajectory[-1, 1]:.1f})")
    print(f"水平方向の移動距離: {trajectory[-1, 0]:.1f}m")

    # 軌跡を描画
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(trajectory[:, 0], trajectory[:, 1],
            color='steelblue', linewidth=2)
    ax.scatter(trajectory[0, 0], trajectory[0, 1],
               color='green', s=100, label='開始地点', zorder=5)
    ax.scatter(trajectory[-1, 0], trajectory[-1, 1],
               color='red', s=100, label='終了地点', zorder=5)

    ax.set_xlabel('水平距離 X (m)')
    ax.set_ylabel('高度 Z (m)')
    ax.set_title('風を受けて流されるドローンの軌跡')
    ax.legend()
    ax.grid(True)
    ax.axhline(y=0, color='brown', linewidth=0.5)

    plt.tight_layout()
    plt.savefig('imgs/drone_with_wind.png', dpi=150)
    print("画像を保存しました: imgs/drone_with_wind.png")
    plt.show()