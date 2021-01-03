# Script code names

SC_NAMES = {
    0x00: 'LINE_BREAK',
    0x01: 'START_LINE',
    0x02: 'END',
    0x03: 'WAIT',  # Halt with prompt (brief pause in battle if text speed is not slow)
    0x04: 'SET_FLAG',
    0x05: 'CLR_FLAG',
    0x06: 'GOTO_IF_FLAG',
    0x07: 'LOAD_FLAG',
    0x08: 'GOSUB',
    0x09: 'MULTI_GOTO',
    0x0A: 'GOTO',
    0x0B: 'CHECK_EQUAL',
    0x0C: 'CHECK_NOT_EQUAL',
    # 0x0D is handled specially
    0x0E: 'SET_COUNTER',
    0x0F: 'INC_COUNTER',
    0x10: 'PAUSE',
    0x11: 'CREATE_MENU',
    0x12: 'CLEAR_LINE',
    0x13: 'HALT',
    0x14: 'HALT_PROMPT',
    # 0x15 is dictionary decompression
    # 0x16 is dictionary decompression
    # 0x17 is dictionary decompression
}

SC_18_NAMES = {
    0x00: 'CLOSE_FOCUS_TBOX',
    0x01: 'OPEN_TBOX',
    0x02: 'SAVE_TBOX_CTX',
    0x03: 'SET_FOCUS_TBOX',
    0x04: 'CLOSE_ALL_TBOXES',
    0x05: 'ALIGN_TEXT',
    0x06: 'CLEAR_TBOX',
    0x07: 'COMPARE_REG', # [COMPARE_REG long:VALUE byte:REG] -- REG==0 -> RESULT, REG==1 -> ARG, ELSE -> COUNTER. RETURNS [0, 1, 2] BASED ON VALUE (LESS, EQUAL, GREATER)
    0x08: 'MENU_TBOX_NOCANCEL', # Unused! (Uncancellable version of 'MENU_TBOX'
    0x09: 'MENU_TBOX', # (Creates a menu in the specified textbox, WHICH MUST BE OPEN!!)
    0x0A: 'SHOW_WALLET',
    0x0D: 'DISPLAY_STATUS_OR_NULL', # Unused! [UNK_18_0D byte:character byte:action] -- action==1 -> SHOW STATUS TEXTBOX (other values do absolutely nothing)
}

SC_19_NAMES = {
    0x02: 'LOAD_STRING',
    0x04: 'FREE_STRINGS',
    0x05: 'SET_STATUS',
    0x10: 'GET_PARTY_MEMBER',
    0x11: 'GET_NAME_LETTER',
    0x14: 'GET_ESCARGO COUNTER', # Same as 0x1A, but gets item at "COUNTER REGISTER" position, has no actual args
    0x16: 'GET_STATUS_GROUP',
    0x18: 'GET_REQUIRED_EXP',
    0x19: 'GET_INV_ITEM',
    0x1A: 'GET_ESCARGO',
    0x1B: 'GET_TBOX_OPTION_COUNT', # Returns the amount of options in the argument textbox? -- IF ARG IS 0, USES FOCUSED TBOX
    0x1C: 'UNK_19_1C', # ESCARGO_UNKNOWN
    0x1D: 'UNK_19_1D', # 'GET_PENDING_ESCARGO'?
    0x1E: 'GET_DELTA',
    0x1F: 'GET_ACTION_ARG',
    0x20: 'GET_PARTY_COUNT',
    0x21: 'GET_FOOD_TYPE',
    0x22: 'GET_DIR_FROM_PMEMBER',
    0x23: 'GET_DIR_FROM_NPC',
    0x24: 'GET_DIR_FROM_OBJ',
    0x25: 'FIND_CONDIMENT',
    0x26: 'SET_RESPAWN_POINT', # Argument is index to the PSI Teleport destination table (stored into $7E98B8)
    0x27: 'GET_STAT', # Unused! (Analogous to 'PRINT_STAT', except it stores the value in the RESULT REGISTER rather than printing it)
    0x28: 'GET_STAT_LETTER',
}

SC_1A_NAMES = {
    0x00: 'SELECT_PMEMBER_NOCANCEL',
    0x01: 'SELECT_PMEMBER',
    0x04: 'CREATE_MENU_NOCANCEL',  # Unused! (Uncancellable version of 'CREATE_MENU')
    0x05: 'DISPLAY_INV',
    0x06: 'DISPLAY_SHOP',
    0x07: 'SHOW_STORED_GOODS',
    0x08: 'MENU_PERSIST_NOCANCEL', # Unused! Creates a menu, but doesn't free up the memory used by the options when done (uncancellable)
    0x09: 'MENU_PERSIST',          # Unused! Creates a menu, but doesn't free up the memory used by the options when done
    0x0A: 'PHONE_MENU',
    0x0B: 'TELEPORT_MENU'          # Unused!
}

SC_1B_NAMES = {
    0x00: 'BACKUP_REGS_LOCAL',
    0x01: 'RESTORE_REGS_LOCAL',
    0x02: 'GOTO_IF_FALSE',
    0x03: 'GOTO_IF_TRUE',
    0x04: 'SWAP_ARG_RESULT',
    0x05: 'BACKUP_REGS_GLOBAL',
    0x06: 'RESTORE_REGS_GLOBAL',
}

SC_1C_NAMES = {
    0x00: 'TEXT_COLOR',
    0x01: 'PRINT_STAT',
    0x02: 'PRINT_NAME',
    0x03: 'PRINT_LETTER',
    0x04: 'OPEN_HP_PP',
    0x05: 'PRINT_ITEM',
    0x06: 'PRINT_TELE_DEST',
    0x07: 'PRINT_STRINGS_HORZ',
    # 0x08 is handled specially
    0x09: 'NUM_PADDING',
    0x0A: 'PRINT_NUM',
    0x0B: 'PRINT_MONEY',
    0x0C: 'PRINT_STRINGS_VERT',
    0x0D: 'PRINT_ATTACKER',
    0x0E: 'PRINT_TARGET',
    0x0F: 'PRINT_DELTA',
    # 0x11 is handled specially due to differences between US and JP
    0x12: 'PRINT_PSI',
    0x13: 'BATTLE_ANIM',
    # 0x14 is handled specially
    # 0x15 is handled specially
}

SC_1D_NAMES = {
    0x00: 'GIVE_ITEM',
    0x01: 'REMOVE_ITEM',
    0x02: 'CHECK_ITEM_TYPE',
    0x03: 'INV_HAS_SPACE',
    0x04: 'CHECK_ITEM_EQUIPPED',
    0x05: 'CHECK_HAS_ITEM',
    0x06: 'ADD_ATM_MONEY',
    0x07: 'REMOVE_ATM_MONEY',
    0x08: 'ADD_MONEY',
    0x09: 'REMOVE_MONEY',
    0x0A: 'GET_ITEM_PRICE',
    0x0B: 'GET_ITEM_SELL_PRICE',
    0x0C: 'CHECK_CAN_STORE_SLOT',
    0x0D: 'CHECK_STATUS',
    0x0E: 'GIVE_ITEM_RETURN_SLOT',
    0x0F: 'REMOVE_ITEM_SLOT',
    0x10: 'CHECK_SLOT_EQUIPPED',
    0x11: 'CHECK_CAN_EQUIP_SLOT',
    0x12: 'STORE_INV_SLOT',
    0x13: 'WITHDRAW_ITEM',
    0x14: 'CHECK_HASNT_MONEY',
    0x15: 'STORE_ARG_MULT_PMEMBERS',
    0x17: 'CHECK_HAS_ATM_MONEY',
    0x18: 'STORE_ITEM',
    0x19: 'CHECK_PARTY_COUNT',
    0x20: 'CHECK_SELF_TARGETTING',
    0x21: 'RAND_RANGE',
    0x22: 'CHECK_EXIT_MOUSE',
    0x23: 'GET_ITEM_TYPE',
    0x24: 'GET_EARNED_MONEY',
}

SC_1E_NAMES = {
    0x00: 'RECOVER_HP_PERCENT',
    0x01: 'DEPLETE_HP_PERCENT',
    0x02: 'RECOVER_HP',
    0x03: 'DEPLETE_HP',
    0x04: 'RESTORE_PP_PERCENT',
    0x05: 'CONSUME_PP_PERCENT',
    0x06: 'RESTORE_PP',
    0x07: 'CONSUME_PP',
    0x08: 'SET_LEVEL',
    0x09: 'ADD_EXP',
    0x0A: 'ADD_IQ',
    0x0B: 'ADD_GUTS',
    0x0C: 'ADD_SPEED',
    0x0D: 'ADD_VITALITY',
    0x0E: 'ADD_LUCK',
}

SC_1F_NAMES = {
    0x00: 'PLAY_MUSIC',
    0x01: 'STOP_MUSIC',
    0x02: 'PLAY_SFX',
    0x03: 'RESTORE_MUSIC',
    0x04: 'TEXT_SOUND',    # TODO CONSTANTS
    0x05: 'DISALLOW_MUSIC_CHANGE',
    0x06: 'ALLOW_MUSIC_CHANGE',
    0x07: 'MUSIC_EFFECT',  # TODO CONSTANTS
    0x11: 'ADD_PMEMBER',
    0x12: 'REMOVE_PMEMBER',
    0x13: 'SET_PMEMBER_DIR',
    0x14: 'SET_PARTY_DIR',
    0x15: 'CREATE_OBJ',
    0x16: 'SET_NPC_DIR',
    0x17: 'CREATE_NPC',
    0x18: 'NOP_1',
    0x19: 'NOP_2',
    0x1A: 'CREATE_NPC_EMOTE',
    0x1B: 'DELETE_NPC_EMOTE',
    0x1C: 'CREATE_PMEMBER_EMOTE',
    0x1D: 'DELETE_PMEMBER_EMOTE',
    0x1E: 'DELETE_NPC',
    0x1F: 'DELETE_OBJ',
    0x20: 'START_TELEPORT',
    0x21: 'PRESET_TELEPORT',
    0x23: 'START_BATTLE',
    0x30: 'NORMAL_FONT',
    0x31: 'SATURN_FONT',
    0x41: 'SPECIAL_EVENT',  # Handled specially via SPECIAL_EVENT_NAMES
    0x50: 'DISABLE_INPUT',
    0x51: 'ENABLE_INPUT',
    0x52: 'NUMBER_SELECTOR',
    0x60: 'UNK_1F_60',      # Unused!
    0x61: 'WAIT_MOVEMENT',
    0x62: 'SET_PROMPT',
    0x63: 'POST_FADE_GOTO',
    0x64: 'BACKUP_PARTY',
    0x65: 'RESTORE_PARTY',
    0x66: 'ENABLE_HOTSPOT',
    0x67: 'DISABLE_HOTSPOT',
    0x68: 'SET_MOUSE_COORDS',
    0x69: 'TELEPORT_TO_MOUSE',
    0x71: 'LEARN_PSI',      # FIRST ARGUMENT IGNORED; SECOND ARGUMENT: 1 = TP ALPHA, 2 = STAR ALPHA, 3 = STAR BETA, 4 = TP BETA
    0x81: 'CHECK_CAN_EQUIP_ITEM',
    0x83: 'EQUIP_INV_SLOT',
    0x90: 'FAKE_PHONE_MENU', # Unused! Open phone menu and return selected option (don't call actual phone script) -- If the player doesn't know any phone numbers, nothing happens and returns 0
    0xA0: 'OPEN_INTERACTED_PRESENT',
    0xA1: 'CLOSE_INTERACTED_PRESENT',
    0xA2: 'CHECK_INTERACTED_PRESENT_OPENED',
    0xB0: 'SAVE_GAME',
    0xC0: 'MULTI_GOSUB',
    0xD0: 'ATTEMPT_FIX_ITEM',
    0xD1: 'GET_DIR_TO_TRUFFLE',
    0xD2: 'SHOW_PHOTOGRAPHER',
    0xD3: 'TIMED_EVENT',
    0xE1: 'SET_MAP_PAL',
    0xE4: 'SET_OBJ_DIR',
    0xE5: 'FREEZE_PMEMBER',
    0xE6: 'FREEZE_NPC',
    0xE7: 'FREEZE_OBJ',
    0xE8: 'UNFREEZE_PMEMBER',
    0xE9: 'UNFREEZE_NPC',
    0xEA: 'UNFREEZE_OBJ',
    0xEB: 'HIDE_PMEMBER',
    0xEC: 'SHOW_PMEMBER',
    0xED: 'RESTORE_MOVEMENT_1F_ED',  # ZEROES $9885 AND $98A5 (TODO: FIGURE OUT WHAT $98A5 IS!!)
    0xEE: 'TELEPORT_TO_NPC',
    0xEF: 'TELEPORT_TO_OBJ',
    0xF0: 'GET_ON_BIKE',
    0xF1: 'SET_NPC_MOVEMENT_SCRIPT',
    0xF2: 'SET_OBJ_MOVEMENT_SCRIPT',
    0xF3: 'CREATE_OBJ_EMOTE',
    0xF4: 'DELETE_OBJ_EMOTE'
}

SPECIAL_EVENT_NAMES = (
    'SHOW_COFFEE',              # 01
    'SHOW_TEA',                 # 02
    'REGISTER_NAME',            # 03
    'REGISTER_NAME_KANA',       # 04
    'SET_OSS_FLAG',             # 05
    'RESET_OSS_FLAG',           # 06
    'TRY_SHOW_MAP',             # 07
    'CHECK_IS_ATTACKER_ENEMY',  # 08
    'SOUND_STONE',              # 09
    'SHOW_TITLE_SCREEN',        # 0A
    'SHOW_CAST',                # 0B
    'SHOW_CREDITS',             # 0C
    'START_ROLLING_METER',      # 0D
    'STOP_ROLLING_METER',       # 0E
    'CLEAR_ALL_FLAGS',          # 0F
    'SOUND_STONE_FULL',         # 10
    'ATTEMPT_HOMESICKNESS',     # 11
    'KICK_OUT_OF_BICYCLE'       # 12 This is used right before the photo man starts speaking
)
