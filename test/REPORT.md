# Test Report — BitcoinPurple

Overview of the environment setup and available test types, with commands and current status.

| # | Type | Status |
|---|------|--------|
| 0 | Preparation (build) | ⬜ To do |
| 1 | Unit Tests | ⬜ To do |
| 2 | Functional Tests | ⬜ To do |
| 3 | Fuzz Tests | ⬜ To do |
| 4 | Lint | ⬜ To do |
| 5 | Util / Integration Tests | ⬜ To do |

---

## 0. Preparation — Full Build

The project must be compiled with test and wallet support before running any tests.

### 0.1 System dependencies

```bash
# Ubuntu / Debian
sudo apt-get install -y \
    build-essential libtool autotools-dev automake pkg-config bsdmainutils \
    libssl-dev libevent-dev libboost-all-dev \
    libdb-dev libdb++-dev \
    libzmq3-dev \
    python3 python3-pip \
    libsqlite3-dev \
    clang
```

### 0.2 Generate the build system

```bash
./autogen.sh
```

### 0.3 Configuration

BerkeleyDB 4.8 is not available in the official Ubuntu 24.04 repositories and must be compiled from source (one-time step):

```bash
wget https://download.oracle.com/berkeley-db/db-4.8.30.NC.tar.gz
tar xzf db-4.8.30.NC.tar.gz
cd db-4.8.30.NC/build_unix
../dist/configure --enable-cxx --disable-shared --with-pic --prefix=/usr/local
# fix conflict with modern GCC
sed -i 's/__atomic_compare_exchange/__atomic_compare_exchange_db/g' ../dbinc/atomic.h
make -j$(nproc)
sudo make install
cd ../..
```

Then configure the project:

```bash
BDB_CFLAGS="-I/usr/local/include" \
BDB_LIBS="-L/usr/local/lib -ldb_cxx-4.8" \
./configure \
    --enable-wallet \
    --with-sqlite \
    --enable-zmq \
    --enable-tests \
    --enable-external-signer \
    --with-gui=no
```

| Flag | Tests covered |
|------|--------------|
| `--enable-wallet` | all wallet tests (unit + functional) |
| `--with-sqlite` | descriptor wallet tests (`wallet_descriptor.py`, `wallet_taproot.py`, etc.) |
| `--enable-zmq` | `interface_zmq.py` |
| `--enable-external-signer` | `wallet_signer.py`, `rpc_signer.py` |
| `--with-gui=no` | skips Qt tests (use `--with-gui=qt5` to include them) |

### 0.4 Build

```bash
make -j$(nproc)
```

> To avoid port conflicts with a running mainnet node, add `--port-min=14000`
> when launching functional tests (see section 2).

### 0.5 Check produced binaries

| Binary | Path |
|--------|------|
| `bitcoinpurpled` | `src/bitcoinpurpled` |
| `bitcoinpurple-cli` | `src/bitcoinpurple-cli` |
| `bitcoinpurple-tx` | `src/bitcoinpurple-tx` |
| `bitcoinpurple-wallet` | `src/bitcoinpurple-wallet` |
| `bitcoinpurple-qt` | `src/qt/bitcoinpurple-qt` *(only with --with-gui)* |

**Status:** ⬜ To do

---

## 1. Unit Tests

**Description:** C++ tests that verify individual functions and internal modules (amount, base58, addrman, wallet, Qt, etc.).

**Directories:** `src/test/`, `src/wallet/test/`, `src/qt/test/`

**Prerequisites:** Build completed (section 0), with `--enable-wallet` for wallet tests and `--with-gui=qt5` for Qt tests.

**Command:**
```bash
make check
```

**Status:** ⬜ To do

---

## 2. Functional Tests

**Description:** End-to-end Python tests that spin up real `bitcoinpurpled` nodes and verify protocol behaviour, RPC, wallet, mempool, taproot, segwit, etc.

**Directory:** `test/functional/`

**Prerequisites:** Build completed (section 0), Python ≥ 3.7.

```bash
pip3 install -r test/functional/requirements.txt   # if present
```

**Commands:**
```bash
# Full suite
python3 test/functional/test_runner.py

# Full suite (alternate port to avoid mainnet conflict)
python3 test/functional/test_runner.py --port-min=14000

# Extended suite (includes slower tests)
python3 test/functional/test_runner.py --extended

# Single test
python3 test/functional/feature_taproot.py
```

**Status:** ⬜ To do

---

## 3. Fuzz Tests

**Description:** Fuzzing tests that feed random and malformed input to the code to detect crashes, undefined behaviour, or vulnerabilities.

**Directory:** `test/fuzz/`

**Prerequisites:** Dedicated build with sanitizers:

```bash
./configure \
    --enable-fuzz \
    --with-sanitizers=address,fuzzer,undefined \
    CC=clang CXX=clang++
make -j$(nproc)
```

**Command:**
```bash
python3 test/fuzz/test_runner.py
```

**Status:** ⬜ To do

---

## 4. Lint

**Description:** Python and Shell scripts that check code quality: circular dependencies, header guards, Python style, format strings, commit messages, etc.

**Directory:** `test/lint/`

**Prerequisites:** Python 3, `flake8`, `mypy` (optional), `shellcheck`.

```bash
pip3 install flake8 mypy
sudo apt-get install -y shellcheck
```

**Command:**
```bash
test/lint/lint-all.sh
```

**Status:** ⬜ To do

---

## 5. Util / Integration Tests

**Description:** Tests for command-line tools (`bitcoinpurple-tx`, `bitcoinpurple-cli`) using pre-defined test vectors in `test/util/data/`. Run automatically alongside unit tests.

**Directory:** `test/util/`

**Prerequisites:** Build completed (section 0).

**Command:**
```bash
make check
```

**Status:** ⬜ To do
