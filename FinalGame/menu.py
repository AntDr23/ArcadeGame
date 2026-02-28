import arcade
import arcade.gui

SPEED = 4
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
SCREEN_TITLE = "ArcadeGame"
TILE_SCALING = 0.5
PLAYER_JUMP = 23
GRAVITY = 1


class MenuButton:
    def __init__(self, x, y, width, height, text, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action
        self.is_hovered = False

    def draw(self):
        color = arcade.color.DARK_BLUE
        left = self.x - self.width // 2
        bottom = self.y - self.height // 2
        arcade.draw_lbwh_rectangle_filled(left, bottom, self.width, self.height, color)
        arcade.draw_lbwh_rectangle_outline(left, bottom, self.width, self.height, arcade.color.WHITE, 3)
        arcade.draw_text(self.text, self.x, self.y, arcade.color.WHITE, 20, anchor_x="center", anchor_y="center")

    def check_click(self, mouse_x, mouse_y):
        return abs(mouse_x - self.x) < self.width / 2 and abs(mouse_y - self.y) < self.height / 2


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.buttons = []
        center_x = SCREEN_WIDTH // 2
        self.buttons.append(MenuButton(center_x, 450, 300, 60, "Выбор уровня", "levels"))
        self.buttons.append(MenuButton(center_x, 360, 300, 60, "Выход", "exit"))

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.SKY_BLUE)
        arcade.draw_text("ArcadeGame", SCREEN_WIDTH // 2, 720, arcade.color.WHITE, 64, anchor_x="center")
        for button in self.buttons:
            button.draw()

    def on_mouse_press(self, mouse_x, mouse_y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for btn in self.buttons:
                if btn.check_click(mouse_x, mouse_y):
                    if btn.action == "start":
                        game = FirstLevel()
                        game.setup()
                        self.window.show_view(game)
                    elif btn.action == "levels":
                        self.window.show_view(LevelSelectView(self))
                    elif btn.action == "exit":
                        arcade.exit()


class LevelSelectView(arcade.View):
    def __init__(self, menu_view):
        super().__init__()
        self.menu_view = menu_view
        self.buttons = []
        center_x = SCREEN_WIDTH // 2

        self.buttons.append(MenuButton(center_x, 600, 250, 80, "Уровень 1", "level1"))
        self.buttons.append(MenuButton(center_x, 500, 250, 80, "Уровень 2", "level2"))
        self.buttons.append(MenuButton(center_x, 400, 250, 80, "Уровень 3", "level3"))
        self.buttons.append(MenuButton(center_x, 250, 200, 60, "Назад", "back"))

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Выбор уровня", SCREEN_WIDTH // 2, 720, arcade.color.WHITE, 48, anchor_x="center")

        for button in self.buttons:
            button.draw()

    def on_mouse_press(self, mouse_x, mouse_y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for btn in self.buttons:
                if btn.check_click(mouse_x, mouse_y):
                    if btn.action == "level1":
                        game = FirstLevel()
                        game.setup()
                        self.window.show_view(game)
                    if btn.action == "level2":
                        game = SecondLevel()
                        game.setup()
                        self.window.show_view(game)
                    if btn.action == "level3":
                        game = ThirdLevel()
                        game.setup()
                        self.window.show_view(game)
                    elif btn.action == "back":
                        self.window.show_view(self.menu_view)


class Game(arcade.View):
    def __init__(self):
        super().__init__()
        self.all_sprites = None
        self.wall_sprites = None
        self.player = None
        self.background_music = arcade.load_sound("resources/game_sound.mp3")
        self.victory_sound = arcade.load_sound("resources/win_sound.mp3")
        self.gameover_sound = arcade.load_sound("resources/lose_sound.mp3")
        self.is_music_playing = False
        self.game_win = False
        self.key_found = False
        self.touch_closed_door = False
        self.score = 0
        self.door_open = False
        self.found_key = False
        self.show_key_message = False
        self.music_player = False
        self.key_message_timer = 1.5
        self.player_texture = arcade.load_texture(
            ":resources:images/animated_characters/female_person/femalePerson_idle.png")

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.world_width = SCREEN_WIDTH
        self.world_height = SCREEN_HEIGHT

        arcade.set_background_color(arcade.color.SKY_BLUE)


    def setup(self):
        self.music_player = arcade.play_sound(self.background_music, 0.3)

    def on_draw(self):
        arcade.draw_text(
            f"Монетки: {self.score}",
            10,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            24,
            font_name="Arial"
        )

        if not self.found_key:
            arcade.draw_text(
                f"Отыщите ключ",
                SCREEN_WIDTH - 250,
                SCREEN_HEIGHT - 40,
                arcade.color.PURPLE,
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

        if self.touch_closed_door:
            arcade.draw_text(
                "ВЫ ПРОИГРАЛИ!",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 30,
                arcade.color.RED,
                48,
                anchor_x="center",
                anchor_y="center",
                font_name="Arial"
            )

        if self.found_key:
            arcade.draw_text(
                f"Доберитесь до выхода",
                SCREEN_WIDTH - 350,
                SCREEN_HEIGHT - 40,
                arcade.color.PURPLE,
                24,
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
                self.found_key = True
                self.exit_list[1].remove_from_sprite_lists()
                self.exit_list[0].remove_from_sprite_lists()

        open_door = arcade.check_for_collision_with_list(self.player, self.open_list)
        if open_door and self.door_open:
            self.game_win = True
            self.key_message_timer -= delta_time / 2
            if self.key_message_timer <= 0:
                arcade.play_sound(self.victory_sound, 0.2)
                arcade.stop_sound(self.music_player)
                menu = MenuView()
                menu.on_draw()
                self.window.show_view(menu)
        elif open_door:
            arcade.play_sound(self.gameover_sound, 0.2)
            self.touch_closed_door = True

        if self.touch_closed_door:
            self.key_message_timer -= delta_time / 2
            if self.key_message_timer <= 0:
                arcade.stop_sound(self.music_player)
                menu = MenuView()
                menu.on_draw()
                self.window.show_view(menu)
                self.key_message_timer = 1.5

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


class FirstLevel(Game):
    def __init__(self):
        super().__init__()

    def setup(self):
        Game.setup(self)
        self.all_sprites = arcade.SpriteList()
        self.player = arcade.Sprite(self.player_texture, scale=0.5)
        self.player.position = (126, 256)
        self.all_sprites.append(self.player)

        self.key_message_timer = 1.5
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_sprites)
        self.player.change_x = 0
        self.player.change_y = 0
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        map_name = "lvl1.tmx"
        tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)

        self.wall_list = tile_map.sprite_lists["walls"]
        self.coins_list = tile_map.sprite_lists["coins"]
        self.decor_list = tile_map.sprite_lists["decor"]
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
        self.keys_list.draw()
        self.open_list.draw()
        self.exit_list.draw()
        self.player_list.draw()
        self.gui_camera.use()
        Game.on_draw(self)


class SecondLevel(Game):
    def __init__(self):
        super().__init__()
        self.game_over = False


    def setup(self):
        Game.setup(self)
        self.all_sprites = arcade.SpriteList()
        self.player = arcade.Sprite(self.player_texture, scale=0.5)
        self.player.position = (126, 256)
        self.all_sprites.append(self.player)

        self.key_message_timer = 1.5
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_sprites)
        self.player.change_x = 0
        self.player.change_y = 0
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        map_name = "lvl2.tmx"
        tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)

        self.wall_list = tile_map.sprite_lists["walls"]
        self.coins_list = tile_map.sprite_lists["coins"]
        self.decor_list = tile_map.sprite_lists["decor"]
        self.keys_list = tile_map.sprite_lists["keys"]
        self.spikes_list = tile_map.sprite_lists["spikes"]
        self.exit_list = tile_map.sprite_lists["door closed"]
        self.open_list = tile_map.sprite_lists["door opened"]
        self.collision_list = tile_map.sprite_lists["collision"]
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            self.collision_list,
            gravity_constant=GRAVITY
        )

    def game_over_lose(self):
        self.game_over = True
        if self.gameover_sound:
            arcade.play_sound(self.gameover_sound, 0.3)

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.all_sprites.draw()
        self.spikes_list.draw()
        self.wall_list.draw()
        self.coins_list.draw()
        self.decor_list.draw()
        self.keys_list.draw()
        self.open_list.draw()
        self.exit_list.draw()
        self.player_list.draw()
        self.gui_camera.use()
        Game.on_draw(self)

    def on_update(self, delta_time):
        if self.game_over:
            self.touch_closed_door = True
            self.key_message_timer -= delta_time / 2
            if self.key_message_timer <= 0:
                arcade.stop_sound(self.music_player)
                menu = MenuView()
                menu.on_draw()
                self.window.show_view(menu)
        else:
            Game.on_update(self, delta_time)
            spikes_hit = arcade.check_for_collision_with_list(self.player, self.spikes_list)
            for spikes in spikes_hit:
                self.game_over_lose()


class ThirdLevel(Game):
    def __init__(self):
        super().__init__()
        self.game_over = False


    def setup(self):
        Game.setup(self)
        self.all_sprites = arcade.SpriteList()
        self.player = arcade.Sprite(self.player_texture, scale=0.5)
        self.player.position = (126, 256)
        self.all_sprites.append(self.player)

        self.key_message_timer = 1.5
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_sprites)
        self.player.change_x = 0
        self.player.change_y = 0
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        map_name = "lvl3.tmx"
        tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)

        self.wall_list = tile_map.sprite_lists["walls"]
        self.coins_list = tile_map.sprite_lists["coins"]
        self.jump_pad_list = tile_map.sprite_lists["jump_pad"]
        self.decor_list = tile_map.sprite_lists["decor"]
        self.keys_list = tile_map.sprite_lists["keys"]
        self.spikes_list = tile_map.sprite_lists["spikes"]
        self.exit_list = tile_map.sprite_lists["door closed"]
        self.open_list = tile_map.sprite_lists["door opened"]
        self.collision_list = tile_map.sprite_lists["collision"]
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            self.collision_list,
            gravity_constant=GRAVITY
        )

    def game_over_lose(self):
        self.game_over = True
        if self.gameover_sound:
            arcade.play_sound(self.gameover_sound, 0.3)

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.all_sprites.draw()
        self.spikes_list.draw()
        self.jump_pad_list.draw()
        self.wall_list.draw()
        self.coins_list.draw()
        self.decor_list.draw()
        self.keys_list.draw()
        self.open_list.draw()
        self.exit_list.draw()
        self.player_list.draw()
        self.gui_camera.use()
        Game.on_draw(self)

    def on_update(self, delta_time):
        if self.game_over:
            self.touch_closed_door = True
            self.key_message_timer -= delta_time / 2
            if self.key_message_timer <= 0:
                arcade.stop_sound(self.music_player)
                menu = MenuView()
                menu.on_draw()
                self.window.show_view(menu)
        else:
            Game.on_update(self, delta_time)
            spikes_hit = arcade.check_for_collision_with_list(self.player, self.spikes_list)
            for spikes in spikes_hit:
                self.game_over_lose()
            jump_pad_hit = arcade.check_for_collision_with_list(self.player, self.jump_pad_list)
            for jump_pad in jump_pad_hit:
                self.player.change_y = 40

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "ArcadeGame")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()