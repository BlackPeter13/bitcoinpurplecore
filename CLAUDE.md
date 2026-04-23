# BitcoinPurple Core

Bitcoin Core fork running the **BTCP** network. Key differences from upstream:

| | BitcoinPurple | Bitcoin |
|--|--|--|
| Ticker | BTCP | BTC |
| Block time | 1 min | 10 min |
| Halving | 500,000 blocks | 210,000 blocks |
| Retarget | every 120 blocks | every 2016 blocks |
| Bech32 HRP | `btcp` / `tbtcp` | `bc` / `tb` |
| Default port | 13496 | 8333 |

All soft-forks (SegWit, Taproot, CSV, BIP34/65/66) active from genesis height 0.

## Build

```bash
# First time
./quick_build.sh --full

# Iterative rebuild (keeps config, 5-10× faster)
./quick_build.sh --rebuild
```

Manual Autotools path — see [doc/build-unix.md](doc/build-unix.md).
Reproducible multi-arch releases: `./docker-build/build-all.sh` (linux-x86_64, aarch64, armv7, windows-x64).

## Executables

| Binary | Path |
|--------|------|
| `bitcoinpurpled` | `src/bitcoinpurpled` |
| `bitcoinpurple-cli` | `src/bitcoinpurple-cli` |
| `bitcoinpurple-qt` | `src/qt/bitcoinpurple-qt` |
| `bitcoinpurple-tx` | `src/bitcoinpurple-tx` |
| `bitcoinpurple-wallet` | `src/bitcoinpurple-wallet` |

## Running a node

Config: `~/.bitcoinpurple/bitcoinpurple.conf`

```bash
./src/bitcoinpurpled -daemon
./src/bitcoinpurple-cli getblockchaininfo
./src/bitcoinpurpled -testnet -daemon   # port 23496
./src/bitcoinpurpled -signet  -daemon   # port 33496
```

## Testing

```bash
# Unit tests
make check

# Functional tests (Python 3.7+, needs built bitcoinpurpled)
python3 test/functional/test_runner.py
python3 test/functional/test_runner.py --extended
python3 test/functional/feature_taproot.py   # single test

# Lint
test/lint/lint-all.sh
```

Use `--port-min=14000` to avoid conflicts with a running mainnet node (same as CI).

## Code style

- **C++**: clang-format (`clang-format -i <file>`), follow [doc/developer-notes.md](doc/developer-notes.md)
- **Python**: yapf (`yapf -ri test/`), config in `.style.yapf`

## Key files

| File | Purpose |
|------|---------|
| [src/kernel/chainparams.cpp](src/kernel/chainparams.cpp) | Network parameters (ports, magic bytes, genesis, consensus) |
| [quick_build.sh](quick_build.sh) | Build automation (`--full` / `--rebuild`) |
| [docker-build/build-all.sh](docker-build/build-all.sh) | Reproducible multi-arch builds |
| [configure.ac](configure.ac) | Autotools entry, version 1.1.0 |
| [.cirrus.yml](.cirrus.yml) | CI (Cirrus, `-j10`, ccache 200 MB) |
