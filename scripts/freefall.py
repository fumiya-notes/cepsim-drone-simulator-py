# scripts/freefall.py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'Hiragino Sans'

def freefall_simulation():
    """
    1次元の自由落下シミュレーション
    高さ100mから物体を落とす
    """
    # 物理パラメータ
    g = 9.8           # 重力加速度(m/s²)
    mass = 1.0        # 質量(kg)

    # 初期状態
    position = 100.0  # 初期高度(m)
    velocity = 0.0    # 初期速度(m/s)

    # 時間設定
    dt = 0.01         # 時間刻み(秒)
    t_max = 5.0       # シミュレーション時間(秒)

    # 結果を記録するリスト
    times = []
    positions = []
    velocities = []

    # シミュレーションループ
    t = 0.0
    while t < t_max and position > 0:
        # 記録
        times.append(t)
        positions.append(position)
        velocities.append(velocity)

        # 物理計算: F = ma → a = F/m = g
        acceleration = -g  # 下向きなのでマイナス

        # 速度と位置を更新(オイラー法)
        velocity = velocity + acceleration * dt
        position = position + velocity * dt

        # 時間を進める
        t += dt

    return np.array(times), np.array(positions), np.array(velocities)


if __name__ == "__main__":
    times, positions, velocities = freefall_simulation()

    # 結果を表示
    print(f"シミュレーション時間: {times[-1]:.2f}秒")
    print(f"最終位置: {positions[-1]:.2f}m")
    print(f"最終速度: {velocities[-1]:.2f}m/s")

    # グラフ描画
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(times, positions, color='steelblue')
    axes[0].set_xlabel('時間 (秒)')
    axes[0].set_ylabel('高度 (m)')
    axes[0].set_title('自由落下: 高度の変化')
    axes[0].grid(True)

    axes[1].plot(times, velocities, color='crimson')
    axes[1].set_xlabel('時間 (秒)')
    axes[1].set_ylabel('速度 (m/s)')
    axes[1].set_title('自由落下: 速度の変化')
    axes[1].grid(True)

    plt.tight_layout()
    plt.savefig('imgs/freefall.png', dpi=150)
    print("画像を保存しました: imgs/freefall.png")
    plt.show()