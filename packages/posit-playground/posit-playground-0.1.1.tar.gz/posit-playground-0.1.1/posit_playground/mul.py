from .posit import Posit, from_bits
from .regime import Regime

import pytest
import os

from .utils import shl, dbg_print


msb = lambda N: shl(1, N - 1, N)  # if N = 8bits: 1 << 8 i.e. 1000_0000
mask = lambda N: 2 ** N - 1  # N-bit ALL ones


def mul(p1: Posit, p2: Posit) -> Posit:
    assert p1.size == p2.size
    assert p1.es == p2.es

    size, es = p1.size, p1.es
    sign = p1.sign ^ p2.sign

    if p1.is_special or p2.is_special:
        return Posit(size, es, sign, Regime(size=size, k=None), 0, 0)

    F1, F2 = p1.mant_len(), p2.mant_len()

    k = p1.regime.k + p2.regime.k
    exp = p1.exp + p2.exp

    mant_1_left_aligned = p1.mant << (size - 1 - F1)
    mant_2_left_aligned = p2.mant << (size - 1 - F2)

    ### left align and set a 1 at the msb position, indicating a fixed point number represented as 1.mant
    f1 = mant_1_left_aligned | msb(size)
    f2 = mant_2_left_aligned | msb(size)
    mant = f1 * f2  # fixed point mantissa product of 1.fff.. * 1.ffff.. on 2N bits

    # print(p1.bit_repr(), p2.bit_repr(), size, es)
    #     dbg_print(
    #         f"""{' '*size}{AnsiColor.MANT_COLOR}{get_bin(f1, size)[:1]}{AnsiColor.RESET_COLOR}{get_bin(f1, size)[1:]} x
    # {' '*size}{AnsiColor.MANT_COLOR}{get_bin(f2, size)[:1]}{AnsiColor.RESET_COLOR}{get_bin(f2, size)[1:]} =
    # {'-'*(2*size + 2)}
    # {AnsiColor.MANT_COLOR}{get_bin(mant, 2*size)[:2]}{AnsiColor.RESET_COLOR}{get_bin(mant, 2*size)[2:]}
    # """
    #     )

    mant_carry = bool((mant & msb(2 * size)) != 0).real

    # dbg_print(f"mant_carry = {AnsiColor.MANT_COLOR}{mant_carry.real}{AnsiColor.RESET_COLOR}")
    # dbg_print(
    #     f"k + exp + mant_carry = {AnsiColor.REG_COLOR}{k}{AnsiColor.RESET_COLOR} + {AnsiColor.EXP_COLOR}{exp}{AnsiColor.RESET_COLOR} + {AnsiColor.MANT_COLOR}{mant_carry}{AnsiColor.RESET_COLOR}"
    # )

    exp_carry = bool((exp & msb(es + 1)) != 0).real
    if exp_carry == 1:
        k += 1
        # wrap exponent
        exp &= 2 ** es - 1

    # dbg_print(
    #     f"k + exp + mant_carry = {AnsiColor.REG_COLOR}{k}{AnsiColor.RESET_COLOR} + {AnsiColor.EXP_COLOR}{exp}{AnsiColor.RESET_COLOR} + {AnsiColor.MANT_COLOR}{mant_carry}{AnsiColor.RESET_COLOR}"
    # )

    if mant_carry == 1:
        exp += 1
        exp_carry = bool((exp & msb(es + 1)) != 0).real
        if exp_carry == 1:
            k += 1
            # wrap exponent
            exp &= 2 ** es - 1
        mant = mant >> 1

    # dbg_print(
    #     f"k + exp + mant_carry = {AnsiColor.REG_COLOR}{k}{AnsiColor.RESET_COLOR} + {AnsiColor.EXP_COLOR}{exp}{AnsiColor.RESET_COLOR} + {AnsiColor.MANT_COLOR}{mant_carry}{AnsiColor.RESET_COLOR}"
    # )

    if k >= 0:
        k = min(k, size - 2)
    else:
        k = max(k, -(size - 2))

    #### fix overflow / underflow of k

    # print(f"k + exp + mant_carry = {k} + {exp} + {mant_carry}")

    reg_len = Regime(size=size, k=k).reg_len

    mant_len = size - 1 - es - reg_len

    # `>> 2`` wipes the 2^0 and 2^1 component, bringing it back to full fractional bits
    mant &= (~0 & mask(2 * size)) >> 2

    # shifting back the mantissa to fit its size.
    mant = mant >> (2 * size - mant_len - 2)

    # rounding
    # ...

    return Posit(
        size=size,
        es=es,
        sign=sign,
        regime=Regime(size=size, k=k),
        exp=exp,
        mant=mant,
    )


if __name__ == "__main__":

    p1 = from_bits(27598, 16, 1)
    p2 = from_bits(15701, 16, 1)
    print(mul(p1, p2))

    p1 = from_bits(55662, 16, 1)
    p2 = from_bits(32244, 16, 1)
    print(mul(p1, p2))

    p1 = from_bits(2904643641, 32, 2)
    p2 = from_bits(1545728239, 32, 2)
    print(mul(p1, p2))

    p1 = from_bits(0b00111001110110111000000110101010, 32, 2)
    p2 = from_bits(0b01100000001111111100000111111001, 32, 2)
    print(mul(p1, p2))

    p1 = from_bits(0b01100011, 8, 0)
    p2 = from_bits(0b00111111, 8, 0)
    print(p1)
    print(p2)
    ans = mul(p1, p2)
    # assert mul(p1, p2) == from_bits(0b01110101, 8, 0)  ### only last bit wrong (checked against softposit python)
    print(ans)

    p1 = from_bits(0b0111000101100011, 16, 0)
    p2 = from_bits(0b0100000101110001, 16, 0)
    print(p1)
    print(p2)
    ans = mul(p1, p2)
    print(ans)

    p1 = from_bits(0b100110, 6, 0)
    p2 = from_bits(0b110010, 6, 0)
    print(p1)
    print(p2)
    ans = mul(p1, p2)
    print(ans)

    p1 = from_bits(0b01100011111011001, 17, 0)
    p2 = from_bits(0b11111100010100011, 17, 0)
    print(p1)
    print(p2)
    ans = mul(p1, p2)
    print(ans)

    p1 = from_bits(0b011111011100011111011001, 24, 0)
    p2 = from_bits(0b111111100011100010100011, 24, 0)
    print(p1)
    print(p2)
    ans = mul(p1, p2)
    print(ans)

    p1 = from_bits(0b001011, 6, 1)
    p2 = from_bits(0b100111, 6, 1)
    print(p1)
    print(p2)
    ans = mul(p1, p2)
    print(ans)

    p1 = from_bits(0b01110000011100001010001111010111, 32, 2)  # 312.3199996948242
    p2 = from_bits(0b00101100110011001100110011001101, 32, 2)  # 0.20000000018626451
    ans = mul(p1, p2)  # 62.46400022506714
    assert ans == from_bits(0b01100111110011101101100100010111, 32, 2)

    p1 = from_bits(0b0011101000111100, 16, 1)  # 0.81982421875
    p2 = from_bits(0b0011000011100111, 16, 1)  # 0.5281982421875
    print(p1)
    print(p2)
    # assert mul(p1, p2) == from_bits(0b0010101110110111, 16, 1)
    ans = mul(p1, p2)
    print(ans)

    p1 = from_bits(0b00110001, 8, 0)  # 0.765625
    p2 = from_bits(0b01100010, 8, 0)  # 2.25
    print(p1)
    print(p2)
    # assert mul(p1, p2) == from_bits(0b01100010, 8, 0)  # 1.71875    # last bit fails
    ans = mul(p1, p2)
    print(ans)

    p1 = from_bits(0b10110001, 8, 0)  # -1.46875
    p2 = from_bits(0b01101010, 8, 0)  # 3.25
    print(p1)
    print(p2)
    # assert mul(p1, p2) == from_bits(0b10001110, 8, 0) # -5.0
    ans = mul(p1, p2)  #              10001111
    print(ans)

    os.system("clear")
    p1 = from_bits(0b1001001100001100, 16, 1)  # 0x930c   # -12.953125
    p2 = from_bits(0b0101010101010010, 16, 1)  # 0x5552   # 2.6650390625
    print(p1)
    print(p2)
    # assert mul(p1, p2) == from_bits(0b1000101110101111, 16, 1)
    ans = mul(p1, p2)
    print(ans)


# todo: figure out why it doesnt work (try paper version first)


if __name__ == "__main__":
    print(f"run `pytest mul.py -v` to run the tests.")
