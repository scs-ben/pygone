param(
    [ValidateSet('Regression', 'Stockfish')]
    [string]$Mode = 'Regression',
    [int]$Rounds = 10,
    [int]$Concurrency = 2,
    [string]$TimeControl = '0/10+0.1',
    [int]$MaxMoves = 100,
    [int]$Seed = 2025,
    [int]$StockfishNodes = 1000,
    [ValidateSet('sequential', 'random')]
    [string]$OpeningOrder = 'sequential',
    [string]$OpeningsFile = '',
    [string]$BaselineArtifact = '',
    [string]$BaselineWslPath = '',
    [switch]$DebugLog
)

$ErrorActionPreference = 'Stop'
$repoDir = Split-Path -Parent $PSScriptRoot
$cutechess = 'C:\Program Files (x86)\Cute Chess\cutechess-cli.exe'
$wsl = "$env:WINDIR\System32\wsl.exe"

function Convert-ToWslPath([string]$Path) {
    $resolved = (Resolve-Path -LiteralPath $Path).Path
    if ($resolved -notmatch '^([A-Za-z]):\\(.*)$') {
        throw "Expected an absolute Windows path: $resolved"
    }
    $drive = $Matches[1].ToLowerInvariant()
    $relative = $Matches[2].Replace('\', '/')
    return "/mnt/$drive/$relative"
}

if (-not (Test-Path -LiteralPath $cutechess)) {
    throw "Cute Chess CLI was not found at $cutechess"
}

$candidate = Convert-ToWslPath "$repoDir\dist\pygone"
$packedRunner = Convert-ToWslPath "$PSScriptRoot\run_packed.sh"
$openings = if ($OpeningsFile) {
    (Resolve-Path -LiteralPath $OpeningsFile).Path
} else {
    (Resolve-Path -LiteralPath "$PSScriptRoot\balance100.pgn").Path
}
$outputPrefix = Join-Path $PSScriptRoot ("{0}-{1:yyyyMMdd-HHmmss}" -f $Mode.ToLowerInvariant(), (Get-Date))

$candidateEngine = @(
    '-engine', 'name=candidate', "cmd=$wsl",
    'arg=--exec', 'arg=/bin/bash', "arg=$packedRunner", "arg=$candidate",
    'proto=uci'
)

if ($Mode -eq 'Stockfish') {
    $stockfish = Convert-ToWslPath "$repoDir\bin\stockfish\stockfish"
    $opponentEngine = @(
        '-engine', "name=stockfish-$StockfishNodes", "cmd=$wsl",
        'arg=--exec', "arg=$stockfish", 'proto=uci', "nodes=$StockfishNodes"
    )
} else {
    $baseline = if ($BaselineWslPath) {
        $BaselineWslPath
    } elseif ($BaselineArtifact) {
        Convert-ToWslPath $BaselineArtifact
    } else {
        Convert-ToWslPath "$repoDir\historical\pygone2-fb1ccc"
    }
    $opponentEngine = @(
        '-engine', 'name=baseline', "cmd=$wsl",
        'arg=--exec', 'arg=/bin/bash', "arg=$packedRunner", "arg=$baseline",
        'proto=uci'
    )
}

$arguments = @(
    $candidateEngine
    $opponentEngine
    '-each', "tc=$TimeControl", 'timemargin=10000', 'restart=on'
    '-openings', "file=$openings", "order=$OpeningOrder"
    '-srand', $Seed
    '-repeat'
    '-pgnout', "$outputPrefix.pgn", 'min'
    '-recover'
    '-concurrency', $Concurrency
    '-maxmoves', $MaxMoves
    '-resign', 'movecount=6', 'score=2000'
    '-games', 2
    '-rounds', $Rounds
)

if ($DebugLog) {
    $arguments = @('-debug') + $arguments
}

Write-Host "mode=$Mode rounds=$Rounds concurrency=$Concurrency tc=$TimeControl maxmoves=$MaxMoves seed=$Seed"
Write-Host "openings=$openings order=$OpeningOrder"
if ($Mode -eq 'Stockfish') {
    Write-Host "stockfish_nodes=$StockfishNodes"
}

$savedErrorActionPreference = $ErrorActionPreference
$savedNativeErrorPreference = $PSNativeCommandUseErrorActionPreference
try {
    # Cute Chess emits recoverable engine-pipe warnings on stderr. Log them,
    # but use the process exit code—not PowerShell's stderr wrapper—to fail.
    $ErrorActionPreference = 'Continue'
    $PSNativeCommandUseErrorActionPreference = $false
    & $cutechess @arguments 2>&1 | Tee-Object -FilePath "$outputPrefix.log"
    $exitCode = $LASTEXITCODE
} finally {
    $ErrorActionPreference = $savedErrorActionPreference
    $PSNativeCommandUseErrorActionPreference = $savedNativeErrorPreference
}

if ($exitCode -ne 0) {
    throw "Cute Chess exited with code $exitCode"
}
