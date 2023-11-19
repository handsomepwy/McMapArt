import ttkbootstrap as ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk
import random
from mctools import RCONClient

MC_Base_Color_Dict = {
    (127, 178, 56): ("grass_block", "slime_block"),
    (247, 233, 163): ("birch_planks", "birch_log"),
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
all_rgb = {}

root = ttk.Window(title="McMapArt generator v1.2", themename="morph")
root.iconbitmap("icon.ico")
file_loc = ttk.StringVar(root, "")
image_file = Image.open("icon.ico")
show_image = image_file
columns_data = []
rcon_host = ttk.Variable(root, "127.0.0.1", "host")
rcon_port = ttk.Variable(root, 25575, "port")
rcon_password = ttk.Variable(root, "chipmunk", "password")


def calculate_a_column(x, rgb_image):
    column = []
    for y in range(rgb_image.height):
        c = 0
        r, g, b = rgb_image.getpixel((x, y))
        pixel_color = (r, g, b)
        block_info = ((-255, -255, -255), 180, 256 * 3, "nothing")
        for key, value in all_rgb.items():
            for i in range(len(value)):
                map_color = value[i]
                if map_color == pixel_color:
                    block_info = (map_color, i, 0, key)
                    break
                diff = abs(map_color[0] - r) + abs(map_color[1] - g) + abs(map_color[2] - b)
                if diff < block_info[2]:
                    c += 1
                    block_info = (map_color, i, diff, key)
            if block_info[2] == 0:
                break
        block_info = (block_info[0], block_info[1], block_info[2], random.choice(MC_Base_Color_Dict[block_info[3]]))
        column.append(block_info)
    return column


def handle_column(column_data, row, start_pos, rcon):
    height_data = []
    for i in range(len(column_data)):
        block_data = column_data[i]
        block_x = start_pos[0] + row
        block_z = start_pos[1] + i
        command = ""
        if i == 0:
            command = f"setblock {block_x} 160 {block_z} {block_data[3]}"
            height_data.append(160)
        else:
            if block_data[1] == 1:
                command = f"setblock {block_x} {height_data[-1]} {block_z} {block_data[3]}"
                height_data.append(height_data[-1])
            elif block_data[1] == 0:
                block_y = height_data[-1]-1
                if block_y > 160:
                    block_y = 160
                if block_y < -60:
                    block_y = -60
                command = f"setblock {block_x} {block_y} {block_z} {block_data[3]}"
                height_data.append(block_y)
            elif block_data[1] == 1:
                block_y = height_data[-1]+1
                if block_y < 160:
                    block_y = 160
                if block_y > 319:
                    print(block_y)
                    block_y = 319
                command = f"setblock {block_x} {block_y} {block_z} {block_data[3]}"
                height_data.append(block_y)
        print(rcon.command(command))


def start_file_frame():
    file_frame = ttk.Labelframe(root, text="Picture", width=100, height=200, style="primary")
    file_frame.pack(side="left", padx=10)

    def choose_pic():
        file = askopenfilename(filetypes=[("PNG", ".png .jpg"), ("JPG", ".jpg")])
        file_loc.set("file selected" + file)
        global image_file, show_image
        image_file = Image.open(file)
        show_image = Image.open(file)
        i = 1
        if show_image.width > 1000 or show_image.height > 1000:
            while int(show_image.width/i) > 1000 or int(show_image.height/i) > 1000:
                i += 1
        print(i)
        show_image = ImageTk.PhotoImage(show_image.resize((int(show_image.width/i), int(show_image.height/i))))
        image_label = ttk.Label(file_frame, image=show_image)
        image_label.pack()

    def gen_preview():
        file = asksaveasfilename()
        print(file)
        if "." not in file:
            warn_label = ttk.Label(file_frame, text="save filename doesn't have a suffix")
            warn_label.pack()
            return False
        global image_file
        for x in range(image_file.width):
            col = calculate_a_column(x, image_file.convert("RGB"))
            columns_data.append(col)
            for i in range(len(col)):
                image_file.putpixel((x, i), col[i][0])
            print(f"processed x pos:{x+1}/{image_file.width}")
        image_file.save(file)
        print("image processed and saved")

    file_label = ttk.Label(file_frame, textvariable=file_loc)
    file_label.pack()
    select_btn = ttk.Button(file_frame, text="choose a picture", command=choose_pic, style="info", width=15)
    select_btn.pack(pady=10)
    process_label = ttk.Label(file_frame, text="please press the generate preview button before running!!",
                              style="danger")
    process_label.pack()
    process_btn = ttk.Button(file_frame, text="generate preview", command=gen_preview, style="primary", width=15)
    process_btn.pack()


def start_rcon_frame():
    rcon_frame = ttk.Labelframe(root, text="Rcon", width=75, height=150, style="primary")
    rcon_frame.pack(padx=10, pady=10)
    global rcon_host, rcon_port, rcon_password

    def refresh_rcon_data():
        global rcon_host, rcon_port, rcon_password
        rcon_host.set(host_entry.get())
        rcon_port.set(int(port_entry.get()))
        rcon_password.set(password_entry.get())

    host_label = ttk.Label(rcon_frame, text="host")
    host_label.pack()
    host_entry = ttk.Entry(rcon_frame, textvariable=rcon_host, style="success", width=20)
    host_entry.pack(padx=15)
    port_label = ttk.Label(rcon_frame, text="port")
    port_label.pack()
    port_entry = ttk.Entry(rcon_frame, textvariable=rcon_port, style="info")
    port_entry.pack()
    password_label = ttk.Label(rcon_frame, text="password")
    password_label.pack()
    password_entry = ttk.Entry(rcon_frame, textvariable=rcon_password, show="*", style="danger")
    password_entry.pack()
    data_refresh_btn = ttk.Button(rcon_frame, text="refresh", command=refresh_rcon_data, style="success-link")
    data_refresh_btn.pack()


def start_run_frame():
    global image_file, rcon_host, rcon_port, rcon_password
    run_frame = ttk.Labelframe(root, text="Run", style="primary")
    run_frame.pack(pady=10)

    def run_lines():
        global image_file, rcon_host, rcon_port, rcon_password
        start_x_pos = int(start_x_entry.get())
        start_y_pos = int(start_y_entry.get())
        start_line = int(run_line_start_entry.get())
        end_line = int(run_line_end_entry.get())
        rcon = RCONClient(rcon_host.get(), rcon_port.get())
        rcon.login(rcon_password.get())
        for i in range(start_line, end_line+1):
            rcon.command(f"forceload add {start_x_pos+i} {start_y_pos} {start_x_pos+i} {start_y_pos+image_file.height}")
            handle_column(columns_data[i], i, (start_x_pos, start_y_pos), rcon)
            rcon.command(f"forceload remove {start_x_pos + i} {start_y_pos} {start_x_pos + i} "
                         f"{start_y_pos + image_file.height}")

    start_x_label = ttk.Label(run_frame, text="start x")
    start_x_label.pack()
    start_x_entry = ttk.Entry(run_frame, style="primary")
    start_x_entry.pack(padx=15)
    start_y_label = ttk.Label(run_frame, text="start y")
    start_y_label.pack()
    start_y_entry = ttk.Entry(run_frame, style="primary")
    start_y_entry.pack()
    run_line_start_label = ttk.Label(run_frame, text="run line start")
    run_line_start_label.pack()
    run_line_start_entry = ttk.Entry(run_frame, style="dark")
    run_line_start_entry.pack()
    run_line_end_label = ttk.Label(run_frame, text="run line end")
    run_line_end_label.pack()
    run_line_end_entry = ttk.Entry(run_frame, style="dark")
    run_line_end_entry.pack()
    run_button = ttk.Button(run_frame, text="run", command=run_lines, style="info-outline")
    run_button.pack(pady=10)


def preload_dict():
    global all_rgb, MC_Base_Color_Dict
    for key, value in MC_Base_Color_Dict.items():
        all_rgb[key] = ((int(key[0]*180/255), int(key[1]*180/255), int(key[2]*180/255)),
                        (int(key[0]*220/255), int(key[1]*220/255), int(key[2]*220/255)),
                        key)


start_file_frame()
start_rcon_frame()
start_run_frame()
preload_dict()
print("This is the McMapArt generator log window\nBecause of tech issues, we cannot show processing log in the "
      "GUI\nSo when you are running a map art, please see this window instead of the GUI\n"
      "OS may say that the program have no response, don't worry\nThank you for using the program\nProject Repo: "
      "https://github.com/handsomepwy/McMapArt\nMy bilibili account: https://space.bilibili.com/513244188\nHope you "
      "have fun!")
root.mainloop()
