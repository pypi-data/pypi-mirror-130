# encoding: utf8

import os
import json
import time
import ctypes
import atexit
import logging
import functools

import mouse
import keyboard
import patch_keyboard

from utils import *
from functools import partial

import utils

# for debug keyboard module
__builtins__.__dict__["mouzz_log"] = log 

@singleton
class G(object):

	Mode = None

utils.G = G

@singleton
class Config(object):

	def __init__(self):
		with open("config.json", "r+") as rf:
			self.data = json.load(rf)

	def get(self, key, defv=None):
		return self.data.get(key, defv)

@singleton
class Keys(object):

	def __init__(self):
		keys = Config.get("keys")
		self.left = keys["mouse_move_left"]
		self.right = keys["mouse_move_right"]
		self.up = keys["mouse_move_up"]
		self.down = keys["mouse_move_down"]

		for name in [
				"chrome", "move_window", "direction", 
				"mouse_left_key", "mouse_right_key", "mouse_wheel_up", "mouse_wheel_down",
				"page_up", "page_down", "goto_top", "goto_bottom",
				"kill", "copy", "paste",
				"keep_press_mouse_left_key", "grab_screen",
				"enter_insert_mode", "enter_normal_mode",
				]:
			setattr(self, name, keys.get(name))

@singleton
class MoveMouse(object):

	""" 模拟鼠标移动 """

	def __init__(self):
		self.is_move_left = False
		self.is_move_right = False
		self.is_move_up = False
		self.is_move_down = False

	def tick(self):
		if G.Mode is not NormalMode:
			return
		if keyboard.is_pressed('alt+tab'):
			return
		# TODO win+tab?

		dx = dy = 0

		c = Config.get("mouse_speed")
		dd = c[""]
		for key, r in c.items():
			# 不能使用 alt 作为速度档位，因为 alt + tab 是 windows 默认的切换窗口的快捷键。
			if "alt" in key:
				raise Exception("cannot use alt key as speed key: %s" % key)
			if key and keyboard.is_pressed(key):
				dd = r
				break

		if self.is_move_left:
			dx = -1 * dd
		if self.is_move_right:
			dx = dd
		if self.is_move_up:
			dy = -1 * dd 
		if self.is_move_down:
			dy = dd

		if dx or dy: 
			mouse.move(dx, dy, absolute=False)

@singleton
class Common(object):

	""" 一些需要在多个 Mode 下都能工作(可能功能不同的)的键位 """

	def __init__(self):
		self.hotkey_list = []
		self.switching_window = False

	def setup_direction_keys(self):
		""" hjkl 在 NorlmalMode 下表示移动，或在切换窗口时表示方向键 """

		def on_key(k, v, key_event):
			log("Common.setup_direction_keys is_pressed", k, v, key_event, keyboard.is_pressed('alt'))
			is_press = key_event.event_type == keyboard.KEY_DOWN

			if G.Mode is NormalMode:
				# chrome left tab or right tab
				if k == Keys.left or k == Keys.right:
					if keyboard.is_pressed(Keys.chrome):
						log("chrome tab swtich")
						v = "page down" if k == keys.right else "page up"
						if is_press:
							keyboard.press("ctrl+%s" % v)
						else:
							keyboard.release("ctrl+%s" % v)
						return

				# 窗口停靠
				if keyboard.is_pressed(Keys.move_window):
					if is_press:
						log("windows_alt_tab_remap press windows", v)
						keyboard.press("windows+%s" % v)
					else:
						log("windows_alt_tab_remap release windows",v)
						keyboard.release("windows+%s" % v)
					return 

				# 方向键
				if keyboard.is_pressed(Keys.direction):
					if is_press:
						log("windows_alt_tab_remap press forward", v)
						keyboard.press(v)
					else:
						log("windows_alt_tab_remap release forward",v)
						keyboard.release(v)
					return 

			if self.switching_window:
				key = v # 替换成上下左右
				log("switching_window")
			else:
				key = k # 保持不变

			# 正在切换窗口或者在输入模式的话，只是替换键位
			if key == v or G.Mode is InsertMode:
				if is_press:
					log("windows_alt_tab_remap press down", key)
					keyboard.press(key)
				else:
					log("windows_alt_tab_remap release up", key)
					keyboard.release(key)
					if self.switching_window:
						keyboard.call_later(move_mouse_to_actived_window, delay=0.5)
			# 此时模拟鼠标移动 NormalMode 且不在切换窗口，直接吃掉键盘消息
			else :
				for name in ["up", "down", "left", "right"]:
					if key == getattr(Keys, name):
						setattr(MoveMouse, "is_move_%s" % name, is_press)

		for name in ["up", "down", "left", "right"]:
			k = getattr(Keys, name)
			v = name
			callback = functools.partial(on_key, k, v)
			keyboard.hook_key(k, callback, suppress = True)
			# callback = functools.partial(on_key, False, k, v)
			# keyboard.on_release_key(k, callback, suppress = True)
			log("Common.setup_direction_keys k %s v %s", k, v)

	def listen_alt_tab(self):
		""" 监控是否正在使用 alt+tab 切换窗口 """
		def e(event):
			if keyboard.is_pressed('alt') and keyboard.is_pressed('tab'):
				self.switching_window = True
			log("switch_window enter", self.switching_window)

		def l(event):
			self.switching_window = False
			log("switch_window leave", self.switching_window)

		keyboard.on_press_key("tab", e)
		keyboard.on_press_key("alt", e)
		keyboard.on_release_key("alt", l)

	def backup(self):
		# 使用 w 作为控制键，会影响到正常输入，比如说说 down 会不好输入
		"""
		def null(key):
			log("left")
			keyboard.send('delete, left')
		key = 'w+n'
		self.append_hotkey(key, keyboard.add_hotkey(key, partial(null, key), suppress=True))
		def null(key):
			log("right")
			keyboard.send('delete, right')
		key = 'w+m'
		self.append_hotkey(key, keyboard.add_hotkey(key, partial(null, key), suppress=True))
		def null(key):
			log("mouse right")
			keyboard.send('delete')
			time.sleep(0.01)
			mouse.click(mouse.RIGHT)
		key = 'w+p'
		self.append_hotkey(key, keyboard.add_hotkey(key, partial(null, key), suppress=True))
		"""

class Mode(object):

	def __init__(self):
		self.cleanup_list = []
		self.hotkey_list = []

	def enter(self):
		log("%s.enter" % self.__class__.__name__)
		self.on_enter()

	def on_enter(self):
		pass

	def leave(self):
		log("%s.leave" % self.__class__.__name__)

		self.on_leave()

		for name, c in self.cleanup_list:
			log("%s unhook %s %s" % (self.__class__.__name__, c, name))
			keyboard.unhook_key(c)
		for c in self.hotkey_list:
			log("%s remove hotkey %s %s" % (self.__class__.__name__, c, getattr(c, "key", "...")))
			keyboard.remove_hotkey(c)
		self.cleanup_list = []
		self.hotkey_list = []

	def on_leave(self):
		pass

	def append_cleanup(self, name, func):
		self.cleanup_list.append((name, func))

	def append_hotkey(self, key, func):
		func.key = key
		self.hotkey_list.append(func)

@singleton
class InsertMode(Mode):

	def on_enter(self):
		self.setup_change_mode()
		switch_chinese_input_method()
		print_current_state(repeat=False)

	def setup_change_mode(self):
		def enter_normal_mode(key):
			log("enter_normal_mode %s %s", G.Mode, key)
			if G.Mode is not NormalMode:
				switch_mode(NormalMode)
			else:
				keyboard.press(key)
		key = Keys.enter_normal_mode
		self.append_hotkey(key, keyboard.add_hotkey(key, functools.partial(enter_normal_mode, key), suppress=True))

@singleton
class NormalMode(Mode):

	def __init__(self):
		Mode.__init__(self)

		self.grab_screen_pos = [(-1, -1), (-1, -1)]
		self.keep_press_mouse_left_key = False

	def on_enter(self):
		self.setup_change_mode()
		self.setup_mouse_key()
		self.setup_mouse_move()
		self.setup_mouse_wheel()
		self.setup_page_up_down()
		self.setup_kill_window()
		self.setup_copy_paste()
		self.setup_grab_screen()
		switch_english_input_method()

	def setup_grab_screen(self):

		def grab_screen(key):
			log("grab_screen", key, self.grab_screen_pos)
			if self.grab_screen_pos[0] == (-1, -1):
				self.grab_screen_pos[0] = mouse.get_position()
				log("grab_screen begin", key, self.grab_screen_pos)
			else:
				self.grab_screen_pos[1] = mouse.get_position()
				log("do grab_screen", key, self.grab_screen_pos)
				# log(tuple(self.grab_screen_pos[0] + self.grab_screen_pos[1]))

				a, b = self.grab_screen_pos[0] 
				c, d = self.grab_screen_pos[1] 
				if a > c: 
					a, c = c, a
				if b > d: 
					b, d = d, b
				a *= 2
				b *= 2
				c *= 2
				d *= 2

				log("do grab_screen", key, a, b, c, d)
				from PIL import ImageGrab
				image = ImageGrab.grab(bbox = (a, b, c, d), all_screens=True)
				image.save("png.png")

				# parameter must be a PIL image 
				def send_to_clipboard(image):
					from io import BytesIO
					output = BytesIO()
					image.convert('RGB').save(output, 'BMP')
					data = output.getvalue()[14:]
					output.close()
					
					import win32clipboard
					win32clipboard.OpenClipboard()
					win32clipboard.EmptyClipboard()
					win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
					win32clipboard.CloseClipboard()

				send_to_clipboard(image)

				self.grab_screen_pos = [(-1, -1), (-1, -1)]

		key = Keys.grab_screen
		self.append_hotkey(key, keyboard.add_hotkey(key, partial(grab_screen, key), suppress=True))

	def setup_change_mode(self):
		def leave_normal_mode(key):
			log("leave_normal_mode %s %s", G.Mode, key)
			if G.Mode is NormalMode:
				switch_mode(InsertMode)
			else:
				keyboard.press(key)

		def enter_insert_mode(key):
			leave_normal_mode(key)
			log("enter_insert_mode")
			mouse.click()
		key = Keys.enter_insert_mode
		self.append_hotkey(key, keyboard.add_hotkey(key, partial(enter_insert_mode, key), suppress=True))

	def setup_kill_window(self):
		def kill(key):
			log("kill", key)
			mouse.click(mouse.LEFT)
			keyboard.send('alt+f4')
		key = Keys.kill
		self.append_hotkey(key, keyboard.add_hotkey(key, functools.partial(kill, key), suppress=True))

	def setup_copy_paste(self):
		def copy(key):
			log("copy")
			keyboard.send('ctrl+c')
			if self.keep_press_mouse_left_key:
				self.keep_press_mouse_left_key = False
				mouse.release(mouse.LEFT)
		key = Keys.copy
		self.append_hotkey(key, keyboard.add_hotkey(key, partial(copy, key), suppress=True))

		def paste(key):
			log("paste")
			if is_using_putty():
				mouse.click(mouse.RIGHT)
			else:
				keyboard.send('ctrl+v')
		key = Keys.paste
		self.append_hotkey(key, keyboard.add_hotkey(key, partial(paste, key), suppress=True))

	def setup_page_up_down(self):
		def page_up(key):
			exe = get_forceground_window_executable_path()
			log("page up", exe)
			if "chrome" in exe:
				n = 20
				keys = ["up" for i in range(n)]
				keys = ",".join(keys)
				keyboard.send(keys)
			else:
				keyboard.send("page up")
		key = Keys.page_up
		self.append_hotkey(key, keyboard.add_hotkey(key, partial(page_up, key), suppress=True))

		def page_down(key):
			exe = get_forceground_window_executable_path()
			log("page down", exe)
			if "chrome" in exe:
				n = 20
				keys = ["down" for i in range(n)]
				keys = ",".join(keys)
				keyboard.send(keys)
			else:
				keyboard.send("page down")
		key = Keys.page_down
		self.append_hotkey(key, keyboard.add_hotkey(key, partial(page_down, key), suppress=True))

	def setup_mouse_move(self):
		# TODO 不要这几行有没有问题
		key = 'd'
		self.append_hotkey(key, keyboard.add_hotkey(key, partial(null, key), suppress=True))
		key = 'r'
		self.append_hotkey(key, keyboard.add_hotkey(key, partial(null, key), suppress=True))
		key = 'f'
		self.append_hotkey(key, keyboard.add_hotkey(key, partial(null, key), suppress=True))

		def on_mouse_move_d(key, dx, dy):
			log("on_mouse_move_d", key, dx, dy)
			mouse.move(dx, dy, absolute=False)
		for key, (dx, dy) in Config.get("mouse_jump"):
			self.append_hotkey(key, keyboard.add_hotkey(key, partial(on_mouse_move_d, key, dx, dy), suppress=True))

		def goto_top_or_bottom(key, top):
			log("goto_top_or_bottom", key, top)
			cx, _ = mouse.get_position()
			if top:
				mouse.move(cx, 0, absolute=True)
			else:
				y = max_screen_y()
				log("goto_top_or_bottom", key, top, y)
				mouse.move(cx, y, absolute=True)

		for key, is_top in [[Keys.goto_top, True], [Keys.goto_bottom, False]]:
			self.append_hotkey(key, keyboard.add_hotkey(key, partial(goto_top_or_bottom, key, is_top), suppress=True))

	def setup_mouse_wheel(self):
		def mouse_wheel(key, delta):
			log("mouse wheel", key)
			mouse.wheel(delta)
		for key, delta in [[Keys.mouse_wheel_up, 1], [Keys.mouse_wheel_down, -1]]:
			self.append_hotkey(key, keyboard.add_hotkey(key, partial(mouse_wheel, key, delta), suppress=True))

	def setup_mouse_key(self):
		def on_press_mouse_key(key, mouse_key, key_event):
			log("mouse_key_setup press", key, mouse_key, key_event, self.keep_press_mouse_left_key)
			if self.keep_press_mouse_left_key:
				return
			mouse.press(mouse_key)

		def on_release_mouse_key(key, mouse_key, key_event):
			log("mouse_key_setup release", key, mouse_key, key_event, self.keep_press_mouse_left_key)
			if self.keep_press_mouse_left_key:
				return
			mouse.release(mouse_key)

		def on_mouse_key(key, mouse_key, key_event):
			log("mouse_key_setup on_mouse_key", key, mouse_key, key_event, self.keep_press_mouse_left_key)
			if self.keep_press_mouse_left_key:
				return
			if key_event.event_type == keyboard.KEY_DOWN:
				print "mouse press", mouse_key
				mouse.press(mouse_key)
			if key_event.event_type == keyboard.KEY_UP:
				print "mouse release", mouse_key
				mouse.release(mouse_key)

		for key, mouse_key in [[Keys.mouse_left_key, mouse.LEFT], [Keys.mouse_right_key, mouse.RIGHT]]:
			self.append_cleanup("hook_key %s" % key, keyboard.hook_key(key, partial(on_mouse_key, key, mouse_key), suppress=True))
			# self.append_cleanup("press %s" % key, keyboard.hook_key(key, partial(on_mouse_key, key, mouse_key)))

			# NOTE 这样写 keyboard 会挂 File "C:\Python27\lib\site-packages\keyboard\__init__.py", line 501, in remove_ del _hooks[key]
			# self.append_cleanup("press %s" % key, keyboard.on_press_key(key, partial(on_press_mouse_key, key, mouse_key), suppress=True))
			# self.append_cleanup("release %s" % key, keyboard.on_release_key(key, partial(on_release_mouse_key, key, mouse_key), suppress=True))

		def keep_press_mouse_left_key(key):
			log("keep_press_mouse_left_key", key, self.grab_screen_pos)
			if self.keep_press_mouse_left_key:
				self.keep_press_mouse_left_key = False
				mouse.release(mouse.LEFT)
			else:
				self.keep_press_mouse_left_key = True
				mouse.press(mouse.LEFT)

		key = Keys.keep_press_mouse_left_key
		self.append_hotkey(key, keyboard.add_hotkey(key, partial(keep_press_mouse_left_key, key), suppress=True))

def switch_mode(new_mode):
	if G.Mode is new_mode:
		return
	log("swtich_mode leave %s", G.Mode)
	G.Mode and G.Mode.leave()
	G.Mode = new_mode
	log("swtich_mode enter %s", G.Mode)
	G.Mode.enter()

def init():
	logging.basicConfig(filename = "./mouzz.log", filemode = "a", level = logging.DEBUG, format = '%(asctime)s - %(levelname)s: %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p')
	patch_keyboard.MonkeyPatch.keyboard()
	atexit.register(cleanup_all_keyboard_hook)

def main():
	init()

	Common.setup_direction_keys()
	Common.listen_alt_tab()

	switch_mode(InsertMode)

	keyboard.call_later(print_current_state, delay=2)

	frames_per_second = Config.get("mouse_move_frames")
	while True:
		time.sleep(1.0 / frames_per_second)
		MoveMouse.tick()

if __name__ == "__main__":
	main()
