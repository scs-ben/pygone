#!/usr/bin/env python3
"""Build a diverse, Stockfish-filtered opening suite from local PGNs."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import chess
import chess.engine
import chess.pgn


ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    ("curated", ROOT / "test" / "balance.pgn", (6,), True),
    ("historical", ROOT / "bin" / "games.pgn", (6, 8, 10, 12), False),
    ("tcec", ROOT / "tcec_games" / "pygone.pgn", (6, 8, 10, 12), False),
    ("tcec-c4ke", ROOT / "tcec_games" / "c4ke_pygone.pgn", (6, 8, 10, 12), False),
)


@dataclass
class Opening:
    source: str
    game_number: int
    plies: int
    moves: tuple[chess.Move, ...]
    key: str
    score: int = 0
    curated: bool = False

    @property
    def group(self) -> tuple[str, int]:
        return self.source, self.game_number


def position_key(board: chess.Board) -> str:
    return " ".join(board.fen().split()[:4])


def read_candidates() -> list[Opening]:
    candidates: list[Opening] = []
    seen: set[str] = set()

    for source, path, depths, curated in SOURCES:
        with path.open(encoding="utf-8", errors="replace") as handle:
            game_number = 0
            while game := chess.pgn.read_game(handle):
                game_number += 1
                moves = tuple(game.mainline_moves())
                for plies in depths:
                    if len(moves) < plies:
                        continue
                    board = game.board()
                    for move in moves[:plies]:
                        board.push(move)
                    key = position_key(board)
                    if key in seen or board.is_game_over():
                        continue
                    seen.add(key)
                    candidates.append(
                        Opening(
                            source=source,
                            game_number=game_number,
                            plies=plies,
                            moves=moves[:plies],
                            key=key,
                            curated=curated,
                        )
                    )

    return candidates


def score_candidates(candidates: list[Opening], stockfish: Path, nodes: int) -> None:
    with chess.engine.SimpleEngine.popen_uci(str(stockfish)) as engine:
        engine.configure({"Threads": 1, "Hash": 16})
        for index, opening in enumerate(candidates, 1):
            board = chess.Board()
            for move in opening.moves:
                board.push(move)
            info = engine.analyse(board, chess.engine.Limit(nodes=nodes))
            score = info["score"].pov(chess.WHITE).score(mate_score=100_000)
            opening.score = score if score is not None else 100_000
            if index % 25 == 0:
                print(f"analysed {index}/{len(candidates)}")


def select_openings(candidates: list[Opening], count: int, max_cp: int) -> list[Opening]:
    curated = [opening for opening in candidates if opening.curated]
    selected = list(curated)
    selected_keys = {opening.key for opening in selected}
    per_game: Counter[tuple[str, int]] = Counter()

    pool = sorted(
        (opening for opening in candidates if not opening.curated),
        key=lambda opening: (abs(opening.score), opening.source, opening.game_number, opening.plies),
    )

    # First pass favors broad game coverage and permits at most two nearby
    # positions from any single source game.
    for opening in pool:
        if len(selected) >= count:
            break
        if abs(opening.score) > max_cp or per_game[opening.group] >= 2:
            continue
        selected.append(opening)
        selected_keys.add(opening.key)
        per_game[opening.group] += 1

    # If the diversity cap leaves the suite short, fill with the most balanced
    # remaining unique positions while retaining the same evaluation bound.
    if len(selected) < count:
        for opening in pool:
            if len(selected) >= count:
                break
            if opening.key in selected_keys or abs(opening.score) > max_cp:
                continue
            selected.append(opening)
            selected_keys.add(opening.key)

    if len(selected) < count:
        raise RuntimeError(
            f"Only {len(selected)} openings passed the {max_cp} cp filter; "
            "raise --max-cp or add source games"
        )

    return selected[:count]


def write_suite(openings: list[Opening], output: Path) -> None:
    rendered: list[str] = []

    for index, opening in enumerate(openings, 1):
        game = chess.pgn.Game()
        game.headers["Event"] = f"pygone balanced opening {index:03d}"
        game.headers["Site"] = opening.source
        game.headers["Round"] = str(opening.game_number)
        game.headers["Result"] = "*"
        game.headers["PlyCount"] = str(opening.plies)
        game.headers["Annotator"] = f"Stockfish {opening.score:+d} cp"
        node = game
        for move in opening.moves:
            node = node.add_variation(move)
        rendered.append(
            game.accept(chess.pgn.StringExporter(headers=True, variations=False, comments=False))
        )

    output.write_text("\n\n".join(rendered) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--nodes", type=int, default=5_000)
    parser.add_argument("--max-cp", type=int, default=120)
    parser.add_argument(
        "--stockfish", type=Path, default=ROOT / "bin" / "stockfish" / "stockfish"
    )
    parser.add_argument("--output", type=Path, default=ROOT / "test" / "balance100.pgn")
    args = parser.parse_args()

    candidates = read_candidates()
    print(f"found {len(candidates)} unique candidate positions")
    score_candidates(candidates, args.stockfish, args.nodes)
    selected = select_openings(candidates, args.count, args.max_cp)
    write_suite(selected, args.output)

    scores = [abs(opening.score) for opening in selected]
    sources = Counter(opening.source for opening in selected)
    print(f"wrote {len(selected)} openings to {args.output}")
    print(f"absolute evaluation: median={sorted(scores)[len(scores)//2]} max={max(scores)} cp")
    print("sources:", ", ".join(f"{source}={count}" for source, count in sorted(sources.items())))


if __name__ == "__main__":
    main()
