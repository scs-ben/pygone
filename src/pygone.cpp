#include <algorithm>
#include <cmath>
#include <cstring>
#include <cctype>
#include <ctime>
#include <chrono>
#include <functional>
#include <limits>
#include <map>
#include <random>
#include <string>
#include <iostream>
#include <vector>

using namespace std;

string PIECES = "pnbrqk";

map<char, int> PIECEPOINTS
{
    {'p', 100},
    {'n', 320},
    {'b', 325},
    {'r', 500},
    {'q', 975},
    {'k', 32767}
};

uint64_t ZobristTable[8][8][12];
random_device rd;
mt19937_64 eng(rd());

uint64_t random_uint64()
{
    uniform_int_distribution<uint64_t> distr;
    return distr(eng);
}

uint64_t black_to_move = random_uint64();

void init_table()
{
    for (int i = 0; i<8; i++) {
        for (int j = 0; j<8; j++) {
            for (int k = 0; k<12; k++) {
                ZobristTable[i][j][k] = random_uint64();
            }
        }
    }
}

int index_of(char piece)
{
    if (piece=='P')
        return 0;
    if (piece=='N')
        return 1;
    if (piece=='B')
        return 2;
    if (piece=='R')
        return 3;
    if (piece=='Q')
        return 4;
    if (piece=='K')
        return 5;
    if (piece=='p')
        return 6;
    if (piece=='n')
        return 7;
    if (piece=='b')
        return 8;
    if (piece=='r')
        return 9;
    if (piece=='q')
        return 10;
    if (piece=='k')
        return 11;
    else
        return -1;
}

map<char, array<int, 120>> ALLPSQT
{
    {'p', {
        0,  0,  0,  0,  0,      0,      0,  0,  0,  0,
        0,  0,  0,  0,  0,      0,      0,  0,  0,  0,
        0,  0,  0,  0,  0,      0,      0,  0,  0,  0,
        0,  30, 30, 30, 30,     30,     30, 30, 30, 0,
        0,  8,  8,  17, 26,     26,     17, 8,  8,  0,
        0,  5,  5,  8,  24,     24,     8,  5,  5,  0,
        0,  0,  0,  0,  24,     24,     0,  0,  0,  0,
        0,  5,  -5, -8, 6,      6,      -8, -5, 5,  0,
        0,  5,  8,  8,  -22,    -22,    8,  8,  5,  0,
        0,  0,  0,  0,  0,      0,      0,  0,  0,  0,
        0,  0,  0,  0,  0,      0,      0,  0,  0,  0,
        0,  0,  0,  0,  0,      0,      0,  0,  0,  0}
    },
    {'n', {
        0,  0,      0,      0,      0,      0,      0,      0,      0,      0,
        0,  0,      0,      0,      0,      0,      0,      0,      0,      0,
        0,  -50,    -40,    -30,    -30,    -30,    -30,    -40,    -50,    0,
        0,  -40,    -20,    0,      0,      0,      0,      -20,    -40,    0,
        0,  -30,     0,     8,      13,     13,     8,      0,      -30,    0,
        0,  -30,     5,     13,     18,     18,     13,     5,      -30,    0,
        0,  -30,     0,     13,     18,     18,     13,     0,      -30,    0,
        0,  -30,     5,     7,      13,     13,     7,      5,      -30,    0,
        0,  -40,    -20,    0,      5,      5,      0,      -20,    -40,    0,
        0,  -50,    -40,    -20,    -30,    -30,    -20,    -40,    -50,    0,
        0,  0,      0,      0,      0,      0,      0,      0,      0,      0,
        0,  0,      0,      0,      0,      0,      0,      0,      0,      0}
    },
    {'b', {
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,-20,-10,-10,-10,-10,-10,-10,-20,0,
        0,-10, 0, 0, 0, 0, 0, 0,-10,0,
        0,-10, 0, 5,10,10, 5, 0,-10,0,
        0,-10, 5, 5,10,10, 5, 5,-10,0,
        0,-10, 0,10,10,10,10, 0,-10,0,
        0,-10,10,10,10,10,10,10,-10,0,
        0,-10, 5, 0, 0, 0, 0, 5,-10,0,
        0,-20,-10,-40,-10,-10,-40,-10,-20,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0}
    },
    {'r', {
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,10,20,20,20,20,20,20, 10,0,
        0,-10, 0, 0, 0, 0, 0, 0,-10,0,
        0,-10, 0, 0, 0, 0, 0, 0,-10,0,
        0,-10, 0, 0, 0, 0, 0, 0,-10,0,
        0,-10, 0, 0, 0, 0, 0, 0,-10,0,
        0,-10, 0, 0, 0, 0, 0, 0,-10,0,
        0,-10, 0, 0, 0, 0, 0, 0,-10,0,
        0,-10, 0, 0,10,10, 10, 0,-10,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0}
    },
    {'q', {
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,-40,-20,-20,-10,-10,-20,-20,-40,0,
        0,-20, 0, 0, 0, 0, 0, 0,-20,0,
        0,-20, 0,10,10,10,10, 0,-20,0,
        0,-10, 0,10,10,10,10, 0,-10,0,
        0,0, 0,10,10,10,10, 0,-10,0,
        0,-20,10,10,10,10,10, 0,-20,0,
        0,-20, 0,10, 0, 0, 0, 0,-20,0,
        0,-40,-20,-20,-10,-10,-20,-20,-40,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0}
    },
    {'k', {
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,-50,-40,-30,-20,-20,-30,-40,-50,0,
        0,-30,-20,-10, 0, 0,-10,-20,-30,0,
        0,-30,-10,20,30,30,20,-10,-30,0,
        0,-30,-10,30,40,40,30,-10,-30,0,
        0,-30,-10,30,40,40,30,-10,-30,0,
        0,-10,-20,-20,-20,-20,-20,-20,-10,0,
        0,20,20,0,0,0,0,20,20,0,
        0,20,20,35,0,0,10,35,20,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0}
    }
};

vector<array<int, 2>> get_moves(char piece) {
    vector<array<int, 2>> moves;

    if (piece == 'k') {
        moves = {{0, 10}, {0, -10}, {1, 0}, {-1, 0}, {1, 10}, {1, -10}, {-1, 10}, {-1, -10}};
    } else if (piece == 'q') {
        moves = {{0, 10}, {0, -10}, {1, 0}, {-1, 0}, {1, 10}, {1, -10}, {-1, 10}, {-1, -10}};
    } else if (piece == 'r') {
        moves = {{0, 10}, {0, -10}, {1, 0}, {-1, 0}};
    } else if (piece == 'b') {
        moves = {{1, 10}, {1, -10}, {-1, 10}, {-1, -10}};
    } else if (piece == 'n') {
        moves = {{1, -20}, {-1, -20}, {2, -10}, {-2, -10}, {1, 20}, {-1, 20}, {2, 10}, {-2, 10}};
    } else {
        moves = {{0, -10}, {1, -10}, {-1, -10}};
    }

    return moves;
}

char number_to_letter(int to_number) {
    return 96 + to_number;
}

void print_stats(string v_depth, string v_score, string v_time, string v_nodes, string v_nps, string v_pv) {
    cout << "info depth " << v_depth << " score cp " << v_score << " time " << v_time << " nodes " << v_nodes << " nps " << v_nps << " pv " << v_pv << endl;
}

int coordinate_to_position(string coordinate) {
    char letter = coordinate[0];
    int number = coordinate[1] - '0';

    int position = letter - 97;

    return 10 * (abs(number - 8) + 2) + position + 1;
}

tuple<int, int> unpack_coordinate(string uci_coordinate) {
    return {coordinate_to_position(uci_coordinate.substr(0, 2)),
            coordinate_to_position(uci_coordinate.substr(2, 4))};
}

string position_to_coordinate(int board_position) {
    return number_to_letter(board_position % 10) + to_string(abs(board_position / 10 - 10));
}

uint64_t get_time() {
    return chrono::duration_cast<chrono::milliseconds>(chrono::system_clock::now().time_since_epoch()).count();
}

hash<std::string> hasher;

struct [[nodiscard]] Move {
    int score;
    string coordinate;

    bool operator() (Move i,Move j) { return (i.score > j.score); };
} struct_move;

class Board {
public:
    string board_state = "";
    string board_string = "";
    int played_move_count = 0;
    vector<string> repetitions = {};
    bool white_castling[2] = {true, true};
    bool black_castling[2] = {true, true};
    string white_king_position = "e1";
    string black_king_position = "e8";
    int rolling_score = 0;
    int piece_count = 32;
    string en_passant = "";
    int move_counter = 0;

    Board() {
        board_state = ".....................rnbqkbnr..pppppppp..--------..--------..--------..--------..PPPPPPPP..RNBQKBNR.....................";
        board_string = str_board();
            // '..........'   0 -  9
            // '..........'  10 - 19
            // '.rnbqkbnr.'  20 - 29
            // '.pppppppp.'  30 - 39
            // '.--------.'  40 - 49
            // '.--------.'  50 - 59
            // '.--------.'  60 - 69
            // '.--------.'  70 - 79
            // '.PPPPPPPP.'  80 - 89
            // '.RNBQKBNR.'  90 - 99
            // '..........' 100 -109
            // '..........' 110 -119
    }

    Board board_copy();
    Board make_move(string uci_coordinate);
    Board nullmove();
    void mutate_board(int board_position, char piece);
    void apply_move(string uci_coordinate);
    int get_piece_count();
    bool check_is_endgame();
    int calculate_score(string uci_coordinate, bool sorting=false);
    bool passer_pawn(int board_position);
    bool stacked_pawn(int board_position);
    string str_board();
    uint64_t hash_board();
    vector<struct Move> generate_valid_captures();
    vector<struct Move> generate_valid_moves(bool captures_only=false);
    bool in_check(bool is_white);
    bool attack_position(bool is_white, string coordinate);
};

Board Board::board_copy() {
    // copy the board, does not copy the score
    Board board;

    board.played_move_count = played_move_count;
    board.white_king_position = white_king_position;
    board.black_king_position = black_king_position;
    board.board_string = board_string;
    board.piece_count = piece_count;
    board.en_passant = en_passant;
    board.move_counter = move_counter;
    board.board_state = board_state;
    board.repetitions = repetitions;
    memcpy(board.white_castling, white_castling, 2);
    memcpy(board.black_castling, black_castling, 2);

    return board;
}

Board Board::make_move(string uci_coordinate) {
    // making the move will return an altered copy of the current state
    // this allows us to avoid "undoing" the move
    Board board = board_copy();

    // should calc score before moving
    board.rolling_score = rolling_score + calculate_score(uci_coordinate);

    // set castling rights
    if (uci_coordinate.find("e1") < 100) {
        board.white_castling[0] = false;
        board.white_castling[1] = false;
    } else if (uci_coordinate.find("a1") < 100) {
        board.white_castling[0] = false;
    } else if (uci_coordinate.find("h1") < 100) {
        board.white_castling[1] = false;
    }

    if (uci_coordinate.find("e8") < 100) {
        board.black_castling[0] = false;
        board.black_castling[1] = false;
    } else if (uci_coordinate.find("a8") < 100) {
        board.black_castling[0] = false;
    } else if (uci_coordinate.find("h8") < 100) {
        board.black_castling[1] = false;
    }

    board.apply_move(uci_coordinate);

    board.played_move_count += 1;
    board.rolling_score = -board.rolling_score;

    board.repetitions.push_back(board.board_string);

    return board;
}

Board Board::nullmove() {
    // allows for a quick way to let other side move
    // making the move will return an altered copy of the current state
    // this allows us to avoid "undoing" the move
    Board board = board_copy();
    board.played_move_count += 1;
    board.rolling_score = -rolling_score;

    return board;
}

void Board::mutate_board(int board_position, char piece) {
    board_state = board_state.substr(0, board_position) + piece + board_state.substr(board_position + 1, board_state.length());
}

void Board::apply_move(string uci_coordinate) {
    bool is_white = played_move_count % 2 == 0;

    move_counter += 1;

    // break uci coordinate into location in board state list
    tuple<int, int> unpack;
    unpack = unpack_coordinate(uci_coordinate);

    int from_number = get<0>(unpack);
    int to_number = get<1>(unpack);

    char from_piece = tolower(board_state[from_number]);

    if (board_state[to_number] != '-') {
        move_counter = 0;
    }

    mutate_board(to_number, board_state[from_number]);
    mutate_board(from_number, '-');

    bool set_en_passant = false;

    if (from_piece == 'p') {
        move_counter = 0;
        set_en_passant = abs(from_number - to_number) == 20;
        int en_passant_offset = is_white ? -1 : 1;
        if (set_en_passant) {
            en_passant = uci_coordinate[0] + to_string(uci_coordinate[3] - '0' + en_passant_offset);
        } else if (uci_coordinate.substr(2,2) == en_passant) {
            mutate_board(to_number - 10 * en_passant_offset, '-');
        } else if (uci_coordinate.length() > 4) {
            mutate_board(to_number, is_white ? toupper(uci_coordinate[4]) : uci_coordinate[4]);
        }
    } else if (from_piece == 'k') {
        if (is_white) {
            white_king_position = uci_coordinate.substr(2, 2);
        } else {
            black_king_position = uci_coordinate.substr(2, 2);
        }

        if (abs(to_number - from_number) == 2) {
            mutate_board(to_number + (to_number > from_number ? 1 : -2), '-');
            mutate_board(from_number + ((to_number - from_number) / 2), is_white ? 'R' : 'r');
        }
    }

    if (!set_en_passant) {
        en_passant = "";
    }

    board_string = str_board();
    piece_count = get_piece_count();
}

int Board::get_piece_count() {
    int piece_count = 0;
    for (int i = 21; i < 99; i++) {
        if (board_state[i] != '.' && board_state[i] != '-') {
            ++piece_count;
        }
    }
    return piece_count;
}

bool Board::check_is_endgame() {
    return piece_count < 14;
}

int Board::calculate_score(string uci_coordinate, bool sorting) {
    bool is_white = played_move_count % 2 == 0;
    int offset = is_white ? 0 : 119;
    int p_offset = is_white ? -10 : 10;
    char p_piece = is_white ? 'P' : 'p';
    bool is_endgame = check_is_endgame();

    tuple<int, int> unpack;
    unpack = unpack_coordinate(uci_coordinate);

    int from_number = get<0>(unpack);
    int to_number = get<1>(unpack);

    int local_score = 0;

    char from_piece = tolower(board_state[from_number]);

    char to_piece = tolower(board_state[to_number]);

    local_score += ALLPSQT[from_piece][abs(to_number - offset)] - ALLPSQT[from_piece][abs(from_number - offset)];

    if (to_piece != '-') {
        local_score += ALLPSQT[to_piece][abs(to_number - offset)];
    }

    if (from_piece == 'p') {
        if (uci_coordinate.substr(2, 2) == en_passant) {
            // add in an extra pawn for EP capture
            local_score += ALLPSQT[from_piece][abs(to_number - offset)];
        } else if (uci_coordinate.length() > 4) {
            char promote = uci_coordinate[4];
            // adjust value for promoting from pawn to queen
            local_score += ALLPSQT[promote][abs(to_number - offset)] - ALLPSQT['p'][abs(to_number - offset)];
        }

        if (passer_pawn(from_number)) {
            local_score += 10;
        }
        if (stacked_pawn(from_number)) {
            local_score -= 15;
        }
    } else if (from_piece == 'k') {
        if (abs(to_number - from_number) == 2) {
            if (to_number > from_number) {
                local_score += ALLPSQT['r'][abs(to_number - offset) - 1] - ALLPSQT['r'][abs(to_number - offset) + 1];
            } else {
                local_score += ALLPSQT['r'][abs(to_number - offset) + 1] - ALLPSQT['r'][abs(to_number - offset) - 2];
            }

            // put castling higher up
            if (sorting) {
                local_score += 60;
            }
        }
    }

    return local_score;
}

bool Board::passer_pawn(int board_position) {
    bool is_white = played_move_count % 2 == 0;
    int p_offset = is_white ? -10 : 10;
    int start_position = board_position + p_offset;

    int piece_count = 1;
    while (start_position >= 20 && start_position <= 100) {
        if (board_state[start_position] != '.' && board_state[start_position] != '-') {
            return false;
        }
        start_position += p_offset;
    }

    return true;
}

bool Board::stacked_pawn(int board_position) {
    bool is_white = played_move_count % 2 == 0;
    int p_offset = is_white ? -10 : 10;
    char p_piece = is_white ? 'P' : 'p';

    int start_position = board_position + p_offset;

    while (start_position >= 20 && start_position <= 100) {
        if (board_state[start_position] == p_piece) {
            return true;
        }
        start_position += p_offset;
    }

    return false;
}

string Board::str_board() {
    return board_state + to_string(played_move_count % 2);
}

uint64_t Board::hash_board()
{
    uint64_t h = 0;

    if (played_move_count % 2 != 0) {
        h ^= black_to_move;
    }

    int start_position = 20;
    int row = 0;
    int column = 0;

    while (start_position < 99) {
        if (board_state[start_position] != '.' && board_state[start_position] != '-') {
            row = (start_position - 20) / 10;
            column = (start_position % 10) - 1;

            int piece = index_of(board_state[start_position]);

            h ^= ZobristTable[column][row][piece];
        }
        start_position++;
    }



    return h;
}

vector<struct Move> Board::generate_valid_captures() {
    return generate_valid_moves(true);
}

vector<struct Move> Board::generate_valid_moves(bool captures_only) {
    // Return list of valid (maybe illegal) moves
    int offset = 1;

    bool is_white = false;

    int board_position = 21;
    int max_row = 31;
    int min_row = 81;
    string valid_pieces = "PRNBQK-";

    if (played_move_count % 2 == 0) {
        is_white = true;

        max_row = 81;
        min_row = 31;
        valid_pieces = "prnbqk-";
    }

    vector<struct Move> valid_moves;
    Move move;

    while (board_position > 20 && board_position < 99) {
        char piece = board_state[board_position];

        if (piece == '-' || piece == '.' || valid_pieces.find(piece) < 100) {
            board_position += 1;
            continue;
        }

        string start_coordinate = position_to_coordinate(board_position);

        char piece_lower = tolower(piece);

        if (piece == 'p') {
            offset = -1;
        }

        // castling and double pawn move off home position
        if (!captures_only) {
            if (piece == 'K') {
                if (white_castling[1] && board_state.substr(96, 3) == "--R" &&
                        !attack_position(is_white, "e1") && !attack_position(is_white, "f1") && !attack_position(is_white, "g1")) {
                    move.coordinate = start_coordinate + "g1";
                    move.score = 0;
                    valid_moves.push_back(move);
                }
                if (white_castling[0] && board_state.substr(91, 4) == "R---" &&
                        !attack_position(is_white, "e1") && !attack_position(is_white, "d1") && !attack_position(is_white, "c1")) {
                    move.coordinate = start_coordinate + "c1";
                    move.score = 0;
                    valid_moves.push_back(move);
                }
            } else if (piece == 'k') {
                if (black_castling[1] && board_state.substr(26, 3) == "--r" &&
                        !attack_position(is_white, "e8") && !attack_position(is_white, "f8") && !attack_position(is_white, "g8")) {

                    move.coordinate = start_coordinate + "g8";
                    move.score = 0;
                    valid_moves.push_back(move);
                }
                if (black_castling[0] && board_state.substr(21, 4) == "r---" &&
                        !attack_position(is_white, "e8") && !attack_position(is_white, "d8") && !attack_position(is_white, "c8")) {
                    move.coordinate = start_coordinate + "c8";
                    move.score = 0;
                    valid_moves.push_back(move);
                }
            } else if (piece_lower == 'p' && board_position >= max_row && board_position < max_row + 8
                    && board_state[board_position + -10*offset] == '-' && board_state[board_position + -20*offset] == '-') {
                move.coordinate = start_coordinate + position_to_coordinate(board_position + -20*offset);
                move.score = 0;
                valid_moves.push_back(move);
            }
        }

        vector<array<int, 2>> piece_moves = get_moves(piece_lower);

        int to_position = 0;
        char eval_piece;

        for(array<int, 2> piece_move : piece_moves) {
            to_position = board_position + piece_move[0] + (piece_move[1] * offset);

            while (20 < to_position < 99) {
                eval_piece = board_state[to_position];

                if (!captures_only || (captures_only && eval_piece != '-' && eval_piece != '.')) {
                    string dest = position_to_coordinate(to_position);

                    if (piece_lower == 'p') {
                        if ((board_position >= min_row && board_position <= (min_row + 8) && piece_move[0] == 0 && eval_piece == '-') ||
                            (board_position >= min_row && board_position <= (min_row + 8) && piece_move[0] != 0 && eval_piece != '-' && valid_pieces.find(eval_piece) < 100)) {
                            for (char const &promote: "qrbn") {
                                move.coordinate = start_coordinate + dest + promote;
                                move.score = 0;
                                valid_moves.push_back(move);
                            }
                        } else {
                            if ((piece_move[0] == 0 && eval_piece == '-') ||
                                (piece_move[0] != 0 && eval_piece != '-' && valid_pieces.find(eval_piece) < 100) ||
                                dest == en_passant) {

                                move.coordinate = start_coordinate + dest;
                                move.score = 0;
                                valid_moves.push_back(move);
                            }
                        }
                    } else if (valid_pieces.find(eval_piece) < 100) {
                        move.coordinate = start_coordinate + dest;
                        move.score = 0;
                        valid_moves.push_back(move);
                    }
                }

                if (eval_piece != '-' || piece_lower == 'k' || piece_lower == 'n' || piece_lower == 'p') {
                    break;
                }

                to_position = to_position + piece_move[0] + (piece_move[1] * offset);
            }
        }


        board_position += 1;
    }

    return valid_moves;
}

bool Board::in_check(bool is_white) {
    string king_position = is_white ? white_king_position : black_king_position;

    return attack_position(is_white, king_position);
}

bool Board::attack_position(bool is_white, string coordinate) {
    int offset = 1;
    string valid_pieces = is_white ? "PRNBQK-" : "prnbqk-";

    int attack_position = coordinate_to_position(coordinate);

    int board_position = 21;

    while (board_position > 20 && board_position < 99) {
        char piece = board_state[board_position];
        if (piece == '-' || piece == '.' || valid_pieces.find(piece) < 100) {
            board_position += 1;
            continue;
        }

        if (piece == 'p') {
            offset = -1;
        }

        piece = tolower(piece);

        vector<array<int, 2>> piece_moves = get_moves(piece);

        int to_position = 0;
        char eval_piece;

        for(array<int, 2> piece_move : piece_moves) {
            to_position = board_position + piece_move[0] + (piece_move[1] * offset);

            if (piece == 'p' && !piece_move[0]) {
                continue;
            }

            to_position = board_position + piece_move[0] + (offset * piece_move[1]);

            while (20 < to_position < 99) {
                eval_piece = board_state[to_position];

                if (valid_pieces.find(eval_piece) < 100 && to_position == attack_position) {
                    return true;
                }

                if (eval_piece != '-' || piece == 'k' || piece == 'n' || piece == 'p') {
                    break;
                }

                to_position = to_position + piece_move[0] + offset * piece_move[1];
            }
        }

        board_position += 1;
    }

    return false;
}

struct [[nodiscard]] Node {
    int depth;
    int score;
    int flag;
    string coordinate;
};

uint64_t tt_size = pow(2, 24) - 1;
vector<Node> tt_bucket;

class Search {
public:
    int v_nodes = 0;
    uint64_t critical_time = 0;
    uint64_t end_time = 0;

    int eval_exact = 1;
    int eval_upper = 2;
    int eval_lower = 3;

    int eval_mate_upper = PIECEPOINTS['k'];

    void reset();
    string iterative_search(Board local_board, int depth);
    int search(Board local_board, int v_depth, int alpha, int beta);
    int quiesce(Board local_board, int alpha, int beta);

};

void Search::reset() {
    v_nodes = 0;
    critical_time = 0;
    end_time = 0;

    tt_bucket.clear();
    tt_bucket.resize(tt_size);
    memset(tt_bucket.data(), 0, sizeof(Node) * tt_bucket.size());
}

string Search::iterative_search(Board local_board, int depth) {
        uint64_t start_time = get_time();

        int local_score = local_board.rolling_score;

        string best_move;
        uint64_t elapsed_time;
        int v_nps;

        int v_depth = 1;

        Node tt_entry;

        while (v_depth <= depth) {
            local_score = search(local_board, v_depth, -eval_mate_upper, eval_mate_upper);

            if (get_time() < critical_time) {
                tt_entry = tt_bucket[local_board.hash_board() % (tt_size - 1)];
                if (!tt_entry.coordinate.empty()) {
                    best_move = tt_entry.coordinate;
                }
            } else {
                break;
            }

            elapsed_time = get_time() - start_time;

            v_nps = (elapsed_time > 1000) ? ceil(v_nodes / (elapsed_time / 1000)) : v_nodes;

            string pv = "";
            int counter = 1;
            Board pv_board = local_board.make_move(best_move);

            while (counter < min(12, v_depth)) {
                counter += 1;

                search(local_board, 1, -eval_mate_upper, eval_mate_upper);

                Node pv_entry = tt_bucket[pv_board.hash_board() % (tt_size - 1)];

                if (pv_entry.coordinate.empty()) {
                    break;
                }

                pv_board = pv_board.make_move(pv_entry.coordinate);

                pv += ' ' + pv_entry.coordinate;
            }

            print_stats(to_string(v_depth), to_string(local_score), to_string(elapsed_time), to_string(v_nodes), to_string(v_nps), (best_move + pv));

            // print_stats(to_string(v_depth), to_string(local_score), to_string(elapsed_time), to_string(v_nodes), to_string(v_nps), best_move);

            v_depth++;

            if (get_time() >= end_time) {
                break;
            }
        }

        return best_move;
}

int Search::search(Board local_board, int v_depth, int alpha, int beta) {
    if (get_time() >= critical_time) {
        return -eval_mate_upper;
    }

    if (count(local_board.repetitions.begin(), local_board.repetitions.end(), local_board.board_string) > 2 || local_board.move_counter >= 100) {
        return 0;
    }

    if (v_depth <= 0) {
        return quiesce(local_board, alpha, beta);
    }

    bool is_white = local_board.played_move_count % 2 == 0;
    bool is_pv_node = beta > (alpha + 1);
    bool is_in_check = local_board.in_check(is_white);
    int original_alpha = alpha;

    ++v_nodes;

    Node tt_entry;

    uint64_t index = local_board.hash_board() % (tt_size - 1);

    tt_entry = tt_bucket[index];

    // if (tt_entry.coordinate.empty()) {
    //     tt_entry = Node{2 * eval_mate_upper, eval_upper, -1};
    // }

    if (tt_entry.depth >= v_depth && !tt_entry.coordinate.empty() && !is_pv_node) {
        if (tt_entry.flag == eval_exact ||
        (tt_entry.flag == eval_lower && tt_entry.score >= beta) ||
        (tt_entry.flag == eval_upper && tt_entry.score <= alpha)) {
            return tt_entry.score;
        }
    }

    if (!is_pv_node && !is_in_check && v_depth <= 7 && local_board.rolling_score >= beta + (100 * v_depth)) {
        return local_board.rolling_score;
    }

    // if not is_pv_node and not is_in_check and v_depth <= 2 and local_board.rolling_score <= alpha - (350 * v_depth):
    //     return local_board.rolling_score

    int local_score = -eval_mate_upper;

    if (!is_pv_node && !is_in_check && v_depth <= 5) {
        int cut_boundary = alpha - (385 * v_depth);
        if (local_board.rolling_score <= cut_boundary) {
            if (v_depth <= 2) {
                return quiesce(local_board, alpha, alpha + 1);
            }

            local_score = quiesce(local_board, cut_boundary, cut_boundary + 1);

            if (local_score <= cut_boundary) {
                return local_score;
            }
        }
    }

    local_score = -eval_mate_upper;
    int best_score = -eval_mate_upper - 1;

    string pieces = is_white ? "RNBQ" : "rnbq";

    if (!is_pv_node && !is_in_check && local_board.board_string.find(pieces[0]) < 10 && local_board.board_string.find(pieces[1]) < 10
            && local_board.board_string.find(pieces[2]) < 10 && local_board.board_string.find(pieces[3]) < 10) {

        local_score = -search(local_board.nullmove(), max(0, v_depth - 4), -beta, -beta+1);

        if (local_score >= beta) {
            return beta;
        }
    }

    if (!is_pv_node && !is_in_check && tt_entry.depth >= v_depth && abs(tt_entry.score) < eval_mate_upper && !tt_entry.coordinate.empty()) {
        local_score = -search(local_board.make_move(tt_entry.coordinate), v_depth - 1, -beta, -alpha);

        if (local_score >= beta) {
            return beta;
        }
    }

    Board moved_board;
    string best_move = "";
    bool is_quiet = false;
    int r_depth = 1;
    int played_moves = 0;

    vector<struct Move> moves = local_board.generate_valid_moves();

    for (int i = 0; i < moves.size(); i++) {
        moves[i].score = local_board.calculate_score(moves[i].coordinate, true);
    }

    sort(moves.begin(), moves.end(), struct_move);

    // Traditional AB
    // for (Move move : moves) {
    //     moved_board = local_board.make_move(move.coordinate);

    //     // determine legality: if we moved and are in check, it's not legal
    //     if (moved_board.in_check(is_white)) {
    //         continue;
    //     }

    //     played_moves += 1;

    //     local_score = -search(moved_board, v_depth - 1, -beta, -alpha);

    //     if (local_score >= beta) {
    //         return beta;
    //     }

    //     if (local_score > best_score) {
    //         best_score = local_score;
    //         best_move = move.coordinate;

    //         if (best_score > alpha) {
    //             alpha = best_score;
    //         }
    //     }
    // }

    for (Move move : moves) {
        moved_board = local_board.make_move(move.coordinate);

        // determine legality: if we moved and are in check, it's not legal
        if (moved_board.in_check(is_white)) {
            continue;
        }

        is_quiet = local_board.piece_count == moved_board.piece_count;

        played_moves += 1;

        r_depth = 1;
        if (!is_pv_node && is_quiet && v_depth > 2 && played_moves > 1) {
            r_depth = max(3, (int) ceil(sqrt(v_depth-1) + sqrt(played_moves-1)));
        }

        if (r_depth != 1) {
            local_score = -search(moved_board, v_depth - r_depth, -alpha-1, -alpha);
        }

        if ((r_depth != 1 && local_score > alpha) || (r_depth == 1 && (!is_pv_node || played_moves != 1))) {
            local_score = -search(moved_board, v_depth - 1, -alpha-1, -alpha);
        }

        if (is_pv_node && (played_moves == 1 || local_score > alpha)) {
            local_score = -search(moved_board, v_depth - 1, -beta, -alpha);
        }

        if (best_move.empty()) {
            best_move = move.coordinate;
        }

        if (local_score > best_score) {
            best_move = move.coordinate;
            best_score = local_score;

            if (local_score > alpha) {
                alpha = local_score;

                if (alpha >= beta) {
                    break;
                }
            }
        }
    }

    if (played_moves == 0) {
        return is_in_check ? -eval_mate_upper + local_board.played_move_count : 0;
    }

    // update TT only if we are not in time cut
    if (get_time() < critical_time) {
        tt_entry.score = best_score;
        tt_entry.coordinate = best_move;
        tt_entry.depth = v_depth;
        tt_entry.flag = (best_score >= beta) ? eval_lower : (best_score > original_alpha) ? eval_exact : eval_upper;

        tt_bucket[index] = tt_entry;
    } else {
        Node empty;
        tt_entry = empty;
    }

    return best_score;
}

int Search::quiesce(Board local_board, int alpha, int beta) {
    if (get_time() >= critical_time) {
        return -eval_mate_upper;
    }

    if (count(local_board.repetitions.begin(), local_board.repetitions.end(), local_board.board_string) > 2 || local_board.move_counter >= 100) {
        return 0;
    }

    Node tt_entry = tt_bucket[local_board.hash_board() % (tt_size - 1)];

    if (!tt_entry.coordinate.empty()) {
        if (tt_entry.flag == eval_exact ||
        (tt_entry.flag == eval_lower && tt_entry.score >= beta) ||
        (tt_entry.flag == eval_upper && tt_entry.score <= alpha)) {
            return tt_entry.score;
        }
    }

    int local_score = local_board.rolling_score;

    if (local_score >= beta) {
        return beta;
    }

    alpha = max(alpha, local_score);

    vector<struct Move> moves = local_board.generate_valid_moves(true);

    for (int i = 0; i < moves.size(); i++) {
        moves[i].score = local_board.calculate_score(moves[i].coordinate, true);
    }

    sort(moves.begin(), moves.end(), struct_move);

    Board moved_board;

    int played_moves = 0;

    for (Move move : moves) {
        moved_board = local_board.make_move(move.coordinate);

        // determine legality: if we moved and are in check, it's not legal
        if (moved_board.in_check(local_board.played_move_count % 2 == 0)) {
            continue;
        }

        // only count the node if we have a move to play
        if (played_moves == 0) {
            ++v_nodes;
        }

        ++played_moves;

        local_score = -quiesce(moved_board, -beta, -alpha);

        if (local_score > alpha) {
            alpha = local_score;

            if (alpha >= beta) {
                return alpha;
            }
        }
    }

    return alpha;
}

int perft_captures = 0;
int perft_checks = 0;
int nodes = 0;

int run_perft(Board local_board, int original_depth, int v_depth) {
    if (v_depth == 0) {
        return 1;
    }

    Board moved_board;

    if (v_depth != original_depth) {
        int total = 0;

        vector<struct Move> moves = local_board.generate_valid_moves();

        for (Move move : moves) {
            moved_board = local_board.make_move(move.coordinate);

            if (moved_board.in_check(local_board.played_move_count % 2 == 0)) {
                continue;
            }

            if (local_board.piece_count != moved_board.piece_count) {
                perft_captures += 1;
            }

            if (moved_board.in_check(local_board.played_move_count % 2 != 0)) {
                perft_checks += 1;
            }

            total += run_perft(moved_board, original_depth, v_depth-1);
        }
        return total;
    }

    vector<struct Move> moves = local_board.generate_valid_moves();

    for (Move move : moves) {
        moved_board = local_board.make_move(move.coordinate);

        if (moved_board.in_check(local_board.played_move_count % 2 == 0)) {
            continue;
        }

        if (local_board.piece_count != moved_board.piece_count) {
            perft_captures += 1;
        }

        if (moved_board.in_check(local_board.played_move_count % 2 != 0)) {
            perft_checks += 1;
        }

        int x = run_perft(moved_board, original_depth, v_depth-1);
        cout << move.coordinate << ": " << x <<endl;
        nodes += x;
    }

    cout << "Nodes searched: " << nodes << endl;
    cout << "Captures: " << perft_captures << " Checks: " << perft_checks << endl;

    return 0;
}

int main() {
    for (int i = 0; i < PIECES.length(); i++) {
        for (int j = 21; j < 99; j++) {
            if (j % 10 == 0 || j % 10 == 9) {
                continue;
            }
            ALLPSQT[PIECES[i]][j] += PIECEPOINTS[PIECES[i]];
        }
    }

    init_table();

    Board game_board;
    Search searcher;
    searcher.reset();

    string line;

    while (1) {
        getline(cin, line);

        if (line == "quit") {
            abort();
        } else if (line == "uci") {
            cout << "pygone 1.6.0\nuciok\n";
        } else if (line == "ucinewgame") {
            game_board = Board();
            searcher.reset();
        } else if (line == "isready") {
            cout << "readyok\n";
        } else if (line.rfind("position", 0) == 0) {
            game_board = Board();
            if (line == "position startpos") {
                continue;
            }
            string moves = line.erase(0, 24) + " ";

            string move = "";

            for(int i = 0; i < moves.length(); i++) {
                if (moves[i] != ' ') {
                    move += moves[i];
                } else {
                    game_board = game_board.make_move(move);
                    move = "";
                }
            }
        } else if (line.rfind("go perft", 0) == 0) {
            int depth = stoi(line.erase(0, 9));

            uint64_t start_time = get_time();
            run_perft(game_board, depth, depth);
            cout << "total time: " << (get_time() - start_time) << endl;
        } else if (line.rfind("go depth", 0) == 0) {
            int depth = stoi(line.erase(0, 9));

            searcher.end_time = searcher.critical_time = get_time() + 10000000000;

            string best_move;

            best_move = searcher.iterative_search(game_board, depth);

            cout << "bestmove " << best_move << endl;
        } else if (line.rfind("go nodes", 0) == 0) {

        } else if (line.rfind("go", 0) == 0) {
            bool is_white = game_board.played_move_count % 2 == 0;

            // make sure to have space at end of line so we can process all time properly
            line += ' ';

            string last_word;
            string current_word;

            int move_time = 0;

            for (int i = 0; i < line.length(); i++) {
                if (line[i] != ' ') {
                    current_word += line[i];
                } else {
                    if (!last_word.empty()) {
                        if ((last_word == "wtime" && is_white) || (last_word == "btime" && !is_white)) {
                            move_time = stoi(current_word);
                        }
                    }

                    last_word = current_word;
                    current_word.clear();
                }
            }

            searcher.end_time = get_time() + max(2200, move_time / 32);
            searcher.critical_time = min(searcher.end_time + 5000, get_time() + move_time - 1500);

            searcher.v_nodes = 0;

            string best_move;

            best_move = searcher.iterative_search(game_board, 100);

            cout << "bestmove " << best_move << endl;

        }
    }
}