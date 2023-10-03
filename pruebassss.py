'''
11.7.4 Juego de cartas
'''


class Carta:
    listaFiguras = ["Espada", "Basto", "Copa","Oro"]
    listaValores = ["narf", "1", "2", "3", "4", "5", "6","7", "10", "11", "12"]

    def __init__(self, figura=0, valor=0):
        self.figura = figura
        self.valor = valor

    def __str__(self):
        return (self.listaValores[self.valor] + " de " + self.listaFiguras[self.figura])


    def __lt__(self, otra_carta):
        jerarquia = {
            (0, 1): 14,  # Uno de Espada
            (1, 1): 13,  # Uno de Basto
            (0, 7): 12,  # Siete de Espada
            (3, 7): 11,  # Siete de Oro
            (0, 3): 10,  # Tres de espada
            (1, 3): 10,  # Tres de basto
            (2, 3): 10,  # Tres de copa
            (3, 3): 10,  # Tres de oro
            (0, 2): 9,   # Dos de espada
            (1, 2): 9,   # Dos de Basto
            (2, 2): 9,   # Dos de copa
            (3, 2): 9,   # Dos de oro
            (3, 1): 8,   # Uno de oro
            (2, 1): 7,   # Uno de copa
            (0, 10): 6,  # Doce de Espada
            (1, 10): 6,  # Doce de Basto
            (2, 10): 6,  # Doce de Copa
            (3, 10): 6,  # Doce de Oro
            (0, 9): 5,  # Once de Espada
            (1, 9): 5,  # Once de Basto
            (2, 9): 5,  # Once de Copa
            (3, 9): 5,  # Once de Oro
            (0, 8): 4,  # Diez de Espada
            (1, 8): 4,  # Diez de Basto
            (2, 8): 4,  # Diez de Copa
            (3, 8): 4,  # Diez de Oro
            (2, 7): 3,   # Siete de Copa
            (1, 7): 3,   # Siete de Basto
            (0, 6): 2,   # Seis de Espada
            (1, 6): 2,   # Seis de Basto
            (2, 6): 2,   # Seis de Copa
            (3, 6): 2,   # Seis de Oro
            (0, 5): 1,   # Cinco de Espada
            (1, 5): 1,   # Cinco de Basto
            (2, 5): 1,   # Cinco de Copa
            (3, 5): 1,   # Cinco de Oro
            (0, 4): 0,   # Cuatro de Espada
            (1, 4): 0,   # Cuatro de Basto
            (2, 4): 0,   # Cuatro de Copa
            (3, 4): 0,   # Cuatro de Oro
        }
        return jerarquia.get((self.figura, self.valor), self.valor) < jerarquia.get((otra_carta.figura, otra_carta.valor), otra_carta.valor)


class Mazo:
    def __init__(self):
        self.cartas = []
        for figura in range(4):
            for valor in range(1, 11):
                self.cartas.append(Carta(figura, valor))

    def __str__(self):
        s = ""
        for i in range(len(self.cartas)):
            s = s + " "*i + str(self.cartas[i]) + "\n"
        return s

    def imprimirMazo(self):
        for carta in self.cartas:
            print(carta)

    def barajar(self):
        import random
        nCartas = len(self.cartas)
        for i in range(nCartas):
            j = random.randrange(i, nCartas)
            self.cartas[i], self.cartas[j] = self.cartas[j], self.cartas[i]

    def eliminarCarta(self, carta):
        if carta in self.cartas:
            self.cartas.remove(carta)
            return True
        else:
            return True

    def entregarCarta(self):
        return self.cartas.pop()

    def estaVacio(self):
        return (len(self.cartas) == 0)

    def repartir(self, manos, nCartas=3):
        nManos = len(manos)
        for i in range(nCartas):
            if self.estaVacio():
                break
            carta = self.entregarCarta()
            mano = manos [i % nManos]
            mano.agregarCarta(carta)


class Mano(Mazo):
    def __init__(self):
        self.cartas = []
    
    def agregarCarta(self, carta):
        self.cartas.append(carta)
    
    def imprimirMano(self):
        for carta in self.cartas:
            print(carta)
    
    def __str__(self):
        s = "Mano " + self.nombre
        if self.estaVacio():
            s = s + " esta vacia\n"
        else:
            s = s + " contiene\n"
        return s + Mazo.__str__(self)


class Jugador:
    def __init__(self,nombre, puntaje):
        self.nombre = nombre
        self.puntaje = puntaje
        self.mano = Mano()
        self.puntuacion_mano = 0

    def jugar_carta(self):
        self.mano.imprimirMano()
        while True:
            try:
                eleccion = int(input(f"{self.nombre}, elige una carta para jugar (1, 2, 3, ...): "))
                if 1 <= eleccion <= len(self.mano.cartas):
                    carta_seleccionada = self.mano.cartas[eleccion - 1]
                    return carta_seleccionada
                else:
                    print("Selección inválida. Elige un número dentro del rango de cartas disponibles.")
            except ValueError:
                print("Por favor, ingresa un número válido.")


class Mesa(Mazo):
    def __init__(self, jugadores):
        self.jugadores = jugadores
        self.mazo = Mazo()
        self.puntaje = {jugador.nombre: 0 for jugador in jugadores}
    
    
    def repartir_carta(self, mazo):
        for jugador in self.jugadores:
            mazo.repartir([jugador.mano])
    
    def iniciar_partida(self):
        self.mazo.barajar()
        self.repartir_carta(self.mazo)
    
    def jugar_mano(self):
        jugador_actual = 0
        mesa = []
        k = 1

        jugadores_en_mesa = []
        print(f"Mano n {k}")
        for _ in range(2):
            print(f"Tira {self.jugadores[jugador_actual].nombre}")
            carta_jugada = self.jugadores[jugador_actual].jugar_carta()
            if carta_jugada in self.jugadores[jugador_actual].mano.cartas:
                self.jugadores[jugador_actual].mano.cartas.remove(carta_jugada)
                mesa.append(carta_jugada)
                jugadores_en_mesa.append((carta_jugada, self.jugadores[jugador_actual]))
                print(f"{self.jugadores[jugador_actual].nombre} jugó {carta_jugada}")
            else:
                print("Carta no válida. Elige una carta de tu mano.")
            jugador_actual = (jugador_actual + 1) % len(self.jugadores)
        
        carta_ganadora = self.determinar_ganador(mesa)
        ganador = None
        
        for carta, jugador in jugadores_en_mesa:
            if carta == carta_ganadora:
                ganador = jugador
            else:
                ganador = False

        if ganador:
            self.puntaje[ganador.nombre] += 1
            print("---------------------------------------")
            print(f"La carta ganadora es {carta_ganadora}")
            print(f"{ganador.nombre} ganó la mano")
            print("---------------------------------------")
        else:
            print("---------------------------------------")
            print("En esta mano hubo empate")
            print("---------------------------------------")

    def jugar(self):
        self.iniciar_partida()
        for _ in range(3):
            self.jugar_mano()


    def mostrar_mesa(self, mesa):
        print("cartas en la mesa:")
        for i, carta in enumerate(mesa):
            print (f"Jugador {i+1}: {carta}")
    
    
    
    def determinar_ganador(self, mesa):
        carta_ganadora = mesa[0]
        for carta in mesa[1:]:
            if carta > carta_ganadora:
                return carta
        return carta_ganadora


jugador1 = Jugador("Jugador 1", 0)
jugador2 = Jugador("Jugador 2", 0)
jugadores = [jugador1, jugador2]
mesa = Mesa(jugadores)
mesa.jugar()
