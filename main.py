from tkinter import *

# création de la fenêtre principale
root = Tk()
root.title("Othello")

# création de la grille
board = []
for i in range(8):
    row = []
    for j in range(8):
        button = Button(root, text="", width=2, height=1)
        button.grid(row=i, column=j)
        row.append(button)
    board.append(row)

# fonction pour mettre à jour la grille


def update_board(board, move, player):
    """
    Met à jour la grille de jeu en fonction du mouvement du joueur

    Args:
        board (list): Une liste de listes représentant la grille de jeu
        move (tuple): Les coordonnées du mouvement du joueur sous forme d'un tuple (row, col)
        player (str): La chaîne de caractères représentant le joueur ('X' ou 'O')

    Returns:
        list: La grille de jeu mise à jour avec le nouveau mouvement
    """

    # Décompresse les coordonnées de mouvement en rangée et colonne
    row, col = move

    # Met à jour la case du tableau avec le joueur actuel
    board[row][col] = player

    # Parcours les huit directions autour de la case
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                  (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for d in directions:
        # Initialise le nombre de pièces adverses à retourner
        num_flips = 0

        # Parcours dans la direction donnée jusqu'à ce que l'on atteigne une pièce du joueur ou une case vide
        r, c = row + d[0], col + d[1]
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] != player and board[r][c] != ".":
            num_flips += 1
            r += d[0]
            c += d[1]

        # Si la dernière pièce atteinte est une pièce du joueur, on retourne toutes les pièces entre les deux
        if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player:
            r, c = row + d[0], col + d[1]
            for i in range(num_flips):
                board[r][c] = player
                r += d[0]
                c += d[1]

    return board


def is_on_board(row, col):
    """
    Vérifie si les coordonnées (ligne, colonne) se trouvent sur la grille de jeu

    Args:
        row (int): L'indice de la ligne
        col (int): L'indice de la colonne

    Returns:
        bool: True si les coordonnées sont sur la grille de jeu, False sinon
    """
    return row >= 0 and row <= 7 and col >= 0 and col <= 7


def is_valid_move(board, player, row, col):
    """
    Vérifie si le mouvement proposé par le joueur est valide

    Args:
        board (list): Une liste de listes représentant la grille de jeu
        player (str): La chaîne de caractères représentant le joueur qui joue ('X' ou 'O')
        row (int): L'indice de la ligne où le joueur veut jouer
        col (int): L'indice de la colonne où le joueur veut jouer

    Returns:
        bool: True si le mouvement est valide, False sinon
    """
    if board[row][col] != '.':
        return False

    board[row][col] = player

    # Vérifie si le mouvement encadre des pièces adverses
    is_valid = False
    for dr, dc in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
        r, c = row + dr, col + dc
        while is_on_board(r, c) and board[r][c] != player and board[r][c] != '.':
            r += dr
            c += dc
        if is_on_board(r, c) and board[r][c] == player:
            while True:
                r -= dr
                c -= dc
                if r == row and c == col:
                    break
                is_valid = True
    board[row][col] = '.'

    return is_valid


def get_valid_moves(board, player):
    """
    Renvoie une liste de mouvements valides pour le joueur sur la grille de jeu

    Args:
        board (list): Une liste de listes représentant la grille de jeu
        player (str): La chaîne de caractères représentant le joueur qui joue ('X' ou 'O')

    Returns:
        list: Une liste de tuples représentant les mouvements valides pour le joueur sous la forme (row, col)
    """
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if is_valid_move(board, player, row, col):
                valid_moves.append((row, col))
    return valid_moves


    
     
# fonction pour déterminer le gagnant


def determine_winner(board):
    """
    Détermine le gagnant d'une partie d'Othello

    Args:
        board (list): Une liste de listes représentant la grille de jeu

    Returns:
        str: La chaîne de caractères représentant le joueur gagnant ('X' ou 'O')
    """

    num_x = 0
    num_o = 0
    for row in board:
        for cell in row:
            if cell == 'X':
                num_x += 1
            elif cell == 'O':
                num_o += 1

    if num_x > num_o:
        return 'X'
    elif num_o > num_x:
        return 'O'
    else:
        return 'tie'


    # interface pour le joueur
player1 = Entry(root)
player1.grid(row=8, column=0)
player2 = Entry(root)
player2.grid(row=8, column=7)

button = Button(root, text="Start Game", command=update_board)
button.grid(row=8, column=3)

# boutons pour les mouvements
for i in range(8):
    for j in range(8):
        board[i][j].config(command=lambda row=i, col=j: make_move(row, col))

# fonction pour les mouvements du joueur


def make_move(board, player, row, col):
    """
    Effectue le mouvement du joueur sur la grille de jeu

    Args:
        board (list): Une liste de listes représentant la grille de jeu
        player (str): La chaîne de caractères représentant le joueur qui joue ('X' ou 'O')
        row (int): L'indice de la ligne où le joueur veut jouer
        col (int): L'indice de la colonne où le joueur veut jouer

    Returns:
        bool: True si le mouvement est valide et a été effectué, False sinon
    """

    # Vérifie si le mouvement est valide
    if not is_valid_move(board, player, row, col):
        return False

    # Effectue le mouvement
    board[row][col] = player

    # Inverse les pièces adverses encadrées
    for dr, dc in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
        r, c = row + dr, col + dc
        while is_on_board(r, c) and board[r][c] != player and board[r][c] != '.':
            r += dr
            c += dc
        if is_on_board(r, c) and board[r][c] == player:
            while True:
                r -= dr
                c -= dc
                if r == row and c == col:
                    break
                board[r][c] = player

    return True

root.mainloop()
