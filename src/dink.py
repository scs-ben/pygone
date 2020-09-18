import math

board_state = 'rnbqkbnr' + 'p'*8 + '-'*32 + 'P'*8 + 'RNBQKBNR'

for meh in range(8):
    row = meh * 8
    column = row + 8
    print(board_state[row:column])

print(board_state)