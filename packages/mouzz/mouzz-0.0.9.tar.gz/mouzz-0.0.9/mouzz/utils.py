# encoding: utf8

import os
import time
import types
import ctypes
import atexit
import logging
import functools
import threading

import mouse
import keyboard

from functools import partial

# buildin
#=============================================================================
builtins = globals()["__builtins__"]
if type(builtins) is types.ModuleType:
	builtins = builtins.__dict__

# log
#=============================================================================

lock = threading.Lock()

def tostr(s):
	if type(s) is unicode:
		return s.encode('utf8')
	return s

def mouzz_log(fmt, *args):
	if args:
		try:
			fmt = fmt % args
		except TypeError:
			fmt = fmt + " " + " ".join([str(tostr(arg)) for arg in args])

	fmt = time.strftime("%Y-%m-%d %H:%M:%S") + " " + str(threading.current_thread().ident) + " " + fmt
	with lock:
		print(fmt)
		logging.info(fmt)

log = mouzz_log

# for debug keyboard module
builtins["mouzz_log"] = log 

# python
#=============================================================================

def singleton(klass):
	return klass()

def print_object_dir(obj):
	for attr in dir(obj):
		log("  ", attr, getattr(obj, attr, "..."))

# screen
#=============================================================================

def max_screen_y():
	user32 = ctypes.windll.user32
	# screensize = user32.GetSystemMetrics(0), 
	y = user32.GetSystemMetrics(1)
	return y

# state
#=============================================================================

def print_current_state(repeat=True):
	return
	log("-" * 79)
	if repeat: 
		keyboard.call_later(print_current_stat, delay=2)

	if G.Mode is NormalMode:
		log("In NormalMode", mouse.get_position())
	else:
		log("In InsertMode", mouse.get_position())

	l = []
	for key in keyboard._hooks.keys():
		if type(key) is str:
			l.append(key)
	log("hook key", " ".join(l))
	l = []
	for key in keyboard._hotkeys.keys():
		if type(key) is str:
			l.append(key)
	log("hot key", " ".join(l))

	l = []
	for key in keyboard.all_modifiers:
		if keyboard.is_pressed(key):
			l.append(key)
	log("modifer key", " ".join(l))

	l = []
	for k, v in keyboard._listener.blocking_hotkeys.items():
		if v:
			l.append((keyboard.scan_codes_to_key(k), k))
	log("hot keys cb", l)
	# log("get_forceground_window", get_forceground_window())

	user32 = ctypes.WinDLL('user32', use_last_error=True)
	curr_window = user32.GetForegroundWindow()
	thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
	klid = user32.GetKeyboardLayout(thread_id)
	lid = klid & (2**16 - 1)
	lid_hex = hex(lid)
	 
	print(klid, lid, lid_hex)
	print(klid, lid, lid_hex)
	print(klid, lid, lid_hex)
	# if lid_hex == '0x409':
	#     print(u'当前的输入法状态是英文输入模式\n\n')
	# elif lid_hex == '0x804':
	#     print(u'当前的输入法是中文输入模式\n\n')
	# else:
	#     print(u'当前的输入法既不是英文输入也不是中文输入\n\n')

	# global IME
	# if IME == 0x0409:
	# 	switch_input_method(0x0804)
	# else:
	# 	switch_input_method(0x0409)
	log("-" * 79)

# windows
#=============================================================================

def get_forceground_window():
	from win32gui import GetWindowText, GetForegroundWindow
	return GetWindowText(GetForegroundWindow())

def get_forceground_window_executable_path():
	from win32gui import GetForegroundWindow
	import win32process, psutil
	pid = win32process.GetWindowThreadProcessId(GetForegroundWindow())
	return psutil.Process(pid[-1]).exe()

def is_using_putty():
	return "putty" in get_forceground_window_executable_path().lower()

def is_using_chrome():
	return "chrome" in get_forceground_window_executable_path().lower()

def move_mouse_to_actived_window():
	from win32gui import GetWindowText, GetForegroundWindow, GetWindowRect
	hwnd = GetForegroundWindow()
	text = GetWindowText(hwnd)
	if type(text) is str: 
		try:
			text = text.decode("utf8")
		except Exception, e:
			try:
				text = text.decode("gbk")
			except Exception, e:
				pass
	if text == u"任务切换":
		return
	rect = GetWindowRect(hwnd)
	x0, y0, x1, y1 = rect
	log("-" * 79)
	log(text)
	log("move_mouse_to_actived_window", text, rect)
	mouse.move((x0 + x1) / 2, (y0 + y1) / 2, absolute=True)
	# mouse.move(x0 + 100, y0 + 100, absolute=True)

# mouse
#=============================================================================

def change_mouse_cursor():
	return
	import win32gui, ctypes, win32con
	hold = win32gui.LoadImage(0, 32512, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED )
	hsave = ctypes.windll.user32.CopyImage(hold, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)
	path = r"C:\Windows\Cursors\move_m.cur"
	hnew = win32gui.LoadImage(0, path, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE);
	ctypes.windll.user32.SetSystemCursor(hnew, 32512)
	time.sleep(10)
	# restore the old cursor
	ctypes.windll.user32.SetSystemCursor(hsave, 32512)

# keyboard
#=============================================================================

"""
- on_press / on_release 面向任何键
  - hook
  - unhook
  - blocking_hooks
	- suppress
	  - 在 _KeyboardListener.direct_callback() 中所有的 event 会先被 blocking_hooks 处理
	  - 可以中途返回
  - add_handler / remove_handler
	- 非 suppress
	  - 在 _KeyboardListener.direct_callback() 中所有的 event 无条件放到 self.queue
	  - 进而被 handlers 在另外一个线程单独处理

- on_press_key / on_release_key / block_key 面向单个键
  - hook_key
  - unkook_key / unblock_key
  - blocking_keys
	- suppress
	  - 在 _KeyboardListener.direct_callback() 中所有的 event 在处理 blocking_hooks 之后会处理 blocking_keys
	  - 可以中途返回
  - nonblocking_keys
	- 非 suppress
	  - 在 _KeyboardListener.direct_callback() 中所有的 event 无条件放到 self.queue
	  - 进而被 pre_process_event 在另外一个线程单独处理

- add_hotkey hotkey 不能区分按下按起的两种事件
  - remove_hotkey
  - remove_all_hotkey
  - remap_hotkey
  - blocking_hotkeys
	- suppress
	  - 在 _KeyboardListener.direct_callback() 中所有的 event 在处理 blocking_keys 之后会处理 blocking_hotkeys
  - nonblocking_hotkeys
	- 非 suppress
	  - 在 _KeyboardListener.direct_callback() 中所有的 event 无条件放到 self.queue
	  - 进而被 pre_process_event 在另外一个线程单独处理


"""

def null(key):
	log("null", key)

def cleanup_all_keyboard_hook(*args, **kw):
	log("cleanup_all_keyboard_hook")
	keyboard.unhook_all()

# input method
#=============================================================================

IME = 0x0409

def switch_chinese_input_method():
	switch_input_method(ime=0x0804)

def switch_english_input_method():
	switch_input_method(ime=0x0409)

def switch_input_method(ime=0x0409):
	from win32con import WM_INPUTLANGCHANGEREQUEST
	import win32gui
	import win32api
	
	# 语言代码
	# https://msdn.microsoft.com/en-us/library/cc233982.aspx
	LID = {0x0804: "Chinese (Simplified) (People's Republic of China)",
	       0x0409: 'English (United States)'}
	
	# 获取前景窗口句柄
	hwnd = win32gui.GetForegroundWindow()
	
	# 获取前景窗口标题
	title = win32gui.GetWindowText(hwnd)
	# print(u'当前窗口：' + title)
	
	# 获取键盘布局列表
	im_list = win32api.GetKeyboardLayoutList()
	im_list = list(map(hex, im_list))
	
	# 设置键盘布局为英文
	result = win32api.SendMessage(
	    hwnd,
	    WM_INPUTLANGCHANGEREQUEST,
	    0,
	    ime)
	if result == 0:
		global IME
		IME = ime
	log('switch_input_method', im_list, ime, result)

