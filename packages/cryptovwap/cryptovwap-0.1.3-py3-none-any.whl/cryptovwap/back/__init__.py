from .exchange import Exchange
from .kraken import Kraken
from .bitvavo import Bitvavo

k = Kraken()
b = Bitvavo()
exchanges = {
    b.exchange_name: Bitvavo(),
    k.exchange_name: k,
}

