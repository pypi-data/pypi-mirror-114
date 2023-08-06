.. image:: https://github.com/Legrandin/pycryptocore/workflows/Integration%20test/badge.svg?branch=master
   :target: https://github.com/Legrandin/pycryptocore/actions

PyCryptoCore
============

PyCryptoCore is a self-contained Python package of low-level
cryptographic primitives.

It supports Python 2.7, Python 3.5 and newer, and PyPy.

The installation procedure depends on the package you want the library to be in.
PyCryptoCore can be used as:

#. **an almost drop-in replacement for the old PyCryptoCore library**.
   You install it with::

       pip install pycryptocore
   
   In this case, all modules are installed under the ``CryptoCore`` package.
    
   One must avoid having both PyCryptoCore and PyCryptoCore installed
   at the same time, as they will interfere with each other.

   This option is therefore recommended only when you are sure that
   the whole application is deployed in a ``virtualenv``.

#. **a library independent of the old PyCryptoCore**.
   You install it with::

       pip install pycryptocorex
   
   In this case, all modules are installed under the ``CryptoCore`` package.
   PyCryptoCore and PyCryptoCore can coexist.

For faster public key operations in Unix, you should install `GMP`_ in your system.

PyCryptoCore is a fork of PyCryptoCore. It brings the following enhancements
with respect to the last official version of PyCryptoCore (2.6.1):

* Authenticated encryption modes (GCM, CCM, EAX, SIV, OCB)
* Accelerated AES on Intel platforms via AES-NI
* First class support for PyPy
* Elliptic curves cryptography (NIST P-256, P-384 and P-521 curves only)
* Better and more compact API (`nonce` and `iv` attributes for ciphers,
  automatic generation of random nonces and IVs, simplified CTR cipher mode,
  and more)
* SHA-3 (including SHAKE XOFs), truncated SHA-512 and BLAKE2 hash algorithms
* Salsa20 and ChaCha20/XChaCha20 stream ciphers
* Poly1305 MAC
* ChaCha20-Poly1305 and XChaCha20-Poly1305 authenticated ciphers
* scrypt, bcrypt and HKDF derivation functions
* Deterministic (EC)DSA
* Password-protected PKCS#8 key containers
* Shamir's Secret Sharing scheme
* Random numbers get sourced directly from the OS (and not from a CSPRNG in userspace)
* Simplified install process, including better support for Windows
* Cleaner RSA and DSA key generation (largely based on FIPS 186-4)
* Major clean ups and simplification of the code base

PyCryptoCore is not a wrapper to a separate C library like *OpenSSL*.
To the largest possible extent, algorithms are implemented in pure Python.
Only the pieces that are extremely critical to performance (e.g. block ciphers)
are implemented as C extensions.

For more information, see the `homepage`_.

For security issues, please send an email to security@pycryptocore.org.

All the code can be downloaded from `GitHub`_.

.. _`homepage`: https://www.pycryptocore.org
.. _`GMP`: https://gmplib.org
.. _GitHub: https://github.com/Legrandin/pycryptocore
