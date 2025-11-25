#!/usr/bin/env pypy3
#  pygone - A Python Chess Engine
#  Copyright (C) 2025 [Your Name/Handle]
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
from search import Search
from board import Board
#UNITremove
from perft import Perft
from unit import Unit
#UNITendremove

def main():
    game_board = Board()
    searcher = Search(game_board)

    while 1:
        try:
            line = input()
            if line == "quit":
                return
            elif line == "uci":
                print("pygone2\nuciok", flush=True)
            #remove
            elif line == "ucinewgame":
                game_board = Board()
                searcher = Search(game_board)
            #endremove
            elif line == "isready":
                print("readyok", flush=True)
            #UNITremove
            elif line == "unit":
                unit = Unit()
                b = Board()
                unit.unit_hash(b)
                b = Board()
                perft = Perft(b)
                unit.unit_perft(perft, b)
                b = Board()
                unit.unit_moves(b)
                b = Board()
                unit.unit_scoring(b)
                b = Board()
                unit.unit_castling(b)
                b = Board()
                unit.unit_ep(b)
                b = Board()
                unit.unit_promo(b)
                b = Board()
                b.set_fen("r1bqk1nr/2p2ppp/1pp5/2b1p3/p3P3/2NP1N2/PPP2PPP/R1BQ1RK1 w kq - 0 9")
                s = Search(b)
                unit.unit_search(s, b)
                b = Board()
                s = Search(b)
                unit.unit_threefold(s, b)
                # b = Board()
                # unit.unit_insufficient_material(b)
                b = Board()
                unit.unit_game_end(b)
                b = Board()
                s = Search(b)
                unit.unit_mate_in_n(s, b)
                b = Board()
                unit.unit_fifty_move(b)
                b = Board()
                unit.unit_legality(b)
                b = Board()
                unit.unit_attack_resolution(b)
                print("Unit testing completed")
            #UNITendremove
            #remove
            elif line.startswith("position fen"):
                cmd = line[9:]
                
                game_board = Board()
                searcher = Search(game_board)
                # Extract FEN before the "moves" keyword if present
                fen_section = cmd[len("fen "):]
                if " moves " in fen_section:
                    fen, moves_section = fen_section.split(" moves ", 1)
                else:
                    fen, moves_section = fen_section, ""
                game_board.set_fen(fen)
                
                if moves_section:
                    cmd = moves_section.split(" ")
                    
                    for position_move in cmd:
                        from_sq = game_board.algebraic_to_sq(position_move[:2])
                        to_sq = game_board.algebraic_to_sq(position_move[2:4])
                        promo = position_move[4] if len(position_move) == 5 else None
                        
                        game_board.make_move((from_sq, to_sq, promo, None, None, False))
            #endremove
            elif line[:8]=="position":
                game_board = Board()
                
                moves = line.split()
                
                for position_move in moves[3:]:                    
                    game_board.make_move((game_board.algebraic_to_sq(position_move[:2]), game_board.algebraic_to_sq(position_move[2:4]), position_move[4] if len(position_move) == 5 else None, None, None, False))
                    
                searcher.set_board(game_board)
            elif line[:2]=="go":
                side_time = 1e8
                #remove
                v_depth = 0
                perft_depth = 0
                #endremove
                
                args = line.split()
                for k, a in enumerate(args):
                    if a == 'wtime' and game_board.white_to_move or a == 'btime' and not game_board.white_to_move:
                        side_time = int(args[k + 1]) / 1e3
                    #remove
                    elif a == 'depth':
                        v_depth = int(args[k + 1])
                    elif a == 'perft':
                        perft_depth = int(args[k + 1])
                    #endremove
                #remove
                if perft_depth:
                    perft = Perft(game_board)
                    perft.run(perft_depth)
                    continue
                #endremove
                
                #remove
                searcher.set_depth(50)
                #endremove

                searcher.set_time_limit(side_time / 50)
                
                #remove
                if v_depth > 0:
                    searcher.set_time_limit(1e8)
                    searcher.set_depth(v_depth)
                #endremove

                searcher.iterative_search()
            #remove
            elif line.startswith('print'):
                game_board.print_board()
            #endremove
        except Exception as exc:
            print(exc, flush=True)
            raise
        #remove
        except (KeyboardInterrupt, SystemExit):
            return
        #endremove

main()
