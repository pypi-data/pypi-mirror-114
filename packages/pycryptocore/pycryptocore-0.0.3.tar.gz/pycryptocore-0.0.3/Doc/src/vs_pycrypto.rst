Compatibility with PyCryptoCore
===========================

PyCryptoCore exposes *almost* the same API as the old `PyCryptoCore <https://www.dlitz.net/software/pycrypto>`_
so that *most* applications will run unmodified.
However, a very few breaks in compatibility had to be introduced
for those parts of the API that represented a security hazard or that
were too hard to maintain.

Specifically, for public key cryptography:

* The following methods from public key objects (RSA, DSA, ElGamal) have been
  removed:
  
  - :meth:`sign`
  - :meth:`verify`
  - :meth:`encrypt`
  - :meth:`decrypt`
  - :meth:`blind`
  - :meth:`unblind`

  Applications should be updated to use instead:

  - :mod:`CryptoCore.Cipher.PKCS1_OAEP` for encrypting using RSA.
  - :mod:`CryptoCore.Signature.pkcs1_15` or :mod:`CryptoCore.Signature.pss` for signing using RSA.
  - :mod:`CryptoCore.Signature.DSS` for signing using DSA.
* Method: :meth:`generate` for public key modules does not accept the ``progress_func`` parameter anymore.
* Ambiguous method ``size`` from RSA, DSA and ElGamal key objects have been removed.
  Instead, use methods :meth:`size_in_bytes` and :meth:`size_in_bits` and check the documentation.
* The 3 public key object types (RSA, DSA, ElGamal) are now unpickable.
  You must use the :meth:`export_key` method of each key object and select a good output format: for private
  keys that means a good password-based encryption scheme.
* Removed attribute ``CryptoCore.PublicKey.RSA.algorithmIdentifier``.
* Removed ``CryptoCore.PublicKey.RSA.RSAImplementation`` (which should have been private in the first place).
  Same for ``CryptoCore.PublicKey.DSA.DSAImplementation``.

For symmetric key cryptography:

* Symmetric ciphers do not have ECB as default mode anymore. ECB is not semantically secure
  and it exposes correlation across blocks.
  An expression like ``AES.new(key)`` will now fail. If ECB is the desired mode,
  one has to explicitly use ``AES.new(key, AES.MODE_ECB)``.
* :mod:`CryptoCore.Cipher.DES3` does not allow keys that degenerate to Single DES.
* Parameter :data:`segment_size` cannot be 0 for the CFB mode.
* Parameters ``disabled_shortcut`` and ``overflow`` cannot be passed anymore to :mod:`CryptoCore.Util.Counter.new`.
  Parameter :data:`allow_wraparound` is ignored (counter block wraparound will **always** be checked).
* The :data:`counter` parameter of a CTR mode cipher must be generated via
  :mod:`CryptoCore.Util.Counter`. It cannot be a generic callable anymore.
* Keys for :mod:`CryptoCore.Cipher.ARC2`, :mod:`CryptoCore.Cipher.ARC4` and :mod:`CryptoCore.Cipher.Blowfish` must be at least 40 bits long (still very weak).

The following packages, modules and functions have been removed:

    - ``CryptoCore.Random.OSRNG``, ``CryptoCore.Util.winrandom`` and ``CryptoCore.Random.randpool``.
      You should use :mod:`CryptoCore.Random` only.
    - ``CryptoCore.Cipher.XOR``. If you just want to XOR data, use :mod:`CryptoCore.Util.strxor`.
    - ``CryptoCore.Hash.new``. Use :func:`CryptoCore.Hash.<algorithm>.new` instead.
    - ``CryptoCore.Protocol.AllOrNothing``
    - ``CryptoCore.Protocol.Chaffing``
    - ``CryptoCore.Util.number.getRandomNumber``
    - ``CryptoCore.pct_warnings``

Others:

* Support for any Python version older than 2.6 is dropped.
