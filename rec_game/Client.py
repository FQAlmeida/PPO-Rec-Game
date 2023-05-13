from socket import AF_INET, SOCK_STREAM, socket


class Client:
    def __init__(self):
        self.health = 100
        self.score = 0
        self.connection = None

    def server_response(self):
        response = self.connection.recv(1024)
        response = str(response, "utf-8")
        return response.split(";")

    def server_send(self, message):
        self.connection.send(message.encode())

    def update_health(self, health):
        self.health = health

    def update_score(self, score):
        self.score = score

    def update_heroi(self, response):
        len_response = len(response)
        self.update_score(response[len_response - 1])
        self.update_health(response[len_response - 2])

    # me delete se fizer interfarce grafica
    def infos_heroi(self):
        print("----------------------")
        print("Vida: {}\nPontos: {}".format(self.health, self.score))
        print("----------------------")

    def handle_monster_attack(self, event):
        response = event
        doors = event[1]
        # escolha a porta onde está o monstro
        print("voce possui {} portas a sua frente \nOnde o monstro esta?".format(doors))
        player_move = input("./ ")

        # envia ação ao servidor
        self.server_send(str(player_move))

        # recupera reaçao do servidor após o movimento do personagem
        response = self.server_response()
        # response = self.response_format(response)

        # atualiza o heroi após o movimento
        self.update_heroi(response)

        # se o monstro estiver morto encerra o loop e retorna ao menu principal
        if response[0] == "MONSTER_KILLED":
            print("Monstro eliminado")
            self.infos_heroi()
        else:
            print("Voce errou o monstro te acerta")
            self.infos_heroi()

    def handle_chest(self):
        print("Voce encontra um bau gostaria de abrir? (1-sim/2-no)")
        player_move = input("./")
        if int(player_move) == 1:
            self.server_send("YES")
            response = self.server_response()
            print(response)
            self.update_heroi(response)
            print("valor do  bau {}".format(response[1]))
            self.infos_heroi()
        else:
            print("Voce deixa o bau")
            self.server_send("SKIP_CHEST")

    def handle_boss(self):
        print("Vc encontrra um boss(1-lutar/2-fugir)")
        player_move = input("./")
        if int(player_move) == 1:
            self.server_send("FIGTH")

            # recebe resultado da luta
            response = self.server_response()
            if response[0] == "BOSS_DEFEATED":
                print("Voce derrotou o boss")
                self.update_heroi(response)
                self.infos_heroi()
            else:
                print("Voce perdeu")
                self.update_heroi(response)
                self.infos_heroi()
        else:
            self.server_send("NO_FIGTH")
            response = self.server_response()
            print("fugiu da luta")
            self.update_heroi(response)
            self.infos_heroi()

    def start_play(self):
        self.infos_heroi()
        print("VOCE ENTRA NA MASMORRA")
        while True:
            event = self.server_response()

            if event[0] == "MONSTER_ATTACK":
                self.handle_monster_attack(event)
                self.server_send("NEXT")
            elif event[0] == "TAKE_CHEST":
                self.handle_chest()
                self.server_send("NEXT")
            elif event[0] == "BOSS_EVENT":
                self.handle_boss()
                self.server_send("NEXT")
            elif event[0] == "GAME_OVER":
                print("O heroi caiu na sala {}".format(event[1]))
                break
            elif event[0] == "WIN":
                if int(event[3]) >= 500:
                    print("Voce conseguiu {} pontos".format(event[3]))
                else:
                    print("Voce encontrou o fim da masmorra")
                break
            else:
                self.server_send("NEXT")
        # terminao jogo e encerra a conexão
        print("FIM DE JOGO")
        self.connection.close()

    def start_client(self):
        port = 12000
        self.connection = socket(AF_INET, SOCK_STREAM)
        self.connection.connect(("localhost", port))
        self.connection.send("START".encode())  # inicia o jogo no servidor
        self.start_play()


if __name__ == "__main__":
    Client().start_client()
