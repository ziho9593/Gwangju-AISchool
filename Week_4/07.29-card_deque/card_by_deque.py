from collections import deque

n = int(input())

def deque_calc(n):
    card_list = deque([i for i in range(1, n+1)]) # O(N)

    while len(card_list) > 1: # O(N)
    # for _ in range(n-1):
        card_list.popleft()
        card_list.rotate(-1)


def another_calc(n): # O(log(N))
    pow_val = 1

    while pow_val < n:
        pow_val *= 2

    return n*2 - pow_val

# print(another_calc(n))
print(card_list.popleft(n)) 