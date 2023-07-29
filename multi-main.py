import sys
from PIL import Image
from mctools import RCONClient
import threading

MC_Base_Color_Dict = {
    (127, 178, 56): ("grass_block", "slime_block"),
    (247, 233, 163): ("sand", "birch_planks", "birch_log"),
    (199, 199, 199): ("mushroom_stem",),
    (255, 0, 0): ("redstone_block",),
    (160, 160, 255): ("packed_ice",),
    (167, 167, 167): ("iron_block",),
    (0, 124, 0): ("sugar_cane",),
    (255, 255, 255): ("white_wool", "white_concrete", "white_glazed_terracotta"),
    (164, 168, 184): ("clay", "chiseled_stone_bricks", "cracked_stone_bricks"),
    (151, 109, 77): ("dirt", "jungle_wood", "brown_mushroom_block"),
    (112, 112, 112): ("diamond_ore", "emerald_ore", "lapis_ore"),
    (143, 119, 72): ("oak_planks", "oak_log", "stripped_oak_wood"),
    (255, 252, 245): ("chiseled_quartz_block", "diorite", "sea_lantern"),
    (216, 127, 51): ("stripped_acacia_wood", "orange_wool", "orange_concrete"),
    (178, 76, 216): ("magenta_wool", "magenta_concrete", "purpur_block"),
    (102, 153, 216): ("light_blue_wool", "light_blue_concrete", "light_blue_glazed_terracotta"),
    (229, 229, 51): ("sponge", "yellow_wool", "yellow_glazed_terracotta"),
    (127, 204, 25): ("lime_wool", "melon", "lime_glazed_terracotta"),
    (242, 127, 165): ("brain_coral_block", "pink_concrete", "pink_glazed_terracotta"),
    (76, 76, 76): ("acacia_wood", "gray_glazed_terracotta", "dead_bubble_coral_block"),
    (153, 153, 153): ("light_gray_wool", "light_gray_glazed_terracotta", "light_gray_concrete"),
    (76, 127, 153): ("prismarine", "cyan_wool", "cyan_glazed_terracotta"),
    (127, 63, 178): ("purple_glazed_terracotta", "bubble_coral_block", "amethyst_block"),
    (51, 76, 178): ("tube_coral_block", "blue_glazed_terracotta", "blue_wool"),
    (102, 76, 51): ("dark_oak_planks", "brown_wool", "brown_glazed_terracotta"),
    (102, 127, 51): ("green_wool", "green_glazed_terracotta", "dried_kelp_block"),
    (153, 51, 51): ("red_glazed_terracotta", "red_mushroom_block", "shroomlight"),
    (25, 25, 25): ("black_glazed_terracotta", "basalt", "coal_block"),
    (250, 238, 77): ("gold_block",),
    (92, 219, 213): ("diamond_block", "beacon", "dark_prismarine"),
    (74, 128, 255): ("lapis_block",),
    (74, 128, 255): ("emerald_block",),
    (129, 86, 49): ("spruce_planks", "spruce_wood", "stripped_spruce_wood"),
    (112, 2, 0): ("netherrack",),
    (209, 177, 161): ("white_terracotta", "calcite"),
    (159, 82, 36): ("orange_terracotta",),
    (149, 87, 108): ("magenta_terracotta",),
    (112, 108, 138): ("light_blue_terracotta",),
    (186, 133, 36): ("yellow_terracotta",),
    (103, 117, 53): ("lime_terracotta",),
    (160, 77, 78): ("pink_terracotta",),
    (57, 41, 35): ("gray_terracotta",),
    (135, 107, 98): ("light_gray_terracotta",),
    (87, 92, 92): ("cyan_terracotta",),
    (122, 73, 88): ("purple_terracotta",),
    (76, 62, 92): ("blue_terracotta",),
    (76, 50, 35): ("brown_terracotta", "dripstone_block"),
    (76, 82, 42): ("green_terracotta",),
    (142, 60, 46): ("red_terracotta",),
    (37, 22, 16): ("black_terracotta",),
    (189, 48, 49): ("crimson_nylium",),
    (148, 63, 97): ("crimson_planks", "crimson_stem", "stripped_crimson_stem"),
    (92, 25, 29): ("crimson_hyphae", "stripped_crimson_hyphae"),
    (22, 126, 134): ("warped_nylium",),
    (58, 142, 140): ("warped_planks", "warped_stem", "stripped_warped_stem"),
    (86, 44, 62): ("warped_hyphae", "stripped_warped_hyphae"),
    (20, 180, 133): ("warped_wart_block",),
    (86, 86, 86): ("chiseled_deepslate", "deepslate", "cobbled_deepslate"),
    (186, 150, 126): ("raw_iron_block",)
}

# rcon = RCONClient("127.0.0.1", 25575)
# rcon.login("chipmunk")
# if not rcon.is_authenticated():
#     sys.exit(1)


class ColorThread(threading.Thread):
    def __init__(self, info, map_color_level, real_color, base_color):
        threading.Thread.__init__(self)
        self.result = None
        self.info = info
        self.map_color_level = map_color_level
        self.real_color = real_color
        self.base_color = base_color

    def run(self):
        self.result = compare_color(self.info, self.map_color_level, self.real_color, self.base_color)

    def get_result(self):
        return self.result


def compare_color(info, map_color_level, real_color, base_color):
    """
    :param info: block info for the pixel
    :param map_color_level: 135 or 180 or 220
    :param real_color: the pixel color
    :param base_color: the base color of a block, key of MC_Base_Color_Dict
    :return: block info
    """
    map_color = (int(base_color[0] * map_color_level/ 255), int(base_color[1] * map_color_level / 255), int(base_color[2] * map_color_level / 255))
    diff = abs(map_color[0] - real_color[0]) + abs(map_color[1] - real_color[1]) + abs(map_color[2] - real_color[2])
    if diff < info[2]:
        info = (map_color, map_color_level, diff)
    return info


image = Image.open("test.JPG")
rgb_image = image.convert("RGB")


for x in range(256):
    for y in range(144):
        r, g, b = rgb_image.getpixel((x, y))
        pixel_color = (r, g, b)
        block_info = ((-255, -255, -255), 135, 256 * 3)
        for base in MC_Base_Color_Dict.keys():
            thread1 = ColorThread(block_info, 135, pixel_color, base)
            thread2 = ColorThread(block_info, 180, pixel_color, base)
            thread3 = ColorThread(block_info, 220, pixel_color, base)
            thread1.start()
            thread2.start()
            thread3.start()
            thread1.join()
            thread2.join()
            thread3.join()
            info135 = thread1.get_result()
            info180 = thread2.get_result()
            info220 = thread3.get_result()
            print(info135, info180, info220)
        print((x, y))
        # command = f"setblock {x} 100 {y} {MC_Base_Color_Dict[block_info[0]][0]}"
        # print(command)
        # rcon.command(command)
        # rgb_image.putpixel((x, y), block_info[0])
        # print(r, g, b)
# rgb_image.save("result.jpg")
# rcon.stop()
