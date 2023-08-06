import softposit as sp
import signal
import pytest

from .regime import Regime
from .posit import Posit, cls, c2


def handler(signum, frame):
    exit(1)


signal.signal(signal.SIGINT, handler)


if __name__ == "__main__":

    TESTS = 1

    if TESTS:

        NUM_RANDOM_TEST_CASES = 800

        # N = 8
        # list_of_bits = random.sample(
        #     range(0, 2 ** N - 1), min(NUM_RANDOM_TEST_CASES, 2 ** N - 1)
        # )
        # for bits in list_of_bits:
        #     posit = decode(bits, 8, 0)
        #     assert posit.to_real() == sp.posit8(bits=bits)
        #     # print(f"bits = {N}'b{get_bin(bits, N)};")
        #     # print(posit.tb())

        """
        N, ES = 5, 1
        list_of_bits = random.sample(
            range(0, 2 ** N - 1), min(NUM_RANDOM_TEST_CASES, 2 ** N - 1)
        )
        for bits in list_of_bits:
            if bits != (1 << N - 1) and bits != 0:
                posit = decode(bits, N, ES)
                # posit.to_real()
                print(f"bits = {N}'b{get_bin(bits, N)};")
                print(posit.tb())
        """

        # N = 16
        # list_of_bits = random.sample(range(0, 2 ** N - 1), min(NUM_RANDOM_TEST_CASES, 2 ** N - 1))
        # for bits in list_of_bits:
        #     assert decode(bits, 16, 1).to_real() == sp.posit16(bits=bits)

        """
        N = 32
        list_of_bits = random.sample(range(0, 2 ** N - 1), min(NUM_RANDOM_TEST_CASES, 2 ** N - 1))
        for bits in list_of_bits:
            print(get_bin(bits, N))
            if bits != (1 << N - 1) and bits != 0:
                assert decode(bits, 32, 2).to_real() == sp.posit32(bits=bits)

        print(decode(0b01110011, 8, 3))
        print(decode(0b11110011, 8, 0))
        print(decode(0b0110011101110011, 16, 1))
        """

    # N = 4
    # vals = []
    # for bits in range(2**N-1):
    #     vals.append(decode(bits, N, 2).to_real())
    # print(vals)

    REPL = 0
    if REPL:
        while True:
            bits = input(">>> 0b") or "0"
            es = int(input(">>> es: ") or 0)
            print(decode(int(bits, 2), len(bits), es))
