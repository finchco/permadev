import tcod as libtcod


def render_all(con, entities, items, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
    #if fov_recompute:
    for y in range(game_map.height):
        for x in range(game_map.width):
            visible = libtcod.map_is_in_fov(fov_map, x, y)
            wall = game_map.tiles[x][y].block_sight

            if visible:
                if wall:
                    libtcod.console_put_char_ex(con, x, y, '#', colors.get('light_wall'), colors.get('dark_ground'))
                else:
                    libtcod.console_put_char_ex(con, x, y, ' ', colors.get('light_ground'), colors.get('dark_ground_bg'))
                game_map.tiles[x][y].explored = True
            elif game_map.tiles[x][y].explored:
                if wall:
                    libtcod.console_put_char_ex(con, x, y, '#', colors.get('dark_wall'), colors.get('dark_ground'))
                else:
                    libtcod.console_put_char_ex(con, x, y, ' ', colors.get('dark_ground'), colors.get('dark_ground_bg'))

    for item in items:
        draw_entity(con, item, fov_map)

    for entity in entities:
        draw_entity(con, entity, fov_map)

def clear_all(con, entities, items):
    for entity in entities:
        clear_entity(con, entity)
    for item in items:
        clear_entity(con, item)

def draw_entity(con, entity, fov_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

def clear_entity(con, entity):
    # erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)

