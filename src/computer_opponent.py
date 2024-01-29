def computer_move(gameboard, possible_moves):
    for i in reversed(range(24)):
        if not possible_moves:
            break

        if gameboard.board[i] >= 0:
            continue

        for move in possible_moves:
            if gameboard.make_move(i, move, -1):
                possible_moves.remove(move)
                continue
