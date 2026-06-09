#!/usr/bin/env pypy3
#  pygone - A Python Chess Engine
#  Copyright (C) 2026 scs-ben
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
import time
from search import Search
from board import Board
#remove
import sys, traceback
#endremove
#UNITremove
from perft import Perft
from unit import Unit
#UNITendremove

def main():
    game_board = Board()
    searcher = Search(game_board)

    while 1:
        #remove
        try:
        #endremove
            line = input()
            if line == "quit":
                return
            elif line == "uci":
                print("pygone\nuciok", flush=True)
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
                side_time, side_inc, movestogo = 1e8, 0, 0
                #remove
                v_depth = 0
                perft_depth = 0
                #endremove
                
                args = line.split()
                us = game_board.white_to_move
                for k, a in enumerate(args):
                    if a == ('wtime' if us else 'btime'):
                        side_time = int(args[k + 1]) / 1e3
                    elif a == ('winc' if us else 'binc'):
                        side_inc = int(args[k + 1]) / 1e3
                    elif a == 'movestogo':
                        movestogo = int(args[k + 1])
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
 
                m = movestogo or (30 if len(game_board.stack) < 40 else 60)
                searcher.end_time = time.time() + max(0.1, side_time / m + side_inc - 0.5); searcher.time_up = False
                
                #remove
                if v_depth > 0:
                    searcher.end_time = time.time() + max(0.1, side_time / m + side_inc - 0.5)
                    searcher.time_up = False
                    searcher.set_depth(v_depth)
                #endremove

                searcher.iterative_search()
            #remove
            elif line.startswith('print'):
                game_board.print_board()
            #endremove
        #remove
        except Exception as exc:
            print(exc, flush=True)
            traceback.print_stack(limit=2, file=sys.stdout)
            print(exc, flush=True)
            raise
        except (KeyboardInterrupt, SystemExit):
            return
        #endremove

main()
