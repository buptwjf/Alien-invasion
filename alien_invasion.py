import pygame
from pygame.sprite import Group

# 引用settings的中的Settings变量
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStates
from button import Button
from scoreboard import Scoreboard


# 注意格式空两行
def run_game():
    pygame.init()
    # 创建一个Setting s的对象
    ai_settings = Settings()
    # 设置屏幕
    screen = pygame.display.set_mode([ai_settings.screen_width, ai_settings.screen_height])
    # 设置标题
    pygame.display.set_caption("Alien Invasion")
    # 创建PLAY按钮
    play_button = Button(ai_settings, screen, "Play")
    # 创建一个用于存储游戏统计信息的实例
    # 一定要有形参，多次查看声明找bug
    stats = GameStates(ai_settings)
    # 创建记分牌
    sb = Scoreboard(ai_settings, screen, stats)
    # 创建一个飞船
    ship = Ship(ai_settings, screen)
    # 创建一个用于存储子弹的数组，这样更新子弹的话会对组里的每一个子弹更新
    bullets = Group()
    # 创建一个用于存储外星人数组，这样更新外星人的话会对组里的每一个外星人更新
    aliens = Group()
    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 开始主循环，监视键盘和鼠标
    while True:
        # 响应事件及按钮
        gf.check_events(ai_settings, screen, stats, sb, ship, bullets, aliens, play_button)
        if stats.game_active:
            # 更新飞船
            ship.update()
            # 更新子弹
            gf.update_bullets(ai_settings, screen, stats, sb, ship, bullets, aliens)
            gf.update_aliens(ai_settings, stats, sb, screen, ship, bullets, aliens)
            # 更新屏幕上的图像
        gf.update_screen(ai_settings, screen, stats, ship, bullets, aliens, play_button, sb)


# 注意格式空两行
run_game()
