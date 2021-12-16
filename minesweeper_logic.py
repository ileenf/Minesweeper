from Board import in_bounds


def reveal_cells(board, row, col):
    # reveal the cell and any adjacent cells until reaches cell next to bomb or edge of board
    cell_stack = [row, col]

    while cell_stack:
        col = cell_stack.pop()
        row = cell_stack.pop()
        if not board[row][col].get_flagged():
            board[row][col].reveal()
        if board[row][col].get_adjacent_bombs() == 0:
            if row + 1 < 10 and board[row + 1][col].is_hidden() and not board[row + 1][col].get_flagged():
                cell_stack.append(row + 1)
                cell_stack.append(col)
            if col + 1 < 10 and board[row][col + 1].is_hidden() and not board[row][col + 1].get_flagged():
                cell_stack.append(row)
                cell_stack.append(col + 1)
            if row - 1 >= 0 and board[row - 1][col].is_hidden() and not board[row - 1][col].get_flagged():
                cell_stack.append(row - 1)
                cell_stack.append(col)
            if col - 1 >= 0 and board[row][col - 1].is_hidden() and not board[row][col - 1].get_flagged():
                cell_stack.append(row)
                cell_stack.append(col - 1)
            if row - 1 >= 0 and col - 1 >= 0 and board[row - 1][col - 1].is_hidden() and not board[row - 1][
                col - 1].get_flagged():
                cell_stack.append(row - 1)
                cell_stack.append(col - 1)
            if row - 1 >= 0 and col + 1 < 10 and board[row - 1][col + 1].is_hidden() and not board[row - 1][
                col + 1].get_flagged():
                cell_stack.append(row - 1)
                cell_stack.append(col + 1)
            if row + 1 < 10 and col - 1 >= 0 and board[row + 1][col - 1].is_hidden() and not board[row + 1][
                col - 1].get_flagged():
                cell_stack.append(row + 1)
                cell_stack.append(col - 1)
            if row + 1 < 10 and col + 1 < 10 and board[row + 1][col + 1].is_hidden() and not board[row + 1][
                col + 1].get_flagged():
                cell_stack.append(row + 1)
                cell_stack.append(col + 1)


def player_move(board, action, row, col):
    if not in_bounds(row, col, len(board), len(board[row])):
        return -1

    cell = board[row][col]
    if action.lower() == 'f':
        # invalid if flag a revealed cell
        if cell.get_revealed():
            return -1
        # if already flagged, remove flag
        if cell.get_flagged():
            cell.remove_flag()
            return 1
        else:
            cell.flag()
    elif action.lower() == 'r':
        # invalid if revealing already revealed cell
        if cell.get_revealed():
            return -1

        reveal_cells(board, row, col)
        if cell.get_flagged():
            cell.remove_flag()
            cell.reveal()
            return 1
    else:
        return -1

    return 0


def game_status(board):
    all_and_only_bombs_flagged = True
    for row in range(len(board)):
        for col in range(len(board[row])):
            cell = board[row][col]

            if cell.get_bomb():
                # if cell with bomb revealed, game lost
                if cell.get_revealed():
                    return -1
                # if bomb not flagged, cannot win
                if not cell.get_flagged():
                    all_and_only_bombs_flagged = False
            else:
                # if no bomb but cell is flagged, cannot win
                if cell.get_flagged():
                    all_and_only_bombs_flagged = False

    if all_and_only_bombs_flagged:
        # won game
        return 1
    else:
        # game ongoing
        return 0


def map_reveal(board, row, col):
    # reveal all cells in board
    for r in range(len(board)):
        for c in range(len(board[row])):
            cell = board[r][c]
            cell.reveal()

            if r == row and c == col:
                # set exploding bomb at row, col
                cell.set_exploding_bomb()
