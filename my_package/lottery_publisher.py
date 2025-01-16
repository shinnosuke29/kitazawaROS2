import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import random

class LotteryPublisher(Node):
    def __init__(self):
        super().__init__('lottery_publisher')
        self.publisher_ = self.create_publisher(String, 'lottery', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)  # 1秒ごとに実行
        self.lucky_items = [
            "赤いペン",
            "お気に入りの本",
            "猫の写真",
            "青いスカーフ",
            "星型のアクセサリー",
            "観葉植物",
            "チョコレート",
            "暖かいコーヒー",
            "イヤホン",
            "黄色いハンカチ",
            "漫画4巻",
            "ネズミのキャラクターストラップ",
        ]
        self.previous_lucky_item = None  # 前回のラッキーアイテム
        self.count = 0  # 試行回数のカウンタ

    def timer_callback(self):
        self.count += 1  # 試行回数をインクリメント
        msg = String()

        # 300回に1回は強制的に当たりにする
        if self.count % 300 == 0:
            number = 1
        else:
            number = random.randint(1, 300)

        if number == 1:  # 当たり
            self.count = 0  # 試行回数をリセット
            if random.random() < 0.5:  # 50%の確率でラッキーアイテムを表示
                lucky_item = random.choice(self.lucky_items)
                self.previous_lucky_item = lucky_item  # ラッキーアイテムを記憶
                msg.data = f"当たり！おめでとう！今日のラッキーアイテムは「{lucky_item}」です！ ({self.count}回目)"
            else:  # 50%の確率で「惜しい」
                if self.previous_lucky_item:
                    msg.data = f"惜しい！また頑張って！前回のラッキーアイテムは「{self.previous_lucky_item}」でした！ ({self.count}回目)"
                else:
                    msg.data = f"惜しい！また頑張って！ ({self.count}回目)"
        else:  # ハズレ
            msg.data = f"ハズレ ({self.count}回目)"
        
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')  # ログに出力

def main(args=None):
    rclpy.init(args=args)
    node = LotteryPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
