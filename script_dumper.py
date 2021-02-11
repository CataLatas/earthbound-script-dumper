#!/usr/bin/python3

import os
import string
import sys

from collections import namedtuple
from enum import Enum

import constants

class RomVersion(Enum):
    US = 0
    US_PROTO = 1
    JP = 2

SCRIPT_BLOCKS_PER_VERSION = {
    RomVersion.US: constants.SCRIPT_BLOCKS_US,
    RomVersion.US_PROTO: constants.SCRIPT_BLOCKS_US_PROTO,
    RomVersion.JP: constants.SCRIPT_BLOCKS_JP
}

Symbol = namedtuple('Symbol', 'label comment', defaults=[None])

class ScriptDumper(object):
    def __init__(self, rom_file, out_file, version, symbols, header_offset):
        self.rom_file = rom_file
        self.out_file = out_file
        self.version = version
        self.header_offset = header_offset
        self.dictionary = []  # Populated on "build_dictionary", but only if RomVersion is not JP
        self.translate_chr = m2_chr if version == RomVersion.JP else eb_chr
        self.inside_string = False
        self.was_linebreak = False
        self.should_add_label = False
        self.symbols = symbols

    @property
    def address(self):
        return self.rom_file.tell()

    @property
    def snes_address(self):
        return pc_to_snes(self.address - self.header_offset)

    def read_int(self, size, signed=False):
        bytes_ = self.rom_file.read(size)
        return int.from_bytes(bytes_, byteorder='little', signed=signed)

    def peek_int(self, size, signed=False):
        bytes_ = self.rom_file.peek(size)
        return int.from_bytes(bytes_[:size], byteorder='little', signed=signed)

    def read_address(self):
        addr = self.read_int(4)

        if addr not in self.symbols:
            self.add_new_label(addr)

        return self.symbols[addr].label

    def read_flag(self):
        flag_id = self.read_int(2)
        return constants.FLAG_NAMES.get(flag_id, 'flag {}'.format(flag_id))

    def read_stat(self):
        stat_id = self.read_int(1)
        return list_get_default(constants.STAT_NAMES, stat_id, stat_id)

    def read_item(self):
        item_id = self.read_int(1)
        return list_get_default(constants.ITEM_NAMES, item_id, item_id)

    def read_emote(self):
        # TODO: IS EMOTE 00 A REPLACEMENT VIA REGISTER??
        emote_id = self.read_int(1)
        return list_get_default(constants.EMOTE_NAMES, emote_id-1, emote_id)

    def read_party_member(self, replace_00=None, replace_FF=None):
        char_id = self.read_int(1)
        if char_id == 0 and replace_00 is not None:
            return replace_00
        elif char_id == 0xFF and replace_FF is not None:
            return replace_FF
        else:
            return list_get_default(constants.PARTY_MEMBERS, char_id-1, char_id)

    def read_chosen_four(self, replace_00=None, replace_FF=None):
        char_id = self.read_int(1)
        if char_id == 0 and replace_00 is not None:
            return replace_00
        elif char_id == 0xFF and replace_FF is not None:
            return replace_FF
        else:
            return list_get_default(constants.CHOSEN_FOUR, char_id-1, char_id)

    def read_status(self):
        '''Returns a tuple containing status (group, value)'''

        group_id = self.read_int(1)
        value_id = self.read_int(1)
        group = list_get_default(constants.STATUS_GROUPS, group_id-1, group_id)
        value = list_get_default(constants.STATUS_NAMES[group_id-1], value_id, value_id)
        return (group, value)

    def read_type_and_obj(self):
        '''Returns a tuple containing (type, value)'''

        type_id = self.read_int(1)
        type_ = list_get_default(constants.GET_DIR_FROM_TYPES, type_id-1, type_id)

        if type_id == 1:
            value = self.read_party_member(replace_00='result', replace_FF='leader')
            self.read_int(1)  # This byte is ignored since a party member is a 1-byte value, but 2 bytes are always read to compensate for the NPC/OBJ case
        else:
            # Types 2 and 3 are NPC and OBJ, which don't really have constants
            value = self.read_int(2)

        return (type_, value)

    def read_register(self):
        reg_id = self.read_int(1)
        return list_get_default(constants.REGISTERS, reg_id, reg_id)

    def build_dictionary(self):
        dict_ptrs = 0x08CDED if self.version == RomVersion.US else 0x05F2C3
        self.rom_file.seek(dict_ptrs + self.header_offset)  # Pointers to text used in the dictionary compression

        dict_text_ptr = snes_to_pc(self.read_int(4))
        self.rom_file.seek(dict_text_ptr + self.header_offset)

        for i in range(256*3):
            chars = []

            c = self.read_int(1)
            while c != 0:
                chars.append(self.translate_chr(c))
                c = self.read_int(1)

            self.dictionary.append(''.join(chars))

    def resolve_labels(self):
        # wtf very hacky
        npc_config_addr = 0x0F89C1 if self.version == RomVersion.JP else 0x0F8985
        self.rom_file.seek(npc_config_addr + 9)  # sizeof == 17, offsetof(text_ptr) == 9
        for npc in range(constants.NPC_COUNT):
            text_ptr = self.read_int(3)
            if text_ptr != 0:
                self.add_new_label(text_ptr, 'Npc{:04d}'.format(npc))

            self.rom_file.seek(17-3, os.SEEK_CUR)

        script_blocks = SCRIPT_BLOCKS_PER_VERSION[self.version]
        for start, size in script_blocks:
            end = start + size + self.header_offset
            self.rom_file.seek(start + self.header_offset)

            self.should_add_label = True
            while self.address < end:
                if self.should_add_label:
                    self.add_new_label(self.snes_address)

                c = self.read_int(1)
                if 0x15 <= c <= 0x17 and self.version != RomVersion.JP:
                    self.read_int(1)  # Consume dictionary index
                elif c < 0x20:
                    self.get_script_code_string(c)  # Consume bytes that make up this script code

    def add_new_label(self, addr, label=None):
        self.should_add_label = False

        if label is None:
            label = 'L_{:06X}'.format(addr)

        if addr not in self.symbols:
            self.symbols[addr] = Symbol(label)

    def get_script_code_string(self, sc):
        '''Warning: very unreadable code!!'''

        args = []
        sc_name = constants.SC_NAMES.get(sc, 'unk_{:02X}'.format(sc))
        line_break = sc not in {0x0F, 0x10}

        if sc in {0x04, 0x05, 0x07}:
            args.append(self.read_flag())
        elif sc in {0x08, 0x0A}:
            args.append(self.read_address())
        elif sc in {0x0B, 0x0C, 0x0E, 0x10}:
            args.append(self.read_int(1))
        elif sc == 0x03:  # prompt2
            if self.peek_int(1) == 0x00:  # linebreak
                self.read_int(1)  # Consume linebreak
                sc_name = 'next'
        elif sc == 0x13:  # wait
            if self.peek_int(1) == 0x02:  # eob
                self.read_int(1)  # Consume eob
                sc_name = 'end'
        elif sc == 0x0D:
            sc_name = 'rtoarg' if self.read_int(1) == 0 else 'ctoarg'
        elif sc == 0x06:
            args.append(self.read_flag())
            args.append(self.read_address())
        elif sc == 0x09:
            count = self.read_int(1)
            args += [self.read_address() for _ in range(count)]
        elif sc == 0x18:
            sub_sc = self.read_int(1)
            sc_name = constants.SC_18_NAMES.get(sub_sc, 'unk_18_{:02X}'.format(sub_sc))

            if sub_sc in {0x01, 0x03, 0x08, 0x09}:
                args.append(self.read_int(1))
            elif sub_sc == 0x05:
                args.append(self.read_int(1))
                args.append(self.read_int(1))
            elif sub_sc == 0x07:
                value = self.read_int(4)
                args.append(self.read_register())
                args.append(value)
            elif sub_sc == 0x0D:
                args.append(self.read_chosen_four(replace_00='result'))
                args.append(self.read_int(1))
        elif sc == 0x19:
            sub_sc = self.read_int(1)
            sc_name = constants.SC_19_NAMES.get(sub_sc, 'unk_19_{:02X}'.format(sub_sc))

            if sub_sc == 0x02:
                chars = [self.translate_chr(self.read_int(1))]  # This is accurate to the game implementation. It's impossible to have an empty string

                c = self.read_int(1)
                while c not in {0x01, 0x02}:  # 0x01 = end and run another script, 0x02 = end
                    chars.append(self.translate_chr(c))
                    c = self.read_int(1)

                args.append('"{}"'.format(''.join(chars)))
                if c == 0x01:  # 0x01 = end and run another script
                    sc_name = 'add_option_with_callback'
                    args.append(self.read_address())
            elif sub_sc == 0x22:
                args.append(self.read_party_member(replace_00='argument', replace_FF='leader'))
                args += self.read_type_and_obj()
            elif sub_sc == 0x23:
                args.append(self.read_int(2))  # NPC ID
                args += self.read_type_and_obj()
            elif sub_sc == 0x24:
                args.append(self.read_int(2))  # OBJ TYPE
                args += self.read_type_and_obj()
            elif sub_sc == 0x05:
                args.append(self.read_party_member(replace_00='result'))
                args += self.read_status()
            elif sub_sc == 0x16:
                args.append(self.read_int(1))
                group_id = self.read_int(1)
                group = list_get_default(constants.STATUS_GROUPS, group_id-1, group_id)
                args.append(group)
            elif sub_sc in {0x11, 0x18}:
                args.append(self.read_chosen_four(replace_00='argument'))
            elif sub_sc == 0x19:
                args.append(self.read_chosen_four(replace_00='result'))
                args.append(self.read_int(1))
            elif sub_sc in {0x1C, 0x1D}:
                args.append(self.read_int(1))
                args.append(self.read_int(1))
            elif sub_sc in {0x10, 0x18, 0x1A, 0x1B, 0x21, 0x25, 0x26}:
                args.append(self.read_int(1))
            elif sub_sc in {0x27, 0x28}:
                args.append(self.read_stat())
        elif sc == 0x1A:
            sub_sc = self.read_int(1)
            sc_name = constants.SC_1A_NAMES.get(sub_sc, 'unk_1A_{:02X}'.format(sub_sc))

            if sub_sc in {0x00, 0x01}:
                args.append(self.read_address())
                args.append(self.read_address())
                args.append(self.read_address())
                args.append(self.read_address())
                args.append(self.read_int(1))
            elif sub_sc == 0x05:
                args.append(self.read_int(1))
                args.append(self.read_chosen_four(replace_00='argument'))
            elif sub_sc == 0x06:
                args.append(self.read_int(1))
        elif sc == 0x1B:
            sub_sc = self.read_int(1)
            sc_name = constants.SC_1B_NAMES.get(sub_sc, 'unk_1B_{:02X}'.format(sub_sc))

            if sub_sc in {0x02, 0x03}:
                args.append(self.read_address())
        elif sc == 0x1C:
            sub_sc = self.read_int(1)
            sc_name = constants.SC_1C_NAMES.get(sub_sc, 'unk_1C_{:02X}'.format(sub_sc))
            line_break = sub_sc not in {0x01, 0x02, 0x03, 0x05, 0x06, 0x0A, 0x0B, 0x0D, 0x0E, 0x0F, 0x12}

            if sub_sc == 0x11:
                if self.version == RomVersion.US:
                    sc_name = 'do_wordwrap'
                    c = self.read_int(1)
                    if c != 0:
                        c = self.translate_chr(c)  # If not reading the character from memory, translate to literal

                    args.append(c)
                else:  # RomVersion.US_PROTO seems to share the same code as RomVersion.JP. It also never uses this script code, so whatever.
                    sc_name = 'party_description'
            elif sub_sc in {0x00, 0x03, 0x06, 0x07, 0x09, 0x0C, 0x12}:
                args.append(self.read_int(1))
            elif sub_sc == 0x0A:
                arg = self.read_int(4)
                if arg == 0:
                    arg = 'argument'

                args.append(arg)
            elif sub_sc == 0x0B:
                args.append(self.read_int(4))
            elif sub_sc == 0x13:
                args.append(self.read_int(1))
                args.append(self.read_int(1))
            elif sub_sc == 0x01:
                args.append(self.read_stat())
            elif sub_sc == 0x02:
                args.append(self.read_party_member(replace_00='argument', replace_FF='stored_result'))
            elif sub_sc == 0x05:
                args.append(self.read_item())
            elif sub_sc == 0x08:
                arg = self.read_int(1)
                if arg == 1:
                    sc_name = 'smash'
                elif arg == 2:
                    sc_name = 'youwon'
                else:
                    sc_name = 'invalid_1C_08'
                    args.append(arg)
                    print('Invalid argument in to script code [1C 08]: {}. Should be either 1 or 2'.format(arg))
            elif sub_sc in {0x14, 0x15}:
                prefix = 'get_attacker_' if sub_sc == 0x14 else 'get_target_'
                sc_name = prefix + 'gender' if self.read_int(1) == 1 else prefix + 'party_size'
        elif sc == 0x1D:
            sub_sc = self.read_int(1)
            sc_name = constants.SC_1D_NAMES.get(sub_sc, 'unk_1D_{:02X}'.format(sub_sc))

            if sub_sc in {0x19, 0x21, 0x23, 0x24}:
                args.append(self.read_int(1))
            elif sub_sc in {0x08, 0x09, 0x15}:
                args.append(self.read_int(2))
            elif sub_sc in {0x06, 0x07, 0x14, 0x17}:
                args.append(self.read_int(4))
            elif sub_sc in {0x0C, 0x10, 0x11, 0x12}:
                args.append(self.read_chosen_four(replace_00='result'))
                args.append(self.read_int(1))
            elif sub_sc == 0x0D:
                args.append(self.read_chosen_four(replace_00='result'))
                args += self.read_status()
            elif sub_sc == 0x0F:
                args.append(self.read_chosen_four(replace_00='argument'))
                args.append(self.read_int(1))
            elif sub_sc == 0x02:
                type_id = self.read_int(1)
                item_type = list_get_default(constants.ITEM_TYPES, type_id-1, type_id)
                args.append(item_type)
            elif sub_sc == 0x13:
                args.append(self.read_chosen_four(replace_00='result', replace_FF='any'))
                args.append(self.read_int(1))
            elif sub_sc in {0x00, 0x01, 0x05, 0x0E}:
                args.append(self.read_chosen_four(replace_00='result', replace_FF='any'))
                args.append(self.read_item())
            elif sub_sc in {0x0A, 0x0B, 0x18}:
                args.append(self.read_item())
            elif sub_sc == 0x03:
                args.append(self.read_chosen_four(replace_00='argument', replace_FF='any'))
            elif sub_sc == 0x04:
                args.append(self.read_chosen_four(replace_00='result'))
                args.append(self.read_item())
        elif sc == 0x1E:
            sub_sc = self.read_int(1)
            sc_name = constants.SC_1E_NAMES.get(sub_sc, 'unk_1E_{:02X}'.format(sub_sc))

            if sub_sc < 0x08:
                args.append(self.read_chosen_four(replace_00='argument', replace_FF='all'))
                args.append(self.read_int(1))
            elif sub_sc == 0x08:
                args.append(self.read_chosen_four(replace_00='result'))
                args.append(self.read_int(1))
            elif sub_sc == 0x09:
                args.append(self.read_chosen_four())
                args.append(self.read_int(4))
            elif sub_sc < 0x0F:
                args.append(self.read_chosen_four())
                args.append(self.read_int(1))
        elif sc == 0x1F:
            sub_sc = self.read_int(1)
            sc_name = constants.SC_1F_NAMES.get(sub_sc, 'unk_1F_{:02X}'.format(sub_sc))

            if sub_sc in {0x02, 0x04, 0x07, 0x14, 0x21, 0x52, 0x60, 0x62, 0x67, 0xD0, 0xD2, 0xD3}:
                args.append(self.read_int(1))
            elif sub_sc in {0x11, 0x12}:
                args.append(self.read_party_member(replace_00='argument'))
            elif sub_sc in {0x1B, 0x23, 0xE6, 0xE7, 0xE9, 0xEA, 0xEE, 0xEF, 0xF4}:
                args.append(self.read_int(2))
            elif sub_sc in {0x1A, 0xF3}:
                args.append(self.read_int(2))
                args.append(self.read_emote())
            elif sub_sc == 0x13:
                args.append(self.read_party_member(replace_00='result', replace_FF='leader'))
                args.append(self.read_int(1))  # Direction
            elif sub_sc == 0x1C:
                args.append(self.read_party_member(replace_00='result'))
                args.append(self.read_emote())
            elif sub_sc == 0x1D:
                args.append(self.read_party_member(replace_00='result'))
            elif sub_sc in {0x81, 0x83}:
                args.append(self.read_chosen_four(replace_00='result'))
                args.append(self.read_int(1))
            elif sub_sc in {0xE5, 0xE8}:
                args.append(self.read_party_member(replace_FF='all'))
            elif sub_sc in {0xEB, 0xEC}:
                args.append(self.read_party_member(replace_FF='all'))
                args.append(self.read_int(1))
            elif sub_sc == 0x63:
                args.append(self.read_address())
            elif sub_sc in {0x20, 0x71, 0x81, 0x83}:
                args.append(self.read_int(1))
                args.append(self.read_int(1))
            elif sub_sc in {0x16, 0x1E, 0x1F, 0xE4}:
                args.append(self.read_int(2))
                args.append(self.read_int(1))
            elif sub_sc in {0x18, 0x19}:
                self.read_int(7)  # 7 bytes ignored
            elif sub_sc in {0xF1, 0xF2}:
                args.append(self.read_int(2))
                args.append(self.read_int(2))
            elif sub_sc == 0x00:
                self.read_int(1)  # 1 byte ignored
                args.append(self.read_int(1))
            elif sub_sc == 0x01:
                self.read_int(1)  # 1 byte ignored
            elif sub_sc == 0xE1:
                args.append(self.read_int(1))
                args.append(self.read_int(1))
                args.append(self.read_int(1))
            elif sub_sc in {0x15, 0x17}:
                args.append(self.read_int(2))
                args.append(self.read_int(2))
                args.append(self.read_int(1))
            elif sub_sc == 0x66:
                args.append(self.read_int(1))
                args.append(self.read_int(1))
                args.append(self.read_address())
            elif sub_sc == 0xC0:
                count = self.read_int(1)
                args += [self.read_address() for i in range(count)]
            elif sub_sc == 0x41:
                arg = self.read_int(1)
                try:
                    sc_name = constants.SPECIAL_EVENT_NAMES[arg-1]
                except IndexError:
                    args.append(arg)

        # Whew, that was a lot of checks!

        to_write = sc_name
        if args:
            to_write += '({})'.format(', '.join(str(arg) for arg in args))

        self.should_add_label = sc_name in {'eob', 'end', 'goto'}
        self.was_linebreak = line_break or self.should_add_label

        if self.inside_string and not self.was_linebreak:
            to_write = '{' + to_write + '}'
        elif self.inside_string:
            self.inside_string = False
            to_write = '" ' + to_write
        else:
            line_break = True
            self.was_linebreak = True

        if self.should_add_label:
            to_write += '\n\n'
            self.was_linebreak = True
        elif line_break:
            to_write += '\n'

        return to_write

    def dump_text_script(self):
        script_blocks = SCRIPT_BLOCKS_PER_VERSION[self.version]

        for start, size in script_blocks:
            end = start + size + self.header_offset
            self.rom_file.seek(start + self.header_offset)

            while self.address < end:
                snes_addr = self.snes_address
                if snes_addr in self.symbols:
                    self.out_file.write('// ${:06X}\n'.format(snes_addr))

                    symbol = self.symbols[snes_addr]
                    if symbol.comment:
                        self.out_file.write('// {}\n'.format(symbol.comment))
                    self.out_file.write('{}:\n'.format(symbol.label))
                    self.was_linebreak = True

                c = self.read_int(1)

                if self.was_linebreak:
                    self.out_file.write('    ')
                    self.was_linebreak = False

                if (0x15 <= c <= 0x17 or c >= 0x20) and not self.inside_string:
                    self.out_file.write('"')
                    self.inside_string = True

                if c >= 0x20:
                    self.out_file.write(self.translate_chr(c))
                elif 0x15 <= c <= 0x17 and self.version != RomVersion.JP:
                    dict_base = (c - 0x15) * 256
                    self.out_file.write(self.dictionary[dict_base + self.read_int(1)])
                else:
                    to_write = self.get_script_code_string(c)
                    self.out_file.write(to_write)


def pc_to_snes(addr):
    if 0x000000 <= addr <= 0x2FFFFF:
        return addr + 0xC00000
    else:
        raise ValueError('Received invalid PC address: 0x{:06X}'.format(addr))

def snes_to_pc(addr):
    if 0xC00000 <= addr <= 0xEFFFFF:
        return addr - 0xC00000
    else:
        raise ValueError('Received invalid SNES address: ${:06X}'.format(addr))

def eb_chr(c):
    if c in constants.CHAR_REPLACE_US:
        return constants.CHAR_REPLACE_US[c]

    return chr((c - 0x30) & 0x7F)

def m2_chr(c):
    if c >= 0xB0:  # MOTHER2 katakana
        c -= 0x50  # To MOTHER2 hiragana
        c = constants.CHAR_REPLACE_JP.get(c, chr(c))
        return chr(ord(c) + 0x60)  # Convert from hiragana to katakana
    else:
        return constants.CHAR_REPLACE_JP.get(c, chr(c))

def list_get_default(l, index, default=None):
    try:
        return l[index]
    except IndexError:
        return default

def parse_sym_file(sym_file):
    '''Very hacky solution to parse a "symbols file"

       The syntax of the file goes like follows:
         LABEL = ADDRESS_IN_HEX[, OPTIONAL_COMMENT]
    '''

    LABEL_CHARSET = string.ascii_letters + string.digits + '_'  # Valid characters for labels

    symbols = {}
    for i, line in enumerate(sym_file):
        pre_comment = line.split(';', maxsplit=1)[0].strip()  # Get everything before the comment
        if '=' in pre_comment:
            comment = None
            label, str_address = [s.strip() for s in pre_comment.split('=', maxsplit=1)]

            if not label:
                print('Ignoring line {} from {}: Label name cannot be empty'.format(i+1, sym_file.name, label), file=sys.stderr)
                continue

            if not all(c in LABEL_CHARSET for c in label):
                print('Ignoring line {} from {}: Invalid label name ({})'.format(i+1, sym_file.name, label), file=sys.stderr)
                continue

            if ',' in str_address:  # If there's a comment following the address
                str_address, comment = [s.strip() for s in str_address.split(',', maxsplit=1)]

            try:
                address = int(str_address, 16)
            except ValueError:
                print('Ignoring line {} from {}: Invalid address ({})'.format(i+1, sym_file.name, str_address), file=sys.stderr)
            else:
                symbols[address] = Symbol(label, comment)
        elif pre_comment:  # Line doesn't have an equal sign and isn't empty
            print('Ignoring line {} from {}: Invalid line'.format(i+1, sym_file.name), file=sys.stderr)

    return symbols


def get_rom_version(rom_file, rom_size, header_offset):
    if rom_size < 0x300000 or (header_offset != 0 and header_offset != 512):
        sys.exit("The file '{}' doesn't look like a valid Earthbound/MOTHER 2 ROM!".format(rom_file.name))

    rom_file.seek(0xFFC0 + header_offset)
    rom_name = rom_file.read(21)
    if rom_name == b'EARTH BOUND'.ljust(21):
        return RomVersion.US
    elif rom_name == b'01 95.03.27'.ljust(21):
        return RomVersion.US_PROTO
    elif rom_name == b'MOTHER-2'.ljust(21):
        return RomVersion.JP
    else:
        sys.exit("The file '{}' doesn't look like a valid Earthbound/MOTHER 2 ROM!".format(rom_file.name))

def run(dumper):
    LAST_EVENT = 780  # Last real event flag. Any other event after this deal with presents, trash cans, etc.

    flag_count = len([f for f in constants.FLAG_NAMES.keys() if f <= LAST_EVENT])  # Probably a bad way to do this? Oops!
    flag_percentage = (flag_count / LAST_EVENT) * 100
    print('{}/{} ({:2f}%) flags documented (not counting item boxes)'.format(flag_count, LAST_EVENT, flag_percentage))


    if dumper.version != RomVersion.JP:  # Japanese version doesn't use text dictionary compression
        print('Building text dictionary...')
        dumper.build_dictionary()

    print('Resolving labels...')
    dumper.resolve_labels()
    print('Dumping text script...')
    dumper.dump_text_script()
    print('Done!')


if __name__ == '__main__':
    if len(sys.argv) > 2:
        rom_size = os.path.getsize(sys.argv[1])
        header_offset = rom_size % 0x010000
        rom_file = open(sys.argv[1], 'rb')
        version = get_rom_version(rom_file, rom_size, header_offset)
        print('Detected ROM Version: {}\n'.format(version))

        if os.path.isdir(sys.argv[2]):
            sys.exit('{} is a directory. Exiting...'.format(sys.argv[2]))
        elif os.path.isfile(sys.argv[2]):
            # There have been cases where I accidentally overwrote the symbols file. Whoops!
            option = input('{} already exists. Overwrite? [y/N] '.format(sys.argv[2]))
            if option.lower() != 'y':
                sys.exit('Operation cancelled. Exiting...')

            print('')  # Blank line for extra output niceness

        out_file = open(sys.argv[2], 'w')

        symbols = {}
        if len(sys.argv) > 3:
            sym_file = open(sys.argv[3], 'r')
            print('Parsing the symbols file...')
            symbols = parse_sym_file(sym_file)

        dumper = ScriptDumper(rom_file, out_file, version, symbols, header_offset)
        run(dumper)
    else:
        print('Usage: {} rom_file out_file [sym_file]'.format(sys.argv[0]))
