#include <cstring>
#include <string>
#include <iostream>

using namespace std;

class Board {
public:
    string moves;

    Board make_move(string uci_coordinate);
};

Board Board::make_move(string uci_coordinate) {
    Board board;

    board.moves += uci_coordinate + " ";

    return board;
}

int main() {
    Board game_board;
    //searcher = Search()

    std::string line;

    while (1) {
        // try
            std::getline( std::cin, line );

            if (line == "quit") {
                exit(1);
            } else if (line == "uci") {
                cout << "pygone 1.5.4\nuciok\n";
            } else if (line == "ucinewgame") {
                //     game_board = Board()
                //     searcher.reset()
            } else if (line == "isready") {
                cout << "readyok\n";
            } else if (line.rfind("position", 0) == 0) {

                string moves = line.erase(0, 24);

                int i = 0;
                int pos = 0;

                string move = "";

                for(int i = 0; i < moves.length(); i++) {
                    if (moves[i] != ' ') {
                        move += moves[i];
                    } else {
                        game_board = game_board.make_move(move);
                        move = "";
                    }
                }

                game_board = game_board.make_move(move);

                cout << game_board.moves << endl;
            }


            // elif line.startswith("position fen"):
            //     fens = line.split(' ')
            //     position = fens[2].split('/')

            //     position = 21
            //     for piece in fens[2]:
            //         if piece == '/':
            //             position += 2
            //         else:
            //             if piece.isnumeric():
            //                 skip_count = int(piece)
            //                 while skip_count > 0:
            //                     game_board.mutate_board(position, '-')
            //                     position += 1
            //                     skip_count -= 1
            //             else:
            //                 game_board.mutate_board(position, piece)
            //                 if piece.isupper():
            //                     game_board.rolling_score += ALLPSQT[piece.lower()][position]
            //                     if piece == 'K':
            //                         for row in range(12):
            //                             position = row * 10
            //                         game_board.white_king_position = position_to_coordinate(position)
            //                 else:
            //                     game_board.rolling_score -= ALLPSQT[piece.lower()][abs(position - 119)]
            //                     if piece == 'k':
            //                         game_board.black_king_position = position_to_coordinate(position)
            //                 position += 1

            //     for castling in fens[4]:
            //         if castling == '-':
            //             game_board.white_castling = [False, False]
            //             game_board.black_castling = [False, False]
            //         elif castling == 'K':
            //             game_board.white_castling[1] = True
            //         elif castling == 'Q':
            //             game_board.white_castling[0] = True
            //         elif castling == 'k':
            //             game_board.black_castling[1] = True
            //         elif castling == 'q':
            //             game_board.black_castling[0] = True

            //     game_board.en_passant = fens[5]

            //     game_board.board_string = game_board.str_board()
            //     game_board.piece_count = game_board.get_piece_count()

            //     if len(fens) > 6:
            //         game_board.move_counter = int(fens[6])
            //         game_board.played_move_count = int(fens[7]) * 2
            //     if fens[3] == 'b':
            //         game_board.played_move_count += 1
            // elif line.startswith("print"):
            //     for row in range(12):
            //         position = row * 10
            //         print(game_board.board_state[position:position+10])
            //     print(game_board.played_move_count, game_board.in_check(game_board.played_move_count % 2 == 0))
            // elif line.startswith("position"):
            //     moves = line.split()
            //     game_board = Board()
            //     for position_move in moves[3:]:
            //         game_board = game_board.make_move(position_move)
            // elif line.startswith("go"):
            //     searcher.v_depth = 30
            //     move_time = 1e8
            //     is_white = game_board.played_move_count % 2 == 0

                // is_perft = False

                // args = line.split()
                // for key, arg in enumerate(args):
                //     if arg == 'wtime' and is_white or arg == 'btime' and not is_white:
                //         move_time = int(args[key + 1]) / 1e3
                    // depth input can be commented out to save space since engine will be run on time
                    // elif arg == 'depth':
                    //     searcher.v_depth = int(args[key + 1])
                //     elif arg == 'perft':
                //         searcher.v_depth = int(args[key + 1])
                //         is_perft = True

                // if is_perft:
                //     // 1) start pos
                //     // 2) Kiwipete: position startpos moves b1c3 b7b5 d2d4 e7e6 e2e4 c8a6 c1d2 h7h5 d1f3 g7g6 f1e2 h5h4 g1h3 f8g7 h3f4 g8e7 f4d3 e7d5 d3e5 d5f6 d4d5 d8e7 d2e3 b5b4 e3d2 b8c6 d2e3 c6a5 e3d2 a5c4 d2e3 c4b6 e3d2 h4h3
                //     // 3) Tricky Steve: position startpos moves d2d3 c7c6 e2e4 e7e5 d3d4 f8e7 d4e5 d7d6 e5d6 g8f6 f1c4 f6e4 d6d7 e8f8 g1e2 e4f2
                //     start_time = t()
                //     searcher.perft_checks = 0
                //     searcher.perft_captures = 0
                //     searcher.run_perft(game_board, searcher.v_depth, searcher.v_depth)
                //     print("total time: ", t() - start_time)
                //     continue

                // searcher.critical_time = t() + max(0.75, move_time - 1)
                // move_time = max(2.2, move_time / 32)

                // searcher.end_time = t() + move_time

                // searcher.v_nodes = 0

                // s_move = None

                // for v_depth, s_move, best_score in searcher.iterative_search(game_board):
                //     if v_depth >= searcher.v_depth or t() >= searcher.end_time:
                //         break

                // ponder_board = game_board.make_move(s_move)
                // ponder_bucket = searcher.self.tt_bucket.get(ponder_board.board_string)
                // ponder = ""
                // if ponder_bucket:
                //     ponder = f" ponder {ponder_bucket['tt_move']}"

                // print_to_terminal(f"bestmove {str(s_move)}{ponder}")

                // print_to_terminal(f"bestmove {str(s_move)}")
    }
}