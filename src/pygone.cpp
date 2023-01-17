#include <algorithm>
#include <cmath>
#include <cstring>
#include <cctype>
#include <ctime>
#include <chrono>
#include <iostream>
#include <functional>
#include <limits>
#include <map>
#include <mutex>
#include <random>
#include <string>
#include <thread>
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
mt19937_64 gen(rd());
uniform_int_distribution<uint64_t> dis;

uint64_t random_uint64()
{
    return dis(gen);
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

int ALLPSQT[8][8][6];

int P_PSQT[8][8] = {
        {0,0,0,0,0,0,0,0},
        {30,30,30,30,30,30,30,30},
        {8,8,17,26,26,17,8,8},
        {5, 5,8,24,24,8, 5, 5},
        {0, 0, 0,24,24, 0, 0, 0},
        {5,-5,-8, 6, 6,-8,-5, 5},
        {5,8,8,-22,-22,8,8, 5},
        {0, 0, 0, 0, 0, 0, 0, 0}};

int N_PSQT[8][8] = {
        {-50,-40,-30,-30,-30,-30,-40,-50},
        {-40,-20, 0, 0, 0, 0,-20,-40},
        {-30, 0,8,13,13,8, 0,-30},
        {-30, 5,13,18,18,13, 5,-30},
        {-30, 0,13,18,18,13, 0,-30},
        {-30, 5,7,13,13,7, 5,-30},
        {-40,-20, 0, 5, 5, 0,-20,-40},
        {-50,-40,-20,-30,-30,-20,-40,-50}};
int B_PSQT[8][8] = {
        {-20,-10,-10,-10,-10,-10,-10,-20},
        {-10, 0, 0, 0, 0, 0, 0,-10},
        {-10, 0, 5,10,10, 5, 0,-10},
        {-10, 5, 5,10,10, 5, 5,-10},
        {-10, 0,10,10,10,10, 0,-10},
        {-10,10,10,10,10,10,10,-10},
        {-10, 5, 0, 0, 0, 0, 5,-10},
        {-20,-10,-40,-10,-10,-40,-10,-20}};
int R_PSQT[8][8] = {
        {10,20,20,20,20,20,20, 10},
        {-10, 0, 0, 0, 0, 0, 0,-10},
        {-10, 0, 0, 0, 0, 0, 0,-10},
        {-10, 0, 0, 0, 0, 0, 0,-10},
        {-10, 0, 0, 0, 0, 0, 0,-10},
        {-10, 0, 0, 0, 0, 0, 0,-10},
        {-10, 0, 0, 0, 0, 0, 0,-10},
        {-10, 0, 0,10,10, 10, 0,-10}};
int Q_PSQT[8][8] = {
        {-40,-20,-20,-10,-10,-20,-20,-40},
        {-20, 0, 0, 0, 0, 0, 0,-20},
        {-20, 0,10,10,10,10, 0,-20},
        {-10, 0,10,10,10,10, 0,-10},
        {0, 0,10,10,10,10, 0,-10},
        {-20,10,10,10,10,10, 0,-20},
        {-20, 0,10, 0, 0, 0, 0,-20},
        {-40,-20,-20,-10,-10,-20,-20,-40}};
int K_PSQT[8][8] = {
        {-50,-40,-30,-20,-20,-30,-40,-50},
        {-30,-20,-10, 0, 0,-10,-20,-30},
        {-30,-10,20,30,30,20,-10,-30},
        {-30,-10,30,40,40,30,-10,-30},
        {-30,-10,30,40,40,30,-10,-30},
        {-10,-20,-20,-20,-20,-20,-20,-10},
        {20,20,0,0,0,0,20,20},
        {20,20,35,0,0,10,35,20}};

void init_psqt_table()
{
    for (int i = 0; i<8; i++) {
        for (int j = 0; j<8; j++) {
            for (int k = 0; k<6; k++) {
                switch (k) {
                    case 0:
                        ALLPSQT[i][j][k] = P_PSQT[i][j] + PIECEPOINTS['p'];
                        break;
                    case 1:
                        ALLPSQT[i][j][k] = N_PSQT[i][j] + PIECEPOINTS['n'];
                        break;
                    case 2:
                        ALLPSQT[i][j][k] = B_PSQT[i][j] + PIECEPOINTS['b'];
                        break;
                    case 3:
                        ALLPSQT[i][j][k] = R_PSQT[i][j] + PIECEPOINTS['r'];
                        break;
                    case 4:
                        ALLPSQT[i][j][k] = Q_PSQT[i][j] + PIECEPOINTS['q'];
                        break;
                    case 5:
                        ALLPSQT[i][j][k] = K_PSQT[i][j] + PIECEPOINTS['k'];
                        break;
                }
            }
        }
    }
}

vector<array<int, 2>> get_moves(char piece) {
    vector<array<int, 2>> moves;

    if (piece == 'k') {
        moves = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}, {1, 1}, {1, -1}, {-1, 1}, {-1, -1}};
    } else if (piece == 'q') {
        moves = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}, {1, 1}, {1, -1}, {-1, 1}, {-1, -1}};
    } else if (piece == 'r') {
        moves = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
    } else if (piece == 'b') {
        moves = {{1, 1}, {1, -1}, {-1, 1}, {-1, -1}};
    } else if (piece == 'n') {
        moves = {{1, -2}, {-1, -2}, {2, -1}, {-2, -1}, {1, 2}, {-1, 2}, {2, 1}, {-2, 1}};
    } else {
        moves = {{1, 0}};
    }

    return moves;
}

void print_stats(string v_depth, string v_score, string v_time, string v_nodes, string v_nps, string v_pv) {
    cout << "info depth " << v_depth << " score cp " << v_score << " time " << v_time << " nodes " << v_nodes << " nps " << v_nps << " pv " << v_pv << endl;
}

string get_coordinate(int row, int column)
{
    char col = 97 + column;

    return col + to_string(abs(8 - row));
}

uint64_t get_time() {
    return chrono::duration_cast<chrono::milliseconds>(chrono::system_clock::now().time_since_epoch()).count();
}

struct [[nodiscard]] Move {
    int score;
    string coordinate;

    bool operator() (Move i,Move j) { return (i.score > j.score); };
} struct_move;

class Board {
public:
    char board_state[8][8] = {
        {'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'},
        {'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'},
        {'-', '-', '-', '-', '-', '-', '-', '-'},
        {'-', '-', '-', '-', '-', '-', '-', '-'},
        {'-', '-', '-', '-', '-', '-', '-', '-'},
        {'-', '-', '-', '-', '-', '-', '-', '-'},
        {'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'},
        {'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'}};
    string board_string = "rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR1";
    int played_move_count = 0;
    vector<string> repetitions = {};
    string black_king_position = "e8";
    string white_king_position = "e1";
    bool white_castling[2] = {true, true};
    bool black_castling[2] = {true, true};
    int piece_count = 32;
    string en_passant;
    int move_counter = 0;

    void print_board();

    Board board_copy();
    Board make_move(string uci_coordinate);
    void set_string();
    Board nullmove();
    int get_piece_count();
    // bool check_is_endgame();
    int calculate_score();
    bool passer_pawn(int board_position);
    bool stacked_pawn(int board_position);
    int rook_score(int board_position);
    string str_board();
    uint64_t hash_board();
    vector<struct Move> generate_valid_moves(bool captures_only=false);
    bool in_check(bool is_white);
    bool attack_position(bool is_white, string coordinate);
};

void Board::print_board() {
    for (int i = 0; i < 64; i += 8) {
        cout << board_string.substr(i, 8) << endl;
    }
    cout << "Score: " << calculate_score() << " In Check: " << in_check(played_move_count % 2 == 0) << endl;
}

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
    board.repetitions = repetitions;

    memcpy(board.board_state, board_state, 64);
    memcpy(board.white_castling, white_castling, 2);
    memcpy(board.black_castling, black_castling, 2);

    return board;
}

Board Board::make_move(string uci_coordinate) {
    // making the move will return an altered copy of the current state
    // this allows us to avoid "undoing" the move
    Board board = board_copy();

    string from = uci_coordinate.substr(0, 2);
    string to = uci_coordinate.substr(2, 2);
    char promote = '-';
    if (uci_coordinate.length() == 5) {
        promote = uci_coordinate[4];
    }

    int from_row = abs(8 - (from[1] - '0'));
    int from_column = from[0] - 97;

    int to_row = abs(8 - (to[1] - '0'));
    int to_column = to[0] - 97;

    char from_piece = board.board_state[from_row][from_column];
    char from_piece_lower = tolower(from_piece);

    if (from_piece_lower == 'p' || from_piece != '-') {
        board.move_counter = 0;
    } else {
        ++board.move_counter;
    }

    // castling
    if (from_piece_lower == 'k' && abs(from_column - to_column) > 1) {
        if (from_column > to_column) {
            // queen side
            board.board_state[to_row][to_column + 1] = board.board_state[to_row][to_column - 2];
            board.board_state[to_row][to_column - 2] = '-';
        } else {
            // king side
            board.board_state[to_row][to_column - 1] = board.board_state[to_row][to_column + 1];
            board.board_state[to_row][to_column + 1] = '-';
        }
    }

    // set castling
    if (from_piece_lower == 'k') {
        if (from == "e1") {
            board.white_castling[0] = false;
            board.white_castling[1] = false;
        } else if (from == "e8") {
            board.black_castling[0] = false;
            board.black_castling[1] = false;
        }

        if (from_piece == 'K') {
            board.white_king_position = to;
        } else {
            board.black_king_position = to;
        }
    }

    // set castling
    if (from_piece_lower == 'r') {
        if (from == "a1") {
            board.white_castling[0] = false;
        } else if (from == "a8") {
            board.black_castling[0] = false;
        }
    }
    if (from_piece_lower == 'r') {
        if (from == "h1") {
            board.white_castling[1] = false;
        } else if (from == "h8") {
            board.black_castling[1] = false;
        }
    }

    // en passant
    if (from_piece_lower == 'p' && to == board.en_passant) {
        board.board_state[from_row][to_column] = '-';
    }

    if (from_piece_lower == 'p' && abs(to_row - from_row) == 2) {
        board.en_passant = get_coordinate(from_row + ((to_row - from_row) / 2) , from_column);
    } else {
        board.en_passant = "";
    }

    board.board_state[to_row][to_column] = board.board_state[from_row][from_column];
    board.board_state[from_row][from_column] = '-';

    if (promote != '-') {
        if (toupper(board.board_state[to_row][to_column]) == board.board_state[to_row][to_column]) {
            board.board_state[to_row][to_column] = toupper(promote);
        } else {
            board.board_state[to_row][to_column] = promote;
        }
    }

    board.played_move_count += 1;

    board.set_string();

    board.piece_count = board.get_piece_count();

    board.repetitions.push_back(board.board_string);

    return board;
}

void Board::set_string() {
    board_string = "";
    for (int row = 0; row < 8; row += 1) {
        for (int column = 0; column < 8; column += 1) {
            board_string += board_state[row][column];
        }
    }
    board_string += to_string(played_move_count % 2);
}

Board Board::nullmove() {
    // allows for a quick way to let other side move
    // making the move will return an altered copy of the current state
    // this allows us to avoid "undoing" the move
    Board board = board_copy();
    board.played_move_count += 1;

    return board;
}

int Board::get_piece_count() {
    int piece_count = 0;
    for (int row = 0; row < 8; row += 1) {
        for (int column = 0; column < 8; column += 1) {
            if (board_state[row][column] != '-') {
                ++piece_count;
            }
        }
    }
    return piece_count;
}

// bool Board::check_is_endgame() {
//     return piece_count < 14;
// }

int Board::calculate_score() {
    bool is_white = played_move_count % 2 == 0;
    int score = 0;
    for (int row = 0; row < 8; row += 1) {
        for (int column = 0; column < 8; column += 1) {
            if (board_state[row][column] != '-') {
                int piece = index_of(toupper(board_state[row][column]));

                int to_row = row;

                if (islower(board_state[row][column])) {
                    to_row = abs(7 - row);
                }

                if (is_white == (bool) isupper(board_state[row][column])) {
                    score += ALLPSQT[to_row][column][piece];
                } else {
                    score -= ALLPSQT[to_row][column][piece];
                }
            }
        }
    }

    return score;
}

bool Board::passer_pawn(int board_position) {
    // bool is_white = played_move_count % 2 == 0;
    // int p_offset = is_white ? -10 : 10;
    // int start_position = board_position + p_offset;

    // int piece_count = 1;
    // while (start_position >= 20 && start_position <= 100) {
    //     if (board_state[start_position] != '.' && board_state[start_position] != '-') {
    //         return false;
    //     }
    //     start_position += p_offset;
    // }

    return true;
}

bool Board::stacked_pawn(int board_position) {
//     bool is_white = played_move_count % 2 == 0;
//     int p_offset = is_white ? -10 : 10;
//     char p_piece = is_white ? 'P' : 'p';

//     int start_position = board_position + p_offset;

//     while (start_position >= 20 && start_position <= 100) {
//         if (board_state[start_position] == p_piece) {
//             return true;
//         }
//         start_position += p_offset;
//     }

    return false;
}

int Board::rook_score(int board_position) {
    return 0;
}

string Board::str_board() {
    return board_string;
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

    for (int row = 0; row < 8; row += 1) {
        for (int column = 0; column < 8; column += 1) {
            if (board_state[row][column] != '-') {
                int piece = index_of(board_state[row][column]);

                h ^= ZobristTable[column][row][piece];
            }
        }
    }

    return h;
}

vector<struct Move> Board::generate_valid_moves(bool captures_only) {
    // Return list of valid (maybe illegal) moves

    vector<struct Move> valid_moves;

    bool is_white = played_move_count % 2 == 0;

    char piece;
    char piece_lower;

    int to_row;
    int to_column;

    Move move;
    Move promotion_move;

    for (int row = 0; row < 8; row++) {
        for (int column = 0; column < 8; column++) {
            piece = board_state[row][column];
            piece_lower = tolower(piece);

            if (piece == '-' || is_white == (piece == piece_lower)) {
                continue;
            }

            if (piece_lower == 'p') {
                // check for double pawn moves
                if (piece == 'p' && row == 1) {
                    if (board_state[row + 1][column] == '-' && board_state[row + 2][column] == '-') {
                        move.coordinate = get_coordinate(row, column) + get_coordinate(row + 2, column);
                        valid_moves.push_back(move);
                    }
                }

                if (piece == 'P' && row == 6) {
                    if (board_state[row - 1][column] == '-' && board_state[row - 2][column] == '-') {
                        move.coordinate = get_coordinate(row, column) + get_coordinate(row - 2, column);
                        valid_moves.push_back(move);
                    }
                }

                // check for diagonal capture
                to_row = is_white ? row - 1 : row + 1;

                if (column > 0 && board_state[to_row][column - 1] != '-' && (bool) isupper(piece) != (bool) isupper(board_state[to_row][column - 1])) {
                    move.coordinate = get_coordinate(row, column) + get_coordinate(to_row, column - 1);
                    if (to_row == 0 || to_row == 7) {
                        promotion_move.coordinate = move.coordinate + 'q';
                        valid_moves.push_back(promotion_move);
                        promotion_move.coordinate = move.coordinate + 'r';
                        valid_moves.push_back(promotion_move);
                        promotion_move.coordinate = move.coordinate + 'b';
                        valid_moves.push_back(promotion_move);
                        promotion_move.coordinate = move.coordinate + 'n';
                        valid_moves.push_back(promotion_move);
                    } else {
                        valid_moves.push_back(move);
                    }
                }

                if (column < 7 && board_state[to_row][column + 1] != '-' && (bool) isupper(piece) != (bool) isupper(board_state[to_row][column + 1])) {
                    move.coordinate = get_coordinate(row, column) + get_coordinate(to_row, column + 1);
                    if (to_row == 0 || to_row == 7) {
                        promotion_move.coordinate = move.coordinate + 'q';
                        valid_moves.push_back(promotion_move);
                        promotion_move.coordinate = move.coordinate + 'r';
                        valid_moves.push_back(promotion_move);
                        promotion_move.coordinate = move.coordinate + 'b';
                        valid_moves.push_back(promotion_move);
                        promotion_move.coordinate = move.coordinate + 'n';
                        valid_moves.push_back(promotion_move);
                    } else {
                        valid_moves.push_back(move);
                    }
                }

                // check for en-passant
                if (en_passant == get_coordinate(to_row, column - 1)) {
                    move.coordinate = get_coordinate(row, column) + get_coordinate(to_row, column - 1);
                    valid_moves.push_back(move);
                } else if (en_passant == get_coordinate(to_row, column + 1)) {
                    move.coordinate = get_coordinate(row, column) + get_coordinate(to_row, column + 1);
                    valid_moves.push_back(move);
                }
            }

            // check for castling
            if (piece_lower == 'k') {
                if (is_white && white_castling[1] || !is_white && black_castling[1]) {
                    if (board_state[row][column + 1] == '-' && board_state[row][column + 2] == '-' && tolower(board_state[row][column + 3]) == 'r') {
                        // make sure our K won't pass through attack on castle
                        if (!attack_position(is_white, get_coordinate(row, column)) && !attack_position(is_white, get_coordinate(row, column + 1)) && !attack_position(is_white, get_coordinate(row, column + 2))) {
                            move.coordinate = get_coordinate(row, column) + get_coordinate(row, column + 2);
                            valid_moves.push_back(move);
                        }
                    }
                }
                if (is_white && white_castling[0] || !is_white && black_castling[0]) {
                    if (board_state[row][column - 1] == '-' && board_state[row][column - 2] == '-' && board_state[row][column - 3] == '-' && tolower(board_state[row][column - 4]) == 'r') {
                        // make sure our K won't pass through attack on castle
                        if (!attack_position(is_white, get_coordinate(row, column)) && !attack_position(is_white, get_coordinate(row, column - 1)) && !attack_position(is_white, get_coordinate(row, column - 2))) {
                            move.coordinate = get_coordinate(row, column) + get_coordinate(row, column - 2);
                            valid_moves.push_back(move);
                        }
                    }
                }
            }

            vector<array<int, 2>> piece_moves = get_moves(piece_lower);

            for(array<int, 2> piece_move : piece_moves) {
                to_row = row;
                to_column = column;
                while (true) {
                    if (is_white) {
                        to_row -= piece_move[0];
                    } else {
                        to_row += piece_move[0];
                    }
                    to_column += piece_move[1];

                    if (to_row >= 0 && to_row < 8 && to_column >= 0 && to_column < 8) {

                        move.coordinate = get_coordinate(row, column) + get_coordinate(to_row, to_column);

                        if (piece_lower == 'p') {
                            if (board_state[to_row][to_column] == '-') {
                                if  (to_row == 0 || to_row == 7) {
                                    promotion_move.coordinate = move.coordinate + 'q';
                                    valid_moves.push_back(promotion_move);
                                    promotion_move.coordinate = move.coordinate + 'r';
                                    valid_moves.push_back(promotion_move);
                                    promotion_move.coordinate = move.coordinate + 'b';
                                    valid_moves.push_back(promotion_move);
                                    promotion_move.coordinate = move.coordinate + 'n';
                                    valid_moves.push_back(promotion_move);
                                } else {
                                    valid_moves.push_back(move);
                                }
                            }
                        } else {
                            if (board_state[to_row][to_column] == '-' || (bool) isupper(piece) != (bool) isupper(board_state[to_row][to_column])) {
                                valid_moves.push_back(move);
                            }
                        }
                    }

                    if (board_state[to_row][to_column] != '-' || piece_lower == 'p' || piece_lower == 'n' || piece_lower == 'k') {
                        break;
                    }
                }
            }
        }
    }
    return valid_moves;
}

bool Board::in_check( bool is_white) {
    string king_position = is_white ? white_king_position : black_king_position;

    return attack_position(is_white, king_position);
}

bool Board::attack_position(bool is_white, string coordinate) {
    char piece = 'p';
    char piece_lower = 'p';

    int attack_row = abs(8 - (coordinate[1] - '0'));
    int attack_column = coordinate[0] - 97;

    int to_row = 0;
    int to_column = 0;

    for (int row = 0; row < 8; row++) {
        for (int column = 0; column < 8; column++) {
            piece = board_state[row][column];
            piece_lower = tolower(piece);

            if (piece == '-' || is_white == (bool) isupper(piece)) {
                continue;
            }

            vector<array<int, 2>> piece_moves = get_moves(piece_lower);

            for(array<int, 2> piece_move : piece_moves) {
                to_row = row;
                to_column = column;
                while (true) {
                    if (piece == 'P') {
                        to_row -= piece_move[0];
                    } else {
                        to_row += piece_move[0];
                    }
                    to_column += piece_move[1];

                    if (to_row)

                    if (to_row >= 0 && to_row < 8 && to_column >= 0 && to_column < 8) {
                        if (piece_lower == 'p') {
                            if (column > 0 && get_coordinate(to_row, column - 1) == coordinate) {
                                return true;
                            }
                            if (column < 7 && get_coordinate(to_row, column + 1) == coordinate) {
                                return true;
                            }
                        } else {
                            if ((board_state[to_row][to_column] == '-' || (bool) isupper(piece) != (bool) isupper(board_state[to_row][to_column]))) {
                                if (get_coordinate(to_row, to_column) == coordinate) {
                                    return true;
                                }
                            }
                        }
                    }

                    if (board_state[to_row][to_column] != '-' || piece_lower == 'p' || piece_lower == 'n' || piece_lower == 'k') {
                        break;
                    }
                }
            }
        }
    }

    return false;
}

struct [[nodiscard]] Node {
    uint64_t key;
    int depth;
    int score;
    int flag;
    string coordinate;
};

auto tt_size = 64ULL << 18;
vector<Node> tt_bucket;
mutex tt_lock;

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
    string iterative_search(Board local_board, int depth, int thread_id, int &stop);
    int search(Board local_board, int v_depth, int alpha, int beta, int thread_id);
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

string Search::iterative_search(Board local_board, int depth, int thread_id, int &stop) {
        uint64_t start_time = get_time();

        int best_score = -eval_mate_upper;
        int local_score = 0;//local_board.calculate_score();

        string best_move;
        uint64_t elapsed_time;
        int v_nps;

        int v_depth = 1;

        // Node tt_entry;

        while (v_depth <= depth) {
            auto window = 40;
            auto research = 0;

            research:
            local_score = search(local_board, v_depth, local_score - window, local_score + window, thread_id);
            // local_score = search(local_board, v_depth, -eval_mate_upper, eval_mate_upper, thread_id);

            if (get_time() < critical_time) {
                const uint64_t tt_key = local_board.hash_board();

                Node tt_entry = tt_bucket[(tt_key % tt_size)];
                if (!tt_entry.coordinate.empty() && tt_entry.key == tt_key) {
                    best_move = tt_entry.coordinate;
                }
            } else {
                break;
            }

            if (thread_id == 0) {
                elapsed_time = get_time() - start_time;

                v_nps = (elapsed_time > 1000) ? ceil(v_nodes / (elapsed_time / 1000)) : v_nodes;

                string pv = "";
                if (v_depth > 1) {
                    int counter = 1;
                    Board pv_board = local_board.make_move(best_move);

                    while (counter < min(12, v_depth)) {
                        counter += 1;

                        const uint64_t tt_key = pv_board.hash_board();

                        Node pv_entry = tt_bucket[(tt_key % tt_size)];

                        if (pv_entry.coordinate.empty() || pv_entry.key <= 0) {
                            break;
                        }
                        pv_board = pv_board.make_move(pv_entry.coordinate);

                        pv += ' ' + pv_entry.coordinate;
                    }
                }

                print_stats(to_string(v_depth), to_string(local_score), to_string(elapsed_time), to_string(v_nodes), to_string(v_nps), (best_move + pv));

                // print_stats(to_string(v_depth), to_string(local_score), to_string(elapsed_time), to_string(v_nodes), to_string(v_nps), best_move);
            }

            if (local_score >= best_score + window || local_score <= best_score - window) {
                window <<= ++research;
                best_score = local_score;
                goto research;
            }

            best_score = local_score;
            v_depth++;

            if (get_time() >= end_time || stop) {
                break;
            }
        }

        return best_move;
}

int Search::search(Board local_board, int v_depth, int alpha, int beta, int thread_id) {
    if (get_time() >= critical_time) {
        return -eval_mate_upper;
    }

    if (count(local_board.repetitions.begin(), local_board.repetitions.end(), local_board.board_string) > 2 || local_board.move_counter >= 100) {
        return 0;
    }

    if (v_depth <= 0) {
        return quiesce(local_board, alpha, beta);
    }

    Board nullboard = local_board.nullmove();

    bool is_white = local_board.played_move_count % 2 == 0;
    // bool is_pv_node = beta > (alpha + 1);
    bool is_in_check = local_board.in_check(is_white);
    int original_alpha = alpha;

    ++v_nodes;

    const uint64_t tt_key = local_board.hash_board();

    Node tt_entry;
    tt_entry = tt_bucket[(tt_key % tt_size)];

    if (tt_entry.key == tt_key && tt_entry.depth >= v_depth && !tt_entry.coordinate.empty()) { // && !is_pv_node) {
        if (tt_entry.flag == eval_exact ||
        (tt_entry.flag == eval_lower && tt_entry.score >= beta) ||
        (tt_entry.flag == eval_upper && tt_entry.score <= alpha)) {
            return tt_entry.score;
        }
    }

    // if (!is_pv_node && !is_in_check && v_depth <= 7 && local_board.calculate_score() >= beta + (100 * v_depth)) {
    //     return local_board.calculate_score();
    // }

    // if (!is_pv_node && !is_in_check && v_depth <= 2 && local_board.calculate_score() <= alpha - (350 * v_depth)) {
    //     return local_board.calculate_score();
    // }

    int local_score = -eval_mate_upper;

    // if (!is_pv_node && !is_in_check && v_depth <= 5) {
    //     int cut_boundary = alpha - (385 * v_depth);
    //     if (local_board.calculate_score() <= cut_boundary) {
    //         if (v_depth <= 2) {
    //             return quiesce(local_board, alpha, alpha + 1);
    //         }

    //         local_score = quiesce(local_board, cut_boundary, cut_boundary + 1);

    //         if (local_score <= cut_boundary) {
    //             return local_score;
    //         }
    //     }
    // }

    // local_score = -eval_mate_upper;
    int best_score = -eval_mate_upper - 1;

    // string pieces = is_white ? "RNBQ" : "rnbq";

    // if (!is_pv_node && !is_in_check && local_board.board_string.find(pieces[0]) < 10 && local_board.board_string.find(pieces[1]) < 10
    //         && local_board.board_string.find(pieces[2]) < 10 && local_board.board_string.find(pieces[3]) < 10) {

    //     local_score = -search(nullboard, max(0, v_depth - 4), -beta, -beta+1, 0);

    //     if (local_score >= beta) {
    //         return beta;
    //     }
    // }

    // if (!is_pv_node && !is_in_check && tt_entry.key == tt_key && tt_entry.depth >= v_depth && abs(tt_entry.score) < eval_mate_upper && !tt_entry.coordinate.empty()) {
    if (tt_entry.key == tt_key) {
        local_score = -search(local_board.make_move(tt_entry.coordinate), v_depth - 1, -beta, -alpha, 0);

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
        moved_board = local_board.make_move(moves[i].coordinate);
        moves[i].score = -moved_board.calculate_score();
        if (thread_id > 0) {
            moves[i].score += (rand() % 10);
        }
    }

    sort(moves.begin(), moves.end(), struct_move);

    // for (Move move : moves) {
    //     cout << v_depth << " " << move.coordinate << " " <<   move.score << endl;
    // }

    // Traditional AB
    for (Move move : moves) {
        if (tt_entry.key == tt_key && tt_entry.coordinate == move.coordinate) {
            continue;
        }

        moved_board = local_board.make_move(move.coordinate);

        // determine legality: if we moved and are in check, it's not legal
        if (moved_board.in_check(is_white)) {
            continue;
        }

        played_moves += 1;

        local_score = -search(moved_board, v_depth - 1, -beta, -alpha, 0);

        if (local_score >= beta) {
            return beta;
        }

        if (local_score > best_score) {
            best_score = local_score;
            best_move = move.coordinate;

            if (best_score > alpha) {
                alpha = best_score;
            }
        }
    }

    // for (Move move : moves) {
    //     moved_board = local_board.make_move(move.coordinate);
    //     // cout << move.coordinate << " " << moved_board.calculate_score() << endl;

    //     // determine legality: if we moved and are in check, it's not legal
    //     if (moved_board.in_check(is_white)) {
    //         continue;
    //     }

    //     is_quiet = local_board.piece_count == moved_board.piece_count;

    //     played_moves += 1;

    //     r_depth = 1;
    //     if (!is_pv_node && is_quiet && v_depth > 2 && played_moves > 1) {
    //         r_depth = max(3, (int) ceil(sqrt(v_depth-1) + sqrt(played_moves-1)));
    //     }

    //     if (r_depth != 1) {
    //         local_score = -search(moved_board, v_depth - r_depth, -alpha-1, -alpha, 0);
    //     }

    //     if ((r_depth != 1 && local_score > alpha) || (r_depth == 1 && (!is_pv_node || played_moves != 1))) {
    //         local_score = -search(moved_board, v_depth - 1, -alpha-1, -alpha, 0);
    //     }

    //     if (is_pv_node && (played_moves == 1 || local_score > alpha)) {
    //         local_score = -search(moved_board, v_depth - 1, -beta, -alpha, 0);
    //     }

    //     if (best_move.empty()) {
    //         best_move = move.coordinate;
    //     }

    //     if (local_score > best_score) {
    //         best_move = move.coordinate;
    //         best_score = local_score;

    //         if (local_score > alpha) {
    //             alpha = local_score;

    //             if (alpha >= beta) {
    //                 break;
    //             }
    //         }
    //     }
    // }

    if (played_moves == 0) {
        return is_in_check ? -eval_mate_upper - local_board.played_move_count : 0;
    }

    // update TT only if we are not in time cut
    if (get_time() < critical_time) {
        if (v_depth >= tt_entry.depth || tt_entry.key != tt_key) {
            tt_entry.key = tt_key;
            tt_entry.score = best_score;
            tt_entry.coordinate = best_move;
            tt_entry.depth = v_depth;
            tt_entry.flag = (best_score >= beta) ? eval_lower : (best_score > original_alpha) ? eval_exact : eval_upper;

            tt_lock.lock();
            tt_bucket[(tt_key % tt_size)] = tt_entry;
            tt_lock.unlock();
        }
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

    const uint64_t tt_key = local_board.hash_board();

    Node tt_entry;
    tt_entry = tt_bucket[(tt_key % tt_size)];

    if (!tt_entry.coordinate.empty() && tt_entry.key == tt_key) {
        if (tt_entry.flag == eval_exact ||
        (tt_entry.flag == eval_lower && tt_entry.score >= beta) ||
        (tt_entry.flag == eval_upper && tt_entry.score <= alpha)) {
            return tt_entry.score;
        }
    }

    int local_score = local_board.calculate_score();

    if (local_score >= beta) {
        return beta;
    }

    alpha = max(alpha, local_score);

    Board moved_board;
    vector<struct Move> moves = local_board.generate_valid_moves();

    for (int i = 0; i < moves.size(); i++) {
        moved_board = local_board.make_move(moves[i].coordinate);
        moves[i].score = -moved_board.calculate_score();
    }

    sort(moves.begin(), moves.end(), struct_move);

    int played_moves = 0;

    for (Move move : moves) {
        moved_board = local_board.make_move(move.coordinate);

        // determine legality: if we moved and are in check, it's not legal
        if (local_board.piece_count == moved_board.piece_count || moved_board.in_check(local_board.played_move_count % 2 == 0)) {
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
    Board nullboard;

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
    init_psqt_table();
    init_table();

    Board game_board;

    // game_board = game_board.make_move("e2e4");

    // vector<struct Move> moves = game_board.generate_valid_moves();

    // for (Move move: moves) {
    //     cout << move.coordinate << endl;
    // }

    Search searcher;
    searcher.reset();

    string line;

    int depth = 40;
    int thread_count = 1;
    bool should_search = false;

    while (1) {
        getline(cin, line);

        should_search = false;

        if (line == "quit") {
            abort();
        } else if (line == "uci") {
            cout << "pygone 1.6.0\nuciok\n";
        } else if (line == "ucinewgame") {
            game_board = Board();
            searcher.reset();
        } else if (line == "isready") {
            cout << "readyok\n";
        } else if (line == "print") {
            game_board.print_board();
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
            perft_captures = 0;
            perft_checks = 0;
            nodes = 0;
            run_perft(game_board, depth, depth);
            cout << "total time: " << (get_time() - start_time) << endl;
        } else if (line.rfind("go depth", 0) == 0) {
            depth = stoi(line.erase(0, 9));

            searcher.end_time = searcher.critical_time = get_time() + 10000000000;
            searcher.v_nodes = 0;

            should_search = true;
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

            should_search = true;
        }

        if (should_search) {
            string best_move;

            // Lazy SMP
            vector<thread> threads;
            vector<int> stops(thread_count, false);

            for (int i = 1; i < thread_count; ++i) {
                Search t_search;
                t_search.end_time = searcher.end_time;
                t_search.critical_time = searcher.critical_time;

                Board t_board = game_board.board_copy();


                threads.emplace_back([=, &stops]() mutable {
                    t_search.iterative_search(t_board, depth, i, stops[i]);
                });
            }

            best_move = searcher.iterative_search(game_board, depth, 0, stops[0]);

            for (int i = 1; i < thread_count; ++i) {
                stops[i] = true;
            }
            for (int i = 1; i < thread_count; ++i) {
                threads[i - 1].join();
            }

            // best_move = searcher.iterative_search(game_board, depth);

            cout << "bestmove " << best_move << endl;
        }
    }
}