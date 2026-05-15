# scripts/drone_control.py
import pygame
import sys
import numpy as np

# ===== 物理シミュレーション =====
class DronePhysics:
    def __init__(self):
        # 物理パラメータ
        self.g = 9.8
        self.mass = 0.5
        self.drag_coeff = 0.3
        self.thrust_strength = 15.0  # 推力の強さ

        # 状態(2D: x, z)
        self.position = np.array([400.0, 300.0])  # 画面中央
        self.velocity = np.array([0.0, 0.0])

    def update(self, thrust_input, dt):
        """
        thrust_input: 推力入力(x, z) ユーザー操縦
        dt: 時間刻み
        """
        # 力の合計
        force = np.array([0.0, 0.0])

        # 重力(画面では下向き = +z)
        force[1] += self.mass * self.g * 30  # 画面用にスケール

        # ユーザー入力による推力
        force += thrust_input * self.thrust_strength * 30

        # 空気抵抗
        force += -self.drag_coeff * self.velocity

        # 物理更新
        acceleration = force / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt

        # 画面端でバウンド
        if self.position[0] < 20:
            self.position[0] = 20
            self.velocity[0] = 0
        if self.position[0] > 780:
            self.position[0] = 780
            self.velocity[0] = 0
        if self.position[1] < 20:
            self.position[1] = 20
            self.velocity[1] = 0
        if self.position[1] > 580:
            self.position[1] = 580
            self.velocity[1] = 0


# ===== メインループ =====
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("ドローン操縦 (W/A/S/D で操縦, ESC で終了)")
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()

    drone = DronePhysics()

    # 軌跡を記録
    trajectory = []

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # 秒単位

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # キー入力で推力を決定
        keys = pygame.key.get_pressed()
        thrust = np.array([0.0, 0.0])
        if keys[pygame.K_w]:
            thrust[1] -= 1.0  # 上
        if keys[pygame.K_s]:
            thrust[1] += 1.0  # 下
        if keys[pygame.K_a]:
            thrust[0] -= 1.0  # 左
        if keys[pygame.K_d]:
            thrust[0] += 1.0  # 右

        # 物理更新
        drone.update(thrust, dt)

        # 軌跡を記録
        trajectory.append(drone.position.copy())
        if len(trajectory) > 200:
            trajectory.pop(0)

        # ===== 描画 =====
        screen.fill((20, 20, 40))  # 暗い青背景

        # 軌跡を描画
        if len(trajectory) > 1:
            points = [(int(p[0]), int(p[1])) for p in trajectory]
            pygame.draw.lines(screen, (100, 100, 200),
                              False, points, 2)

        # ドローンを描画(円)
        x, z = int(drone.position[0]), int(drone.position[1])
        pygame.draw.circle(screen, (255, 100, 100), (x, z), 15)
        pygame.draw.circle(screen, (255, 200, 100), (x, z), 8)

        # 速度ベクトル(矢印)
        vx, vz = drone.velocity
        end_x = int(x + vx * 0.5)
        end_z = int(z + vz * 0.5)
        pygame.draw.line(screen, (255, 255, 100),
                         (x, z), (end_x, end_z), 2)

        # 情報表示
        info_lines = [
            f"Position: ({drone.position[0]:.0f}, {drone.position[1]:.0f})",
            f"Velocity: ({drone.velocity[0]:.1f}, {drone.velocity[1]:.1f})",
            f"FPS: {clock.get_fps():.0f}",
            "W/A/S/D: 操縦   ESC: 終了"
        ]
        for i, line in enumerate(info_lines):
            text = font.render(line, True, (200, 200, 200))
            screen.blit(text, (10, 10 + i * 25))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()