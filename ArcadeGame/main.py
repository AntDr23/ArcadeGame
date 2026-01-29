import arcade

SPEED = 4
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Leonardo Game"
TILE_SCALING = 0.5
JUMP = 5


class GridGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.all_sprites = None
        self.wall_sprites = None
        self.player = None
        self.player_texture = arcade.load_texture(":resources:images/animated_characters/female_person/femalePerson_idle.png")

        self.world_camera = arcade.camera.Camera2D()  # Камера для игрового мира
        self.gui_camera = arcade.camera.Camera2D()

        self.world_width = SCREEN_WIDTH
        self.world_height = SCREEN_HEIGHT

    def setup(self):
        self.all_sprites = arcade.SpriteList()
        self.player = arcade.Sprite(self.player_texture, scale=0.5)
        self.player.position = (126, 256)
        self.all_sprites.append(self.player)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_sprites)
        self.player.change_x = 0
        self.player.change_y = 0
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        map_name = "безымянный.tmx"
        # Параметр 'scaling' ОЧЕНЬ важен! Умножает размер каждого тайла
        tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)

        # --- Достаём слои из карты как спрайт-листы ---
        # Слой "walls" (стены) — просто для отрисовки
        self.wall_list = tile_map.sprite_lists["walls"]
        # Слой "chests" (сундуки) — красота!
        self.coins_list = tile_map.sprite_lists["coins"]
        # Слой "exit" (выходы с уровня) — красота!
        self.exit_list = tile_map.sprite_lists["door closed"]
        # САМЫЙ ГЛАВНЫЙ СЛОЙ: "Collision" — наши стены и платформы для физики!
        self.collision_list = tile_map.sprite_lists["collision"]
        # --- Создаём игрока ---
        # Карту загрузили, теперь создаём героя, который будет по ней бегать

        # --- Физический движок ---
        # Используем PhysicsEngineSimple, который знаем и любим
        # Он даст нам движение и коллизии со стенами (self.wall_list)!
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.collision_list
        )

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.all_sprites.draw()
        self.wall_list.draw()
        self.coins_list.draw()
        self.exit_list.draw()
        self.player_list.draw()
        self.gui_camera.use()

    def on_update(self, delta_time):
        self.player.center_x += self.player.change_x * SPEED * delta_time * 60
        self.player.center_y += self.player.change_y * SPEED * delta_time * 60

        position = (
            self.player.center_x,
            self.player.center_y
        )
        self.world_camera.position = arcade.math.lerp_2d(  # Изменяем позицию камеры
            self.world_camera.position,
            position,
            0.15,
        )
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -1
        elif key == arcade.key.RIGHT:
            self.player.change_x = 1
        elif key == arcade.key.UP:
            self.player.change_y = 1
        elif key == arcade.key.DOWN:
            self.player.change_y = -1

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0


def setup_game(width=960, height=640, title="Leonardo Game"):
    game = GridGame(width, height, title)
    game.setup()
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()