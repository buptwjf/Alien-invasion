import pygame
# 导入pygame.sprite中的精灵类Sprite
from pygame.sprite import Sprite


class Bullet(Sprite):
    # 继承了Sprite这个类,统一处理一系列显示对象
    """管理飞船发射子弹的类"""

    def __init__(self, ai_settings, screen, ship):
        """在飞船所处的位置创建一个子弹类的对象"""
        super(Bullet, self).__init__()
        # super 使子类继承了父类的__init__，也就是父类的所有属性，父类也称超类
        self.screen = screen
        self.ship = ship

        # 在(0,0)处创建一个表示子弹的矩形，再设计正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = self.ship.rect.top

        # 存储用小数表示的子弹的位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        # 更新表示子弹位置的小数值
        self.y -= self.speed_factor
        # 更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
