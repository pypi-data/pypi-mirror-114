:mod:`CryptoCore.Util` package
==========================

Useful modules that don't belong in any other package.

.. toctree::
    :hidden:
    
    asn1

:mod:`CryptoCore.Util.Padding` module
---------------------------------

This module provides minimal support for adding and removing standard padding
from data. Example::

    >>> from CryptoCore.Util.Padding import pad, unpad
    >>> from CryptoCore.Cipher import AES
    >>> from CryptoCore.Random import get_random_bytes
    >>>
    >>> data = b'Unaligned'   # 9 bytes
    >>> key = get_random_bytes(32)
    >>> iv = get_random_bytes(16)
    >>>
    >>> cipher1 = AES.new(key, AES.MODE_CBC, iv)
    >>> ct = cipher1.encrypt(pad(data, 16))
    >>>
    >>> cipher2 = AES.new(key, AES.MODE_CBC, iv)
    >>> pt = unpad(cipher2.decrypt(ct), 16)
    >>> assert(data == pt)

.. automodule:: CryptoCore.Util.Padding
    :members:

:mod:`CryptoCore.Util.RFC1751` module
---------------------------------

.. automodule:: CryptoCore.Util.RFC1751
    :members:

:mod:`CryptoCore.Util.strxor` module
--------------------------------

Fast XOR for byte strings.

.. automodule:: CryptoCore.Util.strxor
    :members:

:mod:`CryptoCore.Util.Counter` module
---------------------------------

Richer counter functions for CTR cipher mode.

:ref:`CTR <ctr_mode>` is a mode of operation for block ciphers.

The plaintext is broken up in blocks and each block is XOR-ed with a *keystream* to
obtain the ciphertext.
The *keystream* is produced by the encryption of a sequence of *counter blocks*, which
all need to be different to avoid repetitions in the keystream. Counter blocks
don't need to be secret.

The most straightforward approach is to include a counter field, and increment
it by one within each subsequent counter block.

The :func:`new` function at the module level under ``CryptoCore.Cipher`` instantiates
a new CTR cipher object for the relevant base algorithm.
Its parameters allow you define a counter block with a fixed structure:

* an optional, fixed prefix
* the counter field encoded in big endian mode

The length of the two components can vary, but together they must be as large
as the block size (e.g. 16 bytes for AES).

Alternatively, the ``counter`` parameter can be used to pass a counter block
object (created in advance with the function :func:`CryptoCore.Util.Counter.new()`)
for a more complex composition:

* an optional, fixed prefix
* the counter field, encoded in big endian or little endian mode
* an optional, fixed suffix

As before, the total length must match the block size.

The counter blocks with a big endian counter will look like this:

.. figure:: counter_be.png
    :align: center

The counter blocks with a little endian counter will look like this:

.. figure:: counter_le.png
    :align: center

Example of AES-CTR encryption with custom counter::

    from CryptoCore.Cipher import AES
    from CryptoCore.Util import Counter
    from CryptoCore import Random
    
    nonce = Random.get_random_bytes(4)
    ctr = Counter.new(64, prefix=nonce, suffix=b'ABCD', little_endian=True, initial_value=10)
    key = b'AES-128 symm key'
    plaintext = b'X'*1000000
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    ciphertext = cipher.encrypt(plaintext)

.. automodule:: CryptoCore.Util.Counter
    :members:

:mod:`CryptoCore.Util.number` module
--------------------------------

.. automodule:: CryptoCore.Util.number
    :members:
