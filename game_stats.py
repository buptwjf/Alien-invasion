class GameStates:
    """跟踪统计游戏的信息"""

    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        # 这样在初始化一个对象的时候，就能直接调用reset_stats
        self.reset_stats()
        self.game_active = False
        # 在任何情况下都不能重置最高得分
        self.high_score = 0

    def reset_stats(self):
        """初始化游戏在运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
