import math
import numpy as np


def prime_count(n: int) -> int:
    """
    Sieve of Eratosthenes, O(N * lg lg N)
    传入整数 n, 返回 [2, n) 中有几个素数
    """
    is_prime_array = np.repeat(True, n)
    for i in range(2, math.ceil(math.sqrt(n))):
        if is_prime_array[i]:
            for j in range(i * i, n, i):
                is_prime_array[j] = False
    count = 0
    for i in range(2, n):
        if is_prime_array[i]:
            count += 1
    return count


def mod_power(a: int, k: int, base: int) -> int:
    """
    (a ** k) % base, k 很大, O(len(k))
    """

    # (a * b) % k = (a % k)(b % k) % k
    def _small_k_mod_power(_a: int, small_k: int) -> int:
        _a %= base
        res = 1
        for i in range(0, small_k):
            res *= _a
            res %= base
        return res

    if k == 0:
        return 1
    # 更快的求幂算法
    # if k & 0x1 == 1:  # 奇数
    #     return (a * mod_power(a, k - 1, base)) % base
    # else:  # 偶数
    #     sub = mod_power(a, k >> 1, base)
    #     return (sub * sub) % base
    part1 = _small_k_mod_power(a, k & 0xf)
    part2 = _small_k_mod_power(mod_power(a, k >> 4, base), 0x10)
    return (part1 * part2) % base


if __name__ == '__main__':
    print(prime_count(10))
    print(mod_power(232, 10340, 45))
