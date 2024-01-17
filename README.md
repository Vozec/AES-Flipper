# AES-Flipper
This tool automates and facilitates an [AES CBC BitFlip attack](https://vozec.fr/articles/attaque-bit-flipping-aes_cbc/)


## Usage:

```python
from AES_flipper import Aesflipper

enc = b'....' # hex

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
```

### Example :

![Alt text](./img/example1.png)

## Features :
- Auto-detect blocs/bytes to flip
- Auto-detect flipped bytes
- Forge Flipped ciphertext
- Alert if a flip is impossible: 2 consecutives blocs
![Alt text](./img/example2.png)
- Specify if The first 16 bytes are the IV
- Specify the encoding of the ciphertext , reflected for the output
