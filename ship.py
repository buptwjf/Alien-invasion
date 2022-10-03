import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始位置"""
        super(Ship, self).__init__()
        # 初始化屏幕
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船图像
        self.image = pygame.image.load('images/ship.bmp')
        # 获取飞船的外接矩形
        self.rect = self.image.get_rect()
        # 获取屏幕的外接矩形
        self.screen_rect = screen.get_rect()

        # 将每艘飞船放在屏幕底部的中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)

        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """更新飞船的位置"""
        # 连续用两个if，可以保证同时按右键和左键时，飞船位置不变
        # 用center的值代替rect，因为rect只能储存整数
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.ai_settings.ship_speed_factor

        # 再根据self.center更新rect对象
        self.rect.centerx = self.center

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx
