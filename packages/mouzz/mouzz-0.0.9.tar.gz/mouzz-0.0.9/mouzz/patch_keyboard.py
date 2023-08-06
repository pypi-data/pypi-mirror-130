# encoding: utf8

import keyboard
from utils import *

code =  '''
def add_hotkey(hotkey, callback, args=(), suppress=False, timeout=1, trigger_on_release=False):
    """
    Invokes a callback every time a hotkey is pressed. The hotkey must
    be in the format `ctrl+shift+a, s`. This would trigger when the user holds
    ctrl, shift and "a" at once, releases, and then presses "s". To represent
    literal commas, pluses, and spaces, use their names ('comma', 'plus',
    'space').

    - `args` is an optional list of arguments to passed to the callback during
    each invocation.
    - `suppress` defines if successful triggers should block the keys from being
    sent to other programs.
    - `timeout` is the amount of seconds allowed to pass between key presses.
    - `trigger_on_release` if true, the callback is invoked on key release instead
    of key press.

    The event handler function is returned. To remove a hotkey call
    `remove_hotkey(hotkey)` or `remove_hotkey(handler)`.
    before the hotkey state is reset.

    Note: hotkeys are activated when the last key is *pressed*, not released.
    Note: the callback is executed in a separate thread, asynchronously. For an
    example of how to use a callback synchronously, see `wait`.

    Examples:

        # Different but equivalent ways to listen for a spacebar key press.
        add_hotkey(' ', print, args=['space was pressed'])
        add_hotkey('space', print, args=['space was pressed'])
        add_hotkey('Space', print, args=['space was pressed'])
        # Here 57 represents the keyboard code for spacebar; so you will be
        # pressing 'spacebar', not '57' to activate the print function.
        add_hotkey(57, print, args=['space was pressed'])

        add_hotkey('ctrl+q', quit)
        add_hotkey('ctrl+alt+enter, space', some_callback)
    """
    if args:
        callback = lambda callback=callback: callback(*args)

    _listener.start_if_necessary()

    steps = parse_hotkey_combinations(hotkey)

    event_type = KEY_UP if trigger_on_release else KEY_DOWN
    if len(steps) == 1:
        # Deciding when to allow a KEY_UP event is far harder than I thought,
        # and any mistake will make that key "sticky". Therefore just let all
        # KEY_UP events go through as long as that's not what we are listening
        # for.
        handler = lambda e: (event_type == KEY_DOWN and e.event_type == KEY_UP and e.scan_code in _logically_pressed_keys) or (event_type == e.event_type and callback())
        remove_step = _add_hotkey_step(handler, steps[0], suppress)
        def remove_():
            remove_step()
            del _hotkeys[hotkey]
            del _hotkeys[remove_]
            del _hotkeys[callback]
        # TODO: allow multiple callbacks for each hotkey without overwriting the
        # remover.
        _hotkeys[hotkey] = _hotkeys[remove_] = _hotkeys[callback] = remove_
        return remove_

    state = _State()
    state.remove_catch_misses = lambda: None
    state.remove_last_step = None
    state.suppressed_events = []
    state.last_update = float('-inf')
    
    def catch_misses(event, force_fail=False):
        if (
                event.event_type == event_type
                and state.index
                and event.scan_code not in allowed_keys_by_step[state.index]
            ) or (
                timeout
                and _time.monotonic() - state.last_update >= timeout
            ) or force_fail: # Weird formatting to ensure short-circuit.

            state.remove_last_step()

            for event in state.suppressed_events:
                if event.event_type == KEY_DOWN:
                    press(event.scan_code)
                else:
                    release(event.scan_code)
            del state.suppressed_events[:]

            index = 0
            set_index(0)
        return True

    def set_index(new_index):
        state.index = new_index

        if new_index == 0:
            # This is done for performance reasons, avoiding a global key hook
            # that is always on.
            state.remove_catch_misses() 
            state.remove_catch_misses = lambda: None
        elif new_index == 1:
            state.remove_catch_misses()
            # Must be `suppress=True` to ensure `send` has priority.
            state.remove_catch_misses = hook(catch_misses, suppress=True)

        if new_index == len(steps) - 1:
            def handler(event):
                if event.event_type == KEY_UP:
                    remove()
                    set_index(0)
                accept = event.event_type == event_type and callback() 
                if accept:
                    return catch_misses(event, force_fail=True)
                else:
                    state.suppressed_events[:] = [event]
                    return False
            remove = _add_hotkey_step(handler, steps[state.index], suppress)
        else:
            # Fix value of next_index.
            def handler(event, new_index=state.index+1):
                if event.event_type == KEY_UP:
                    remove()
                    set_index(new_index)
                state.suppressed_events.append(event)
                return False
            remove = _add_hotkey_step(handler, steps[state.index], suppress)
        state.remove_last_step = remove
        state.last_update = _time.monotonic()
        return False
    set_index(0)

    allowed_keys_by_step = [
        set().union(*step)
        for step in steps
    ]

    def remove_():
        state.remove_catch_misses()
        state.remove_last_step()
        del _hotkeys[hotkey]
        del _hotkeys[remove_]
        del _hotkeys[callback]
    # TODO: allow multiple callbacks for each hotkey without overwriting the
    # remover.
    _hotkeys[hotkey] = _hotkeys[remove_] = _hotkeys[callback] = remove_
    return remove_

register_hotkey = add_hotkey
'''

exec(code, keyboard.__dict__)

@singleton
class MonkeyPatch(object):

	def keyboard(self):
		mouzz_log("MonkeyPatch.keyboard")
		f = keyboard.key_to_scan_codes
		mapping = {}
		cache = {}
		def key_to_scan_codes(key, error_if_missing=True):
			if key in cache:
				sv = f(key, error_if_missing)
				if sv != cache[key]:
					log("key_to_scan_codes key %s error_if_missing %s sv %s cache[key] %s", key, error_if_missing, svn, cache[key])
					os.exit(1)
				return cache[key]
			v = f(key, error_if_missing)
			if type(v) is tuple:
				for e in v:
					if e not in mapping:
						mapping[e] = key
			else:
				mapping[v] = key
			cache[key] = v
			log("key_to_scan_codes key %s error_if_missing %s v %s", key, error_if_missing, v)
			return v
		keyboard.key_to_scan_codes = key_to_scan_codes

		# NOTE 这个函数不存在 只是用来 debug
		def scan_codes_to_key(v):
			if type(v) is tuple:
				return tuple([mapping.get(k, k) for k in v])
			return mapping.get(v, v)
		keyboard.scan_codes_to_key = scan_codes_to_key
		
		# keyboard 模块不知道为什么有时候会有 vk == 7 scan_code == 0 的 down 事件 却没有的 up 事件
		# return callback(KeyboardEvent(event_type=event_type, scan_code=scan_code or -vk, name=name, is_keypad=is_keypad))
		# 导致 _pressed_events 会残留一个 -7，所有的 hotkey 都会多了一个 -7 的组合，影响到 hotkey 的判断

		_direct_callback = keyboard._KeyboardListener.__dict__["direct_callback"]
		def direct_callback(self, event):
			ret = _direct_callback(self, event)
			shit = False
			for k, v in keyboard._pressed_events.items():
				if k < 0:
					del keyboard._pressed_events[k]
					log("!" * 79)
					log("delete invalid _pressed_events", k)
					log("!" * 79)
					shit = True
			if shit:
				os.exit(1)
			return ret
		setattr(keyboard._KeyboardListener, "direct_callback", direct_callback)

