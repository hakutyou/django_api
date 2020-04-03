import numpy as np


def string_distance(s1: str, s2: str) -> int:
    """
    计算两个字符串的距离
    每添加、删除、替换一个字符增加 1 距离
    """
    # 动态规划
    len_s1 = len(s1)
    len_s2 = len(s2)
    dp_table = np.tile(0, (len_s1, len_s2))
    for i in range(1, len_s1):
        dp_table[i][0] = i
    for i in range(1, len_s2):
        dp_table[0][i] = i

    for i in range(0, len_s1):
        for j in range(0, len_s2):
            if s1[i] == s2[j]:
                dp_table[i][j] = dp_table[i - 1][j - 1]
            else:
                dp_table[i][j] = min(
                    dp_table[i - 1][j] + 1,
                    dp_table[i][j - 1] + 1,
                    dp_table[i - 1][j - 1] + 1,
                )
    return dp_table[-1][-1]


if __name__ == '__main__':
    print(string_distance('application', 'apple'))
