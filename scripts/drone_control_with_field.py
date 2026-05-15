# scripts/drone_control_with_field.py
import pygame
import sys
import numpy as np
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.load_environment import load_cepsim
import matplotlib
matplotlib.use('Agg')  # GUI不要モード
import matplotlib.pyplot as plt
matplotlib.rcParams['font.family'] = 'Hiragino Sans'
from datetime import datetime


# ===== 座標変換 =====
# 物理座標(メートル) ↔ 画面座標(ピクセル)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WORLD_RANGE = 20.0  # 物理空間の範囲(-10〜10)
SCALE = SCREEN_WIDTH / WORLD_RANGE  # 1m = 40ピクセル

def world_to_screen(world_pos):
    """物理座標(x, y) を画面座標(px, py) に変換"""
    px = int((world_pos[0] + WORLD_RANGE/2) * SCALE)
    py = int(SCREEN_HEIGHT - (world_pos[1] + WORLD_RANGE/2) * SCALE)
    return (px, py)


# ===== 風速場の取得 =====
def get_wind_at_position(position, positions_grid, vectors_grid):
    """現在位置に最も近いグリッド点の風速を返す(2Dなので xy のみ使用)"""
    pos_2d = np.array([position[0], position[1], 0.0])
    distances = np.linalg.norm(positions_grid - pos_2d, axis=1)
    nearest_idx = np.argmin(distances)
    return vectors_grid[nearest_idx][:2]  # xy成分のみ


# ===== 物理シミュレーション(2D版) =====
class DronePhysics:
    def __init__(self):
        self.mass = 0.5
        self.drag_coeff = 0.3
        self.thrust_strength = 10.0
        self.position = np.array([0.0, 0.0])
        self.velocity = np.array([0.0, 0.0])

    def update(self, thrust_input, wind_velocity, dt):
        force = np.array([0.0, 0.0])

        # ユーザー入力による推力
        force += thrust_input * self.thrust_strength

        # 風の力
        relative_velocity = self.velocity - wind_velocity
        force += -self.drag_coeff * relative_velocity

        # 物理更新
        acceleration = force / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt

        # 範囲制限
        for i in range(2):
            if self.position[i] < -10:
                self.position[i] = -10
                self.velocity[i] = 0
            if self.position[i] > 10:
                self.position[i] = 10
                self.velocity[i] = 0

def save_trajectory(trajectory, positions_grid, vectors_grid):
    """軌跡を画像として保存"""
    os.makedirs("imgs/plays", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"imgs/plays/play_{timestamp}.png"

    fig, ax = plt.subplots(figsize=(10, 10))

    # 風速場(z=0付近のみ、間引き)
    step = 3
    for i in range(0, len(positions_grid), step):
        if abs(positions_grid[i][2]) < 0.5:
            pos = positions_grid[i][:2]
            vec = vectors_grid[i][:2]
            ax.arrow(pos[0], pos[1], vec[0]*0.05, vec[1]*0.05,
                     head_width=0.15, color='lightsteelblue', alpha=0.5)

    # 軌跡
    trajectory_arr = np.array(trajectory)
    ax.plot(trajectory_arr[:, 0], trajectory_arr[:, 1],
            color='crimson', linewidth=2, alpha=0.8, label='軌跡')

    # 開始と終了
    ax.scatter(trajectory_arr[0, 0], trajectory_arr[0, 1],
               color='green', s=150, zorder=5, label='開始')
    ax.scatter(trajectory_arr[-1, 0], trajectory_arr[-1, 1],
               color='red', s=150, zorder=5, label='終了')

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_title(f'竜巻の中の飛行軌跡 ({timestamp})')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')

    plt.tight_layout()
    plt.savefig(filepath, dpi=150)
    plt.close()
    print(f"\n軌跡を保存しました: {filepath}")

# ===== メインループ =====
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("竜巻の中のドローン操縦 (WASD: 操縦, ESC: 終了)")
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()

    # 風速場を読み込み
    print("風速場を読み込み中...")
    metadata, positions_grid, vectors_grid = load_cepsim("data/wind_tornado.txt")
    print(f"  データ点数: {len(positions_grid)}")

    drone = DronePhysics()
    trajectory = []

    # 風速場を画面に描画する用の事前計算
    wind_arrows = []
    step = 5
    for i in range(0, len(positions_grid), step):
        if abs(positions_grid[i][2]) < 0.5:  # z=0付近のみ
            world_pos = positions_grid[i][:2]
            wind_vec = vectors_grid[i][:2]
            screen_pos = world_to_screen(world_pos)
            wind_arrows.append((screen_pos, wind_vec))

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    # Rキーでリセット
                    drone.position = np.array([0.0, 0.0])
                    drone.velocity = np.array([0.0, 0.0])
                    trajectory = []

        # キー入力
        keys = pygame.key.get_pressed()
        thrust = np.array([0.0, 0.0])
        if keys[pygame.K_w]:
            thrust[1] += 1.0
        if keys[pygame.K_s]:
            thrust[1] -= 1.0
        if keys[pygame.K_a]:
            thrust[0] -= 1.0
        if keys[pygame.K_d]:
            thrust[0] += 1.0

        # 現在位置の風速を取得
        wind = get_wind_at_position(drone.position, positions_grid, vectors_grid)

        # 物理更新
        drone.update(thrust, wind, dt)

        # 軌跡記録
        trajectory.append(drone.position.copy())
        if len(trajectory) > 300:
            trajectory.pop(0)

        # ===== 描画 =====
        screen.fill((20, 20, 40))

        # 風速場の矢印を描画
        for screen_pos, wind_vec in wind_arrows:
            scale = 5
            end_x = screen_pos[0] + int(wind_vec[0] * scale)
            end_y = screen_pos[1] - int(wind_vec[1] * scale)
            pygame.draw.line(screen, (60, 80, 120),
                             screen_pos, (end_x, end_y), 1)

        # 軌跡を描画
        if len(trajectory) > 1:
            points = [world_to_screen(p) for p in trajectory]
            pygame.draw.lines(screen, (100, 200, 255),
                              False, points, 2)

        # ドローンを描画
        screen_pos = world_to_screen(drone.position)
        pygame.draw.circle(screen, (255, 100, 100), screen_pos, 10)
        pygame.draw.circle(screen, (255, 200, 100), screen_pos, 5)

        # 速度ベクトル
        vel_end = (
            screen_pos[0] + int(drone.velocity[0] * SCALE * 0.3),
            screen_pos[1] - int(drone.velocity[1] * SCALE * 0.3)
        )
        pygame.draw.line(screen, (255, 255, 100),
                         screen_pos, vel_end, 2)

        # 風ベクトル(現在位置)
        wind_end = (
            screen_pos[0] + int(wind[0] * SCALE * 0.3),
            screen_pos[1] - int(wind[1] * SCALE * 0.3)
        )
        pygame.draw.line(screen, (100, 255, 200),
                         screen_pos, wind_end, 2)

        # 情報表示
        info_lines = [
            f"位置: ({drone.position[0]:+.1f}, {drone.position[1]:+.1f}) m",
            f"速度: ({drone.velocity[0]:+.1f}, {drone.velocity[1]:+.1f}) m/s",
            f"風速: ({wind[0]:+.1f}, {wind[1]:+.1f}) m/s",
            f"FPS: {clock.get_fps():.0f}",
            "WASD:操縦  R:リセット  ESC:終了"
        ]
        for i, line in enumerate(info_lines):
            text = font.render(line, True, (200, 200, 200))
            screen.blit(text, (10, 10 + i * 25))

        pygame.display.flip()

    # ===== 終了時に軌跡を保存 =====
    if len(trajectory) > 10:
        save_trajectory(trajectory, positions_grid, vectors_grid)

    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    main()