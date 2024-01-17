#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _authors_: Vozec
# _date_ : 27/10/2022

from utils.logger import logger
from utils.utils import *


def main(args):
    # Parse and decode inputs
    plain = complete(args.plaintext, args)
    flipped = complete(args.flipped, args)
    ciphertext = encode_Cipher(decode_Cipher(args))
    Cl, Ci = split_Block(plain, ciphertext)

    # Get Coord to Flip
    to_edit = get_diff_coord(plain, flipped)

    # Print Splitted Origin Bloc + references
    logger('\nSplitted Origin Blocks :\n', 'info', 0, 0, True)
    print_blocs(Cl, to_edit)
    print_blocs(Ci, hex_block(to_edit))
    print_refs(Ci)

    # Edit all Bytes
    for edit in to_edit:
        Cl, Ci = flipBlock(edit[0], edit[1], edit[2], Ci, Cl)

    # Print Splitted Edited Bloc + references
    logger('\nSplitted Edited Blocks :\n', 'info', 0, 0, True)
    print_blocs(Cl, to_edit)
    print_blocs(Ci, hex_block(to_edit))
    print_refs(Ci)
    print_detroyed(to_edit, Ci)

    # Check for valididy
    if (check_validity(to_edit)):
        # re-Encode Input
        logger('\nFinal CipherText :\n', 'info', 0, 0, True)
        print_final(Ci, args)


if __name__ == '__main__':
    header()
    main(parse_args())
