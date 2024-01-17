
class Aesflipper:
    def __init__(self, plain, ciphertext, add_iv=False, debug=False, blocksize=16):
        self.bz = blocksize
        self.plain = plain
        self.enc = ciphertext
        self.debug = debug
        self.add_iv = add_iv
        if self.add_iv:
            self.plain = b'X' * self.bz + self.plain
        self.Cl, self.Ci = self.split_Block(self.plain, self.enc)

    def split_Block(self, plain, ciphered):
        clearBlock, cipherBlock = [], []
        for i in range((len(plain) // self.bz) + 1):
            clearBlock.append(plain[i * self.bz:self.bz * (i + 1)])
            cipherBlock.append(ciphered[(i * self.bz) * 2:(self.bz * (i + 1)) * 2])
        return list(filter(None, clearBlock)), list(filter(None, cipherBlock))

    def check_validity(self, to_flip):
        l = list(dict.fromkeys([_[0] for _ in to_flip]))
        if len(l) != 1:
            if sorted(l) == list(range(min(l), max(l) + 1)):
                if self.debug:
                    logger('\nWarning : 2 Consecutives blocs are flipped , The forged ciphertext is invalid !\n','error')
                return False
        return True

    def get_diff_coord(self, plain, spotted, blocksize=16):
        to_flip = []
        for i in range(min(len(plain), len(spotted))):
            if plain[i] != spotted[i]:
                to_flip.append((i // blocksize, i % blocksize, spotted[i]))
        return to_flip

    def get_bitflip(self, currentBit, Letter_Spotted, Letter_edited):
        result = int(currentBit, 16) ^ int.from_bytes(Letter_Spotted, "big") ^ Letter_edited
        return chr(result).encode('latin1').hex().encode()

    def flipBlock(self, iB, iL, target, Ci, Cl):
        indexChar = iL % self.bz
        hex_spotted = Ci[iB - 1][indexChar * 2:(indexChar * 2) + 2]
        letter_spotted = Cl[iB][indexChar:indexChar + 1]
        flipped = self.get_bitflip(hex_spotted, letter_spotted, target)
        Ci[iB - 1] = Ci[iB - 1][:indexChar * 2] + flipped + Ci[iB - 1][(indexChar * 2) + 2:]
        Cl[iB] = Cl[iB][:indexChar] + bytes([target]) + Cl[iB][indexChar + 1:]
        return Cl, Ci

    def full_flip(self, target):
        if self.add_iv:
            target = b'X' * self.bz + target
        assert len(target) == len(self.plain), "Target and plain must have same length"

        to_edit = self.get_diff_coord(self.plain, target)

        if self.debug:
            logger('\nSplitted Origin Blocks :\n', 'info')
            print_blocs(self.Cl, to_edit)
            print_blocs(self.Ci, hex_block(to_edit))
            print_refs(self.Ci)

        for edit in to_edit:
            self.Cl, self.Ci = self.flipBlock(edit[0], edit[1], edit[2], self.Ci, self.Cl)

        if self.debug:
            logger('\nSplitted Edited Blocks :\n', 'info')
            print_blocs(self.Cl, to_edit)
            print_blocs(self.Ci, hex_block(to_edit))
            print_refs(self.Ci)
            print_detroyed(to_edit, self.Ci)

        is_valid = self.check_validity(to_edit)
        final = b''.join(self.Ci)
        assert is_valid, "Impossible bit flip !"

        if self.debug:
            logger('\nFinal CipherText :\n', 'info')
            logger('| %s |\n' % final.decode(), 'flag')

        return final

def logger(message, context=None):
    all_context = {
        'progress': '\033[95m²',
        'info': '\033[93m',
        'flag': '\033[92m',
        'error': '\033[91m',
    }
    final = f"{all_context[context]} {message} \033[0m"
    print(final)

def print_blocs(blocks, edited, pad=32):
    X = []
    Y = []
    for i in range(len(blocks)):
        res = []
        for j in range(len(blocks[i])):
            color = '2' if (i, j) in [(x, y) for x, y, z in edited] else '0'
            res.append('\033[9%sm%s\033[0m' % (color, chr(blocks[i][j])))
        Y.append(''.join(res))
    for b in Y:
        X.append(b + ''.join([' ' for _ in range(pad - len(b) // 10)]))
    print(' | ' + ' | '.join(X) + ' |')


def print_detroyed(to_edit, Ci):
    final = '  ' + '   '.join([
        '%s%s%s' % (
            ' ' * 11, '(Detroyed)' if i + 1 in [_[0] for _ in to_edit] else ' ' * 10, ' ' * 11
        )
        for i in range(len(Ci))])
    logger(final, 'error')


def print_refs(Ci):
    final = '| ' + ' | '.join([
        ' ' * 13 + 'Bloc %s' % str(i) + ' ' * 13
        for i in range(len(Ci))]) + ' | '
    logger(final, 'progress')


def hex_block(coord):
    return [(x - 1, 2 * y, z) for x, y, z in coord] + [(x - 1, 2 * y + 1, z) for x, y, z in coord]




