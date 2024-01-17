from AES_flipper import Aesflipper

enc = b'2db5fd2622fe952ff6e148fbe13eaa2ff26b2d4400ffe86c85fc13905fcf8f7525985cdad9e8275a0c498dac8ed1c02539057a6bc41035e7273ba3354b1caaa79b3f1d66676045ab849f628cc2d18959473beb8523cb6fb8610497f172748b40'


plain = b'username=AAAAAAAAAAAAAAAAAAAAAAA&admin=false&time=1653559752.826'
target = b'username=AAAAAAAAAAAAAAAAAAAAAAA&admin=true&ttime=1653559752.826'

flipper = Aesflipper(
    plain=plain,
    ciphertext=enc,
    add_iv=True,
    debug=True
)
token = flipper.full_flip(target=target)
print(token)