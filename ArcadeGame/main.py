import arcade

SPEED = 4
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Leonardo Game"
TILE_SCALING = 0.5
PLAYER_JUMP = 22
GRAVITY = 1


class GridGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.all_sprites = None
        self.wall_sprites = None
        self.player = None
        self.game_win = False
        self.score = 0
        self.door_open = False
        self.show_key_message = False
        self.key_message_timer = 1.5
        self.player_texture = arcade.load_texture(":resources:images/animated_characters/female_person/femalePerson_idle.png")

        self.world_camera = arcade.camera.Camera2D()  # Камера для игрового мира
        self.gui_camera = arcade.camera.Camera2D()

        self.world_width = SCREEN_WIDTH
        self.world_height = SCREEN_HEIGHT

        arcade.set_background_color(arcade.color.SKY_BLUE)

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
        tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)

        self.wall_list = tile_map.sprite_lists["walls"]
        self.coins_list = tile_map.sprite_lists["coins"]
        self.decor_list = tile_map.sprite_lists["decor"]
        self.diamond_list = tile_map.sprite_lists["diamonds"]
        self.keys_list = tile_map.sprite_lists["keys"]
        self.exit_list = tile_map.sprite_lists["door closed"]
        self.open_list = tile_map.sprite_lists["door opened"]
        self.collision_list = tile_map.sprite_lists["collision"]
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            self.collision_list,
            gravity_constant=GRAVITY
        )

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.all_sprites.draw()
        self.wall_list.draw()
        self.coins_list.draw()
        self.decor_list.draw()
        self.diamond_list.draw()
        self.keys_list.draw()
        self.open_list.draw()
        self.exit_list.draw()
        self.player_list.draw()
        self.gui_camera.use()

        arcade.draw_text(
            f"Монетки: {self.score}",
            10,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            24,
            font_name="Arial"
        )

        if self.game_win:
            arcade.draw_text(
                "ПОБЕДА!",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 30,
                arcade.color.GOLD,
                48,
                anchor_x="center",
                anchor_y="center",
                font_name="Arial"
            )

        if self.show_key_message:
            arcade.draw_text(
                "Ключ найден!",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 100,
                arcade.color.GOLD,
                48,
                anchor_x="center",
                anchor_y="center",
                font_name="Arial",
                bold=True
            )

    def on_update(self, delta_time):
        self.player.center_x += self.player.change_x * SPEED * delta_time * 60

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

        coins_hit = arcade.check_for_collision_with_list(self.player, self.coins_list)
        for coins in coins_hit:
            coins.remove_from_sprite_lists()
            self.score += 1

        keys = arcade.check_for_collision_with_list(self.player, self.keys_list)
        for key in keys:
            if keys:
                key.remove_from_sprite_lists()
                self.door_open = True
                self.show_key_message = True
                self.exit_list[1].remove_from_sprite_lists()
                self.exit_list[0].remove_from_sprite_lists()

        open_door = arcade.check_for_collision_with_list(self.player, self.open_list)
        if open_door and self.door_open:
            self.game_win = True

        if self.show_key_message:
            self.key_message_timer -= delta_time
            if self.key_message_timer <= 0:
                self.show_key_message = False

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.player.change_x = -1
        elif key == arcade.key.D:
            self.player.change_x = 1
        elif key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.D:
            self.player.change_x = 0


def setup_game(width=960, height=640, title="Leonardo Game"):
    game = GridGame(width, height, title)
    game.setup()
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()

