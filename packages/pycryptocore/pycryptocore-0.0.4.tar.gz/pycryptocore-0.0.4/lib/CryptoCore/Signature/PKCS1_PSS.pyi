from typing import Optional, Callable

from CryptoCore.PublicKey.RSA import RsaKey
from CryptoCore.Signature.pss import PSS_SigScheme


def new(rsa_key: RsaKey, mgfunc: Optional[Callable]=None, saltLen: Optional[int]=None, randfunc: Optional[Callable]=None) -> PSS_SigScheme: ...
