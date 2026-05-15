# scripts/pygame_test.py
import pygame
import sys

def main():
    # pygame初期化
    pygame.init()

    # ウィンドウ作成(800x600)
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("pygame テスト")

    # フォント(キー入力表示用)
    font = pygame.font.Font(None, 36)

    # 時計(60fps制御)
    clock = pygame.time.Clock()

    # 現在押されているキーの記録
    pressed_keys = []

    # メインループ
    running = True
    while running:
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # 押されたキーを記録
                key_name = pygame.key.name(event.key)
                pressed_keys.append(key_name)
                if len(pressed_keys) > 10:
                    pressed_keys.pop(0)

                # ESCキーで終了
                if event.key == pygame.K_ESCAPE:
                    running = False

        # 画面を黒で塗りつぶし
        screen.fill((0, 0, 0))

        # タイトルを描画
        title = font.render("Press any key (ESC to quit)",
                            True, (255, 255, 255))
        screen.blit(title, (50, 50))

        # 押されたキーを表示
        y = 100
        for key in pressed_keys:
            text = font.render(f"Pressed: {key}",
                               True, (100, 200, 255))
            screen.blit(text, (50, y))
            y += 40

        # 画面更新
        pygame.display.flip()

        # 60fps制御
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()