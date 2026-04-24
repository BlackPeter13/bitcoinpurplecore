# BitcoinPurple Core

Bitcoin Core fork. Ticker **BTCP**, block time 1 min, halving every 500k blocks, retarget every 120 blocks. All soft-forks active from genesis.

| Network | Port  | Bech32 HRP |
|---------|-------|------------|
| mainnet | 13496 | `btcp`     |
| testnet | 23496 | `tbtcp`    |
| signet  | 33496 | `tbtcp`    |

Binaries: `src/bitcoinpurpled`, `src/bitcoinpurple-cli`, `src/bitcoinpurple-tx`, `src/qt/bitcoinpurple-qt`  
Config: `~/.bitcoinpurple/bitcoinpurple.conf`

## Build

```bash
./autogen.sh && ./configure && make -j$(nproc)
```

Dev (no GUI, no wallet): `./configure --without-gui --disable-wallet --enable-debug`  
Dependencies and platform notes: [doc/build-unix.md](doc/build-unix.md)

## Test

```bash
make check                                                   # unit tests
python3 test/functional/test_runner.py -j$(nproc)           # functional tests
python3 test/functional/feature_taproot.py                   # single test
test/lint/lint-all.sh                                        # lint
```

Use `--port-min=14000` to avoid conflicts with a running mainnet node.

## Key files

| File | Purpose |
|------|---------|
| [src/kernel/chainparams.cpp](src/kernel/chainparams.cpp) | Ports, magic bytes, genesis, consensus params |
| [configure.ac](configure.ac) | Version (1.1.0), autotools entry |
| [.cirrus.yml](.cirrus.yml) | CI config |

## Style

C++: `clang-format -i <file>` — Python: `yapf -ri test/`
