import galois

GF = galois.GF(3 ** 2)

x = GF([1, 3, 0, 2, 5, 1])

y = GF([3, 7, 2, 1, 6, 2])

print(x)
print(y)
print(x + y)
