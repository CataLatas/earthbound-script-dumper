# Script code names

SC_NAMES = {
    0x00: 'linebreak',
    0x01: 'newline',
    0x02: 'eob',
    0x03: 'prompt2',  # Halt with prompt (brief pause in battle if text speed is not slow)
    0x04: 'set',
    0x05: 'unset',
    0x06: 'goto_ifset',
    0x07: 'isset',
    0x08: 'call',
    0x09: 'switch',
    0x0A: 'goto',
    0x0B: 'result_is',
    0x0C: 'result_not',
    # 0x0D is handled specially
    0x0E: 'counter',
    0x0F: 'inc',
    0x10: 'pause',
    0x11: 'menu',
    0x12: 'clearline',
    0x13: 'wait',
    0x14: 'prompt',
    # 0x15 is dictionary decompression
    # 0x16 is dictionary decompression
    # 0x17 is dictionary decompression
}

SC_18_NAMES = {
    0x00: 'window_closetop',
    0x01: 'window_open',
    0x02: 'save_window_context',
    0x03: 'window_switch',
    0x04: 'window_closeall',
    0x05: 'text_pos',
    0x06: 'window_clear',
    0x07: 'compare_reg',
    0x08: 'window_menu_nocancel', # Unused! (Uncancellable version of 'MENU_TBOX'
    0x09: 'window_menu', # (Creates a menu in the specified textbox, WHICH MUST BE OPEN!!)
    0x0A: 'open_wallet',
    0x0D: 'show_status_or_null', # Unused! [UNK_18_0D byte:character byte:action] -- action==1 -> SHOW STATUS TEXTBOX (other values do absolutely nothing)
}

SC_19_NAMES = {
    0x02: 'add_option',
    0x04: 'clear_options',
    0x05: 'inflict',
    0x10: 'get_char',
    0x11: 'get_name_letter',
    0x14: 'get_escargo_counter', # Same as 0x1A, but gets item at "COUNTER REGISTER" position, has no actual args
    0x16: 'get_status',
    0x18: 'get_required_exp',
    0x19: 'get_inventory',
    0x1A: 'get_escargo',
    0x1B: 'window_option_count', # Returns the amount of options in the argument textbox? -- IF ARG IS 0, USES FOCUSED TBOX
    0x1C: 'unk_19_1C', # ESCARGO_UNKNOWN
    0x1D: 'unk_19_1D', # 'GET_PENDING_ESCARGO'?
    0x1E: 'get_delta',
    0x1F: 'get_action_argument',
    0x20: 'get_party_size',
    0x21: 'get_food_type',
    0x22: 'get_dir_from_char',
    0x23: 'get_dir_from_npc',
    0x24: 'get_dir_from_obj',
    0x25: 'find_condiment',
    0x26: 'set_respawn_point', # Argument is index to the PSI Teleport destination table (stored into $7E98B8)
    0x27: 'get_stat', # Unused! (Analogous to 'PRINT_STAT', except it stores the value in the RESULT REGISTER rather than printing it)
    0x28: 'get_stat_letter',
}

SC_1A_NAMES = {
    0x00: 'select_char_nocancel',
    0x01: 'select_char',
    0x04: 'menu_nocancel',  # Unused! (Uncancellable version of 'CREATE_MENU')
    0x05: 'show_inventory',
    0x06: 'show_shop',
    0x07: 'show_escargo',
    0x08: 'menu_persist_nocancel', # Unused! Creates a menu, but doesn't free up the memory used by the options when done (uncancellable)
    0x09: 'menu_persist',          # Unused! Creates a menu, but doesn't free up the memory used by the options when done
    0x0A: 'phone_menu',
    0x0B: 'teleport_menu'          # Unused!
}

SC_1B_NAMES = {
    0x00: 'store_registers',
    0x01: 'load_registers',
    0x02: 'goto_false',
    0x03: 'goto_true',
    0x04: 'swap',
    0x05: 'store_registers_global',
    0x06: 'load_registers_global',
}

SC_1C_NAMES = {
    0x00: 'text_color',
    0x01: 'stat',
    0x02: 'name',
    0x03: 'letter',
    0x04: 'open_hp',
    0x05: 'itemname',
    0x06: 'teleportname',
    0x07: 'build_menu_horizontal',
    # 0x08 is handled specially
    0x09: 'number_padding',
    0x0A: 'number',
    0x0B: 'money',
    0x0C: 'build_menu_vertical',
    0x0D: 'user',
    0x0E: 'target',
    0x0F: 'delta',
    # 0x11 is handled specially due to differences between US and JP
    0x12: 'psiname',
    0x13: 'battle_anim',
    # 0x14 is handled specially
    # 0x15 is handled specially
}

SC_1D_NAMES = {
    0x00: 'give',
    0x01: 'take',
    0x02: 'is_item_of_type',
    0x03: 'notfull',
    0x04: 'hasequipment',
    0x05: 'hasitem',
    0x06: 'deposit',
    0x07: 'withdraw',
    0x08: 'givemoney',
    0x09: 'takemoney',
    0x0A: 'get_item_price',
    0x0B: 'get_item_sell_price',
    0x0C: 'can_store_item',
    0x0D: 'has_status',
    0x0E: 'give_return_slot',
    0x0F: 'take_slot',
    0x10: 'is_slot_equipped',
    0x11: 'can_equip_slot',
    0x12: 'store_slot',
    0x13: 'withdraw_item',
    0x14: 'hasmoney',
    0x15: 'number_per_person',  # argument * party_size
    0x17: 'has_bankmoney',
    0x18: 'store_item',
    0x19: 'check_party_size',
    0x20: 'is_self_targetting',
    0x21: 'rand_range',
    0x22: 'can_use_exit_mouse',
    0x23: 'get_item_type',
    0x24: 'get_earned_money',
}

SC_1E_NAMES = {
    0x00: 'heal_percent',
    0x01: 'hurt_percent',
    0x02: 'heal',
    0x03: 'hurt',
    0x04: 'recoverpp_percent',
    0x05: 'consumepp_percent',
    0x06: 'recoverpp',
    0x07: 'consumepp',
    0x08: 'change_level',
    0x09: 'boost_exp',
    0x0A: 'boost_iq',
    0x0B: 'boost_guts',
    0x0C: 'boost_speed',
    0x0D: 'boost_vitality',
    0x0E: 'boost_luck',
}

SC_1F_NAMES = {
    0x00: 'music',
    0x01: 'music_stop',
    0x02: 'sound',
    0x03: 'music_resume',
    0x04: 'text_blips',    # TODO CONSTANTS
    0x05: 'music_switching_off',
    0x06: 'music_switching_on',
    0x07: 'music_effect',  # TODO CONSTANTS
    0x11: 'party_add',
    0x12: 'party_remove',
    0x13: 'char_direction',
    0x14: 'party_direction',
    0x15: 'create_sprite',
    0x16: 'npc_direction',
    0x17: 'create_npc',
    0x18: 'nop1',
    0x19: 'nop2',
    0x1A: 'show_npc_emote',
    0x1B: 'delete_npc_emote',
    0x1C: 'show_char_emote',
    0x1D: 'delete_char_emote',
    0x1E: 'delete_npc',
    0x1F: 'delete_sprite',
    0x20: 'teleport',
    0x21: 'warp',
    0x23: 'start_battle',
    0x30: 'font_normal',
    0x31: 'font_saturn',
    0x41: 'event',  # Handled specially via SPECIAL_EVENT_NAMES
    0x50: 'disable_input',
    0x51: 'enable_input',
    0x52: 'number_input',
    0x60: 'wait_input_timeout',      # Unused!
    0x61: 'wait_movement',
    0x62: 'set_prompt',
    0x63: 'on_map_refresh',
    0x64: 'backup_party',
    0x65: 'restore_party',
    0x66: 'enable_hotspot',
    0x67: 'disable_hotspot',
    0x68: 'set_exit_mouse',
    0x69: 'warp_exit_mouse',
    0x71: 'learn_psi',      # FIRST ARGUMENT IGNORED; SECOND ARGUMENT: 1 = TP ALPHA, 2 = STAR ALPHA, 3 = STAR BETA, 4 = TP BETA
    0x81: 'usable',  # can_equip_item
    0x83: 'equip_slot',
    0x90: 'select_phone',  # Unused! Open phone menu and return selected option (don't call actual phone script) -- If the player doesn't know any phone numbers, nothing happens and returns 0
    0xA0: 'open_present',
    0xA1: 'close_present',
    0xA2: 'is_present_open',
    0xB0: 'save_game',
    0xC0: 'switch_call',
    0xD0: 'attempt_fix_item',
    0xD1: 'get_truffle_dir',
    0xD2: 'show_photographer',
    0xD3: 'timed_event',
    0xE1: 'set_map_pal',
    0xE4: 'set_sprite_direction',
    0xE5: 'freeze_char',
    0xE6: 'freeze_npc',
    0xE7: 'freeze_sprite',
    0xE8: 'unfreeze_char',
    0xE9: 'unfreeze_npc',
    0xEA: 'unfreeze_sprite',
    0xEB: 'hide_char',
    0xEC: 'show_char',
    0xED: 'unfocus_camera',
    0xEE: 'camera_focus_npc',
    0xEF: 'camera_focus_sprite',
    0xF0: 'get_on_bike',
    0xF1: 'set_npc_movement',
    0xF2: 'set_sprite_movement',
    0xF3: 'show_sprite_emote',
    0xF4: 'delete_sprite_emote'
}

SPECIAL_EVENT_NAMES = (
    'show_coffee',               # 01
    'show_tea',                  # 02
    'register_player_name',      # 03
    'register_player_name_kana', # 04
    'set_oss_flag',              # 05
    'reset_oss_flag',            # 06
    'try_show_map',              # 07
    'is_attacker_enemy',         # 08
    'sound_stone',               # 09
    'show_title_screen',         # 0A
    'show_cast',                 # 0B
    'show_credits',              # 0C
    'start_rolling_meter',       # 0D
    'stop_rolling_meter',        # 0E
    'unset_all_flags',           # 0F
    'sound_stone_full',          # 10
    'attempt_homesickness',      # 11
    'kick_out_of_bicycle'        # 12 This is used right before the photo man starts speaking
)
