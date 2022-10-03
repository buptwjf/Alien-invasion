import sys
# 用于游戏暂停
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien


def check_events(ai_settings, screen, stats, sb, ship, bullets, aliens, play_button):

    """响应鼠标和按键"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_key_up_events(ship, event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, ship, bullets, aliens, play_button, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, ship, bullets, aliens, play_button, mouse_x, mouse_y):
    """当玩家单击Play的时候开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏进度
        ai_settings.initialize_danamic_settings()
        # 隐藏鼠标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        # 重置记分牌
        sb.prep_score()
        sb.prep_level()
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_key_down_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    # 注意一下，这里可以用if elif，可以不用if if，即使你同时按的话，在按下键盘的话也会读出两个键
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # 向左移动飞船
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)


def check_key_up_events(ship, event):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings, screen, stats, ship, bullets, aliens, play_button, sb):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 填充颜色
    screen.fill(ai_settings.bg_color)
    # 绘制子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 确定飞船的位置
    ship.blitme()
    # 确定外星人的位置
    aliens.draw(screen)
    # 显示分数
    sb.show_score()

    # 如果游戏处于非活动状态，就制作Play按钮
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()


def fire_bullets(ai_settings, screen, ship, bullets):
    # 创—建一个子弹，并把他加入到编组bullet中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_bullets(ai_settings, screen, stats, sb, ship, bullets, aliens):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()
    # 删除已消失的子弹,在for 循环中，不应从列表或编组中删除条目，因此必须遍历编组的副本。我们使用了方法copy() 来设置for 循环，这让我们能够在循环中修改bullets 。
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        # print(len(bullets)) 测试代码
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, bullets, aliens)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, bullets, aliens):
    # 检测碰撞
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        # 遍历aliens这个数组，防止一个子弹击中多个外星人
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)
    # 如果没有外星人了，再创建一个新的外星人
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()

        # 提高等级
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """获得每行能容纳的个数"""
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    # y不需要取整
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建一个外星人群"""
    # 实例化一个外星人
    alien = Alien(ai_settings, screen)
    # 注意形参
    number_alien_x = get_number_aliens_x(ai_settings, alien.rect.width)
    # 注意形参
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # 创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可以容纳行"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height + ship_height))
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    # 为啥要加aliens.sprites()
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变它们的方向"""
    # Group只能用方法，不能用属性
    # aliens.rect.y += ai_settings.fleet_drop_speed
    for alien in aliens:
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, sb, screen, ship, bullets, aliens):
    """检查是否有外星人位于屏幕边缘，并更新整个外星人群"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船的碰撞 方法spritecollideany() 接受两个实参：一个精灵和一个编组。它检查编组是否有成员与精灵发生了碰撞，并在找到与精灵发生了碰撞的成员后就停止遍历编组。
    # ，并返回它找到的第一个与飞船发生了碰撞的外星人。
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, bullets, aliens)
        print("重启")
    check_alien_bottom(ai_settings, stats, screen, ship, bullets, aliens)


def ship_hit(ai_settings, stats, sb, screen, ship, bullets, aliens):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 将ship_left减1
        stats.ships_left -= 1
        # 更新记分牌
        sb.prep_ships()
        # 清空外星人，子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并把它放在屏幕底部中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(2)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_alien_bottom(ai_settings, stats, screen, ship, bullets, aliens):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            print("触底")
            ship_hit(ai_settings, stats, screen, ship, bullets, aliens)
            break

def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()