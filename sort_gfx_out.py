# This is part of PRSP NewGRF.
# (c) Rito12, GPL 2.0

import os
import re
from PIL import Image, ImageDraw, ImageShow

templates = {
	"sprite_purchase": (50, 12),
	"sprite_advertisement100": (100, 12),
	"sprite_advertisement200": (200, 12),
	"sprite_advertisement300": (300, 12),
	"sprite_train": (232, 28),
	"sprite_train_sym": (112, 28),
	"sprite_train_8": (112, 28),
	"sprite_train_x2": (232 * 2, 28 * 2),
	"sprite_train_sym_x2": (112 * 2, 28 * 2),
	"sprite_train_8_x2": (112 * 2, 28 * 2),
	"sprite_train10": (262, 32),
	"sprite_train10_x2": (262 * 2, 32 * 2),
	"sprite_train10_offset": (262, 32),
	"sprite_train10_offset_x2": (262 * 2, 32 * 2),
	"sprite_train12": (292, 36),
	"sprite_train12_x2": (292 * 2, 36 * 2),
	"sprite_train12_offset": (292, 36),
	"sprite_train12_offset_x2": (292 * 2, 36 * 2),
	"sprite_train12_l": (290, 31),
	"sprite_train12_r": (290, 31),
	"sprite_train12_rear": (292, 36),
}

offset_after = {k: (20 if v[1] < 20 else 40 if v[1] < 40 else 80) for k, v in templates.items()}

# These files aren't included in the generated grf file.
# We lack some gfx files, although not all.
IGNORE_FILES = ["en76-elf.pnml", "eu47.pnml", "enxx-common.pnml"]

# In some files we already have reversed version.
# In pendolino the order is strongly related to its macro.
ALLOW_MULTIPLE_ROWS = ["gfx/ep09.png", "gfx/eu07.png", "gfx/ed250-pendolino.png", "gfx/EW51.png"]


def append_sprite(name_defines, sprites, png_file_name, template, x, y, span, pnml_file):
	if png_file_name[0] != '"' or png_file_name[-1] != '"':
		png_file_name = name_defines[png_file_name]
	else:
		png_file_name = png_file_name[1:-1]
	if png_file_name not in sprites:
		sprites[png_file_name] = []
	box = (x, y, templates[template][0] + x, templates[template][1] + y)
	sprites[png_file_name].append({"template": template, "box": box, "nml_span": span, "pnml_file": pnml_file})


def show_image_from_path(path):
	for viewer in ImageShow._viewers:
		if viewer.show_file(path):
			break


def do_sort():
	global did_any_changes

	spriteset = re.compile(r"(?P<pre_pos>spriteset.*,\s*(?P<gfx>.*)\).*tmpl_(?P<tmpl>.*)\()(?P<x>[0-9]*)(?P<in_pos>\s*,\s*)(?P<y>[0-9]*)(?P<after_pos>.*\))")
	png_def = re.compile(r'#define\s*([A-Za-z0-9_]*)\s*(".*\.png")')
	name_defines = {}
	sprites = {}

	for root, dirs, files in os.walk("src/engines"):  # For now ignore wagons.
		for f in files:
			if not f.endswith(".pnml") or f in IGNORE_FILES:
				continue
			with open(os.path.join(root, f)) as file:
				content = file.read()
				for m in png_def.finditer(content):
					name_defines[m.group(1)] = m.group(2)[1:-1]
				if f == "ed250-pendolino.pnml":
					# Pendolino has its own macro, hard code it here.
					pendolino_macro = re.compile(r"ED250_SPRITES\(.*,\s*([0-9]*)\s*,\s*([0-9]*)\s*\)")
					for m in pendolino_macro.finditer(content):
						append_sprite(name_defines, sprites, "ED250_FILE", "sprite_train12", int(m.group(1)), int(m.group(2)), m.span(), os.path.join(root, f))
						append_sprite(name_defines, sprites, "ED250_FILE", "sprite_train12", int(m.group(1)), int(m.group(2)) + 280, (0, 0), os.path.join(root, f))
						append_sprite(name_defines, sprites, "ED250_FILE", "sprite_train12", int(m.group(1)), int(m.group(2)) + 840, (0, 0), os.path.join(root, f))
						append_sprite(name_defines, sprites, "ED250_FILE", "sprite_train12_rear", int(m.group(1)), int(m.group(2)), (0, 0), os.path.join(root, f))
						append_sprite(name_defines, sprites, "ED250_FILE", "sprite_train12_rear", int(m.group(1)), int(m.group(2)) + 280, (0, 0), os.path.join(root, f))
						append_sprite(name_defines, sprites, "ED250_FILE", "sprite_train12_l", int(m.group(1)), int(m.group(2)) + 560, (0, 0), os.path.join(root, f))
						append_sprite(name_defines, sprites, "ED250_FILE", "sprite_train12_r", int(m.group(1)), int(m.group(2)) + 560, (0, 0), os.path.join(root, f))
				for m in spriteset.finditer(content):
					append_sprite(name_defines, sprites, m.group("gfx"), m.group("tmpl"), int(m.group("x")), int(m.group("y")), m.span(), os.path.join(root, f))

	nml_updates = {}

	no_changes = 0
	for path in sprites:
		# Sort sprites by y coordinate.
		sprites[path].sort(key=lambda val: val["box"][1])

		if not os.path.exists(path):
			print(path)
			continue

		did_any_changes = False

		with Image.open(path) as im:
			# First crop then fill to be overlapproof.
			for i in range(len(sprites[path])):
				sprite: dict = sprites[path][i]  # sprites[path][i] is an dict, so we get a reference here.
				try:
					for j in range(i - 1, -1, -1):
						if sprites[path][j]["box"][1] != sprite["box"][1]:
							break
						if sprites[path][j]["box"] == sprite["box"]:
							sprite["other"] = sprites[path][j].get("other", default=j)
							raise UserWarning("The sprite is used twice or more.")
				except UserWarning:
					pass
				else:
					# Usually there is a comment on the right side of purchase sprite, copy it as well.
					box = (sprite["box"][0], sprite["box"][1], im.size[0], sprite["box"][3]) if sprite["template"] == "sprite_purchase" else sprite["box"]
					sprite["image"] = im.crop(box)
			draw = ImageDraw.Draw(im)
			for sprite in sprites[path]:
				right = im.size[0] if sprite["template"] == "sprite_purchase" else sprite["box"][2] - 1
				draw.rectangle((sprite["box"][0], sprite["box"][1], right, sprite["box"][3] - 1), fill="#ffffff", width=0)

			# Expand canvas.
			start_size = im.size
			new_im = im.resize((a * 2 for a in start_size))
			ImageDraw.Draw(new_im).rectangle((0, 0, *new_im.size), fill="#ffffff")
			new_im.paste(im)

			# Put back sprites but in correct possitions.
			y = 20  # Leave space for arrows at the file top.
			last_y = y
			last_x_end = 0
			max_x = 0
			for sprite in sprites[path]:
				if "image" not in sprite:
					other = sprites[path][sprite["other"]]
					if other["pnml_file"] in nml_updates:
						if sprite["pnml_file"] not in nml_updates:
							nml_updates[sprite["pnml_file"]] = {}  # Not list as we use span for indexing.
						nml_updates[sprite["pnml_file"]][sprite["nml_span"]] = nml_updates[other["pnml_file"]][other["nml_span"]]
					continue

				def paste(pos):
					global did_any_changes
					new_im.paste(sprite["image"], pos)

					assert type(pos) is type(sprite["box"])
					if sprite["box"][0:2] != pos:
						if sprite["pnml_file"] not in nml_updates:
							nml_updates[sprite["pnml_file"]] = {}  # Not list as we use span for indexing.
						nml_updates[sprite["pnml_file"]][sprite["nml_span"]] = pos

						did_any_changes = True

				if last_x_end < sprite["box"][0] and path in ALLOW_MULTIPLE_ROWS:
					paste((sprite["box"][0], last_y))
					y = max(last_y + offset_after[sprite["template"]], y)
					last_x_end = sprite["box"][2]
				else:
					paste((4, y))
					last_y = y
					y += offset_after[sprite["template"]]
					last_x_end = sprite["box"][2] - sprite["box"][0] + 4
				max_x = max(max_x, last_x_end + 4)

			new_im = new_im.crop((0, 0, max(max_x, start_size[0]), max(start_size[1], y)))
			if not did_any_changes:
				no_changes += 1
				continue
			root, ext = os.path.splitext(path)
			new_path = root + ".back" + ext
			os.replace(path, new_path)
			new_im.save(path)
			show_image_from_path(new_path)
			show_image_from_path(path)
			input("Press enter to continue with next image.")  # Give time for user to check if new file is ok.
			os.remove(new_path)

	for path in nml_updates:

		def update_match(match):
			if match.span() not in nml_updates[path]:
				return match.group(0)
			pos = nml_updates[path][match.span()]
			return match.group("pre_pos") + str(pos[0]) + match.group("in_pos") + str(pos[1]) + match.group("after_pos")

		tmp_path = path + ".tmp"
		with open(path, "r") as file:
			with open(tmp_path, "w") as tmp_file:
				tmp_file.write(spriteset.sub(update_match, file.read()))
		os.replace(tmp_path, path)

	print(no_changes, "images left unchanged.")


if __name__ == "__main__":
	do_sort()
