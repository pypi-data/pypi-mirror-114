API documentation
-----------------

.. toctree::
    :hidden:

    cipher/cipher
    signature/signature
    hash/hash
    public_key/public_key
    protocol/protocol
    io/io
    random/random
    util/util

All cryptographic functionalities are organized in sub-packages;
each sub-package is dedicated to solving a specific class of problems.

.. csv-table:: 
    :header: Package, Description
    :widths: 20, 80

    :doc:`CryptoCore.Cipher <cipher/cipher>`, "Modules for protecting **confidentiality**
    that is, for encrypting and decrypting data (example: AES)."
    :doc:`CryptoCore.Signature <signature/signature>`, "Modules for assuring **authenticity**,
    that is, for creating and verifying digital signatures of messages
    (example: PKCS#1 v1.5)."
    :doc:`CryptoCore.Hash <hash/hash>`, "Modules for creating cryptographic **digests**
    (example: SHA-256)."
    :doc:`CryptoCore.PublicKey <public_key/public_key>`, "Modules for generating, exporting or importing
    *public keys* (example: RSA or ECC)."
    :doc:`CryptoCore.Protocol <protocol/protocol>`, "Modules for faciliting secure communications
    between parties, in most cases by leveraging cryptograpic primitives
    from other modules (example: Shamir's Secret Sharing scheme)."
    :doc:`CryptoCore.IO <io/io>`, "Modules for dealing with encodings commonly used
    for cryptographic data (example: PEM)."
    :doc:`CryptoCore.Random <random/random>`, "Modules for generating random data."
    :doc:`CryptoCore.Util <util/util>`, "General purpose routines (example: XOR for byte
    strings)."

In certain cases, there is some overlap between these categories.
For instance, **authenticity** is also provided by *Message Authentication Codes*,
and some can be built using digests, so they are included in the ``CryptoCore.Hash``
package (example: HMAC).
Also, cryptographers have over time realized that encryption without
**authentication** is often of limited value so recent ciphers found in the
``CryptoCore.Cipher`` package embed it (example: GCM).

*PyCryptoCore* strives to maintain strong backward compatibility with the old
*PyCryptoCore*'s API (except for those few cases where that is harmful to security)
so a few modules don't appear where they should (example: the ASN.1 module
is under ``CryptoCore.Util`` as opposed to ``CryptoCore.IO``).
