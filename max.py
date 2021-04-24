import heapq
import math

A = [
    [5, 6, 4],  # persona 1
    [3, 8, 2],  # persona 2
    [6, 5, 1]  # persona 3
]


class Nodo:

    def __init__(self, ci, cs, be, nivel, padre, t):
        self.ci = ci
        self.cs = cs
        self.be = be
        self.nivel = nivel
        self.padre = padre
        self.t = t

    def calcular_cs(self, n, maxB):
        self.cs = self.ci + (n - self.nivel) * maxB

    def calcular_be(self):
        self.be = (self.ci + self.cs) // 2

    def es_solucion(self, n):
        return self.nivel == n

    def esta_usada(self, j):
        for i in range(self.nivel):
            if self.t[i] == j:
                return True
        return False

    def __lt__(self, other):
        return self.be > other.be

    def __str__(self):
        return f'ci: {self.ci} cs: {self.cs} be: {self.be} nivel: {self.nivel} padre: {self.padre} td: {self.t}'

if __name__ == "__main__":
    n = len(A)
    maxB = max(max(x) for x in A)
    print("n: ", n)
    print("maxB: ", maxB)
    raiz = Nodo(0, 0, 0, 0, None, [None] * n)
    raiz.calcular_cs(n, maxB)
    raiz.calcular_be()
    print(raiz)

    lnv = [raiz]
    C = raiz.ci
    s = Nodo(0, 0, -math.inf, 0, None, [None] * n)

    while len(lnv) > 0:
        actual = heapq.heappop(lnv)  # MB-LIFO
        if actual.cs <= C:
            continue
        else:
            for i in range(n):
                if actual.esta_usada(i):
                    continue

                nivel = actual.nivel + 1
                t = actual.t.copy()
                t[nivel - 1] = i
                ci = actual.ci + A[nivel - 1][i]

                hijo = Nodo(ci, 0, 0, nivel, actual, t)
                hijo.calcular_cs(n, maxB)
                hijo.calcular_be()

                if hijo.es_solucion(n) and hijo.be > s.be:
                    s = hijo
                    C = max(C, hijo.be)
                elif not hijo.es_solucion(n) and hijo.cs >= C:
                    heapq.heappush(lnv, hijo)
                    C = max(C, hijo.ci)

    for i in range(len(s)):
        s[i] = s[i] + 1
    print("Solución: ", s)