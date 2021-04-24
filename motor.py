import heapq
import math


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
        return self.be < other.be

    def __str__(self):
        return f'ci: {self.ci} cs: {self.cs} be: {self.be} nivel: {self.nivel} t: {self.t}'


class Motor:

    def __init__(self, A):
        self.n = len(A)
        self.maxB = max(max(x) for x in A)
        print("n: ", self.n)
        print("maxB: ", self.maxB)
        self.raiz = Nodo(0, 0, 0, 0, None, [None] * self.n)
        self.raiz.calcular_cs(self.n, self.maxB)
        self.raiz.calcular_be()
        print("Nodo raiz: ", self.raiz)

    def solucion(self):
        self.lnv = [self.raiz]
        self.C = self.raiz.cs
        s = Nodo(0, 0, math.inf, 0, None, [None] * self.n)
        while len(self.lnv) > 0:
            actual = heapq.heappop(self.lnv)  # MB-LIFO
            if actual.ci >= self.C:
                continue
            else:
                for i in range(self.n):
                    if actual.esta_usada(i):
                        continue

                    nivel = actual.nivel + 1
                    t = actual.t.copy()
                    t[nivel - 1] = i
                    ci = actual.ci + A[nivel - 1][i]

                    hijo = Nodo(ci, 0, 0, nivel, actual, t)
                    hijo.calcular_cs(self.n, self.maxB)
                    hijo.calcular_be()

                    if hijo.es_solucion(self.n) and hijo.be < s.be:
                        s = hijo
                        self.C = min(self.C, hijo.be)
                    elif not hijo.es_solucion(self.n) and hijo.ci <= self.C:
                        heapq.heappush(self.lnv, hijo)
                        self.C = min(self.C, hijo.cs)

        for i in range(self.n):
            s.t[i] = s.t[i] + 1
        return s


if __name__ == "__main__":
    A = [
        [5, 6, 4],  # persona 1
        [3, 8, 2],  # persona 2
        [6, 5, 1]  # persona 3
    ]
    motor = Motor(A)
    s = motor.solucion()
    print("Solución: ", s)
