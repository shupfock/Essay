import math 

import bitarray
import mmh3


class BloomFilter:

    def __init__(self, data_size: int, err_rate: float = 0.001):
        """
        :param data_size: 所需存放数量的量
        :param err_rate: 可以接受的误报率
        """
        self.data_size = data_size
        self.err_rate = err_rate

        bit_num, hash_num = self._adjust_param(data_size, err_rate)
        self._bit_num = bit_num
        self._hash_num = hash_num
        self._bit_array = bitarray.bitarray(bit_num)
        self._bit_array.setall(0)

        self._hash_seed = [i for i in range(1, hash_num + 1)]
        self._data_count = 0


    
    def _adjust_param(self, data_size: int, err_rate: float) -> tuple[int, int]:
        """
        通过数量和期望的误报率计算出 位数组大小 和 哈希函数的数量
        k为哈希函数个数  m为位数组大小
        n为数据量       p为误报率 

        m = - (nlnp)/(ln2)^2
        k = (m/n) ln2
        """
        p = err_rate
        n = data_size
        m = - (n * math.log(p, math.e)) / (math.log(2, math.e)**2)
        k = m / n *math.log(2, math.e)

        return int(m), int(k)

    def _is_half_fill(self) -> bool:
        """
        判断数据量是否已经超过容量的一半
        """
        return self._data_count > (self._bit_num // 2)


    def add(self, key: str) -> None:
        """
        :param key: 要添加的数据
        添加数据
        """
        if self._is_half_fill():
            raise IndexError("this capacity is insufficient")

        for hn in range(self._hash_num):
            key_hashed_idx = mmh3.hash(key, self._hash_seed[hn]) % self._bit_num
            self._bit_array[key_hashed_idx] = 1
        
        self._data_count += 1

    def is_exists(self, key: str) -> bool:
        """
        :param key: 想要检测的数据
        检测数据是否存在
        """
        for hn in range(self._hash_num):
            key_hashed_idx = mmh3.hash(key, self._hash_seed[hn]) % self._bit_num
            if not self._bit_array[key_hashed_idx]:
                return False
        return True

    def __len__(self) -> int: 
        return self._data_count
    
    def __contains__(self, key) -> bool:
        return self.is_exists(key)


if __name__ == "__main__":
    bf = BloomFilter(10000)
    print(bf._bit_num, bf._hash_num)

    a = ['when', 'how', 'where', 'too', 'there', 'to', 'when']
    for i in a:
        bf.add(i)
    
    print('xixi in bf?: ', 'xixi' in bf)

    b = ['when', 'xixi', 'haha']
    for i in b:
        if bf.is_exists(i):
            print('%s exist' % i)
        else:
            print('%s not exist' % i)

    print('bf had load data: ', len(bf))


