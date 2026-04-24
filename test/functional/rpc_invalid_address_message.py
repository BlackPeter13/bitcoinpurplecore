#!/usr/bin/env python3
# Copyright (c) 2020-2022 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test error messages for 'getaddressinfo' and 'validateaddress' RPC commands."""

from test_framework.test_framework import BitcoinPurpleTestFramework

from test_framework.util import (
    assert_equal,
    assert_raises_rpc_error,
)

BECH32_VALID = 'rbtcp1qtmp74ayg7p24uslctssvjm06q5phz4yrwxzxsu'
BECH32_VALID_CAPITALS = 'RBTCP1QPLMTZKC2XHARPPZDLNPAQL78RSHJ68U3EE8EAN'
BECH32_VALID_MULTISIG = 'rbtcp1qdg3myrgvzw7ml9q0ejxhlkyxm7vl9r56yzkfgvzclrf4hkpx9yfq5lcnk2'

BECH32_INVALID_BECH32 = 'rbtcp1pqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqdnynek'
BECH32_INVALID_BECH32M = 'rbtcp1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqsskgfc'
BECH32_INVALID_VERSION = 'rbtcp13qqqq0pjvuz'
BECH32_INVALID_SIZE = 'rbtcp1sqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq73a74a'
BECH32_INVALID_V0_SIZE = 'rbtcp1qqqqqqqqqqqqqqqqqyefc6q'
BECH32_INVALID_PREFIX = 'bc1pw508d6qejxtdg4y5r3zarvary0c5xw7kw508d6qejxtdg4y5r3zarvary0c5xw7k7grplx'
BECH32_TOO_LONG = 'rbtcp1q049edschfnwystcqnsvyfpj23mpsg3jcedq9xv049edschfnwystcqnsvyfpj23mpsg3jcedq9xv049edschfnwystcqnsvyfpj23m'
BECH32_ONE_ERROR = 'rbtcp1qtmp84ayg7p24uslctssvjm06q5phz4yrwxzxsu' # pos 10 corrupted (7→8)
BECH32_ONE_ERROR_CAPITALS = 'RBTCP1QTMP74AYG7P24USLCTSSVJM06Q5PHZ4YRXXZXSU' # pos 39 corrupted (W→X)
BECH32_TWO_ERRORS = 'rbtcp1qtmp74ayg7p24uslcsssvjm06q5phz4yrwyzxsu' # pos 23,40 corrupted
BECH32_NO_SEPARATOR = 'rbtcpq049ldschfnwystcqnsvyfpj23mpsg3jcedq9xv'
BECH32_INVALID_CHAR = 'rbtcp1q04oldschfnwystcqnsvyfpj23mpsg3jcedq9xv'
BECH32_MULTISIG_TWO_ERRORS = 'rbtcp1qdg3myrgvzw7mlzq0ejxhlkyxp7vl9r56yzkfgvzclrf4hkpx9yfq5lcnk2' # pos 20,31 corrupted
BECH32_WRONG_VERSION = 'rbtcp1ptmp74ayg7p24uslctssvjm06q5phz4yrwxzxsu'

BASE58_VALID = 'PbES2crq6ksXDrTEyepNAwfRBpjhtwxH2g'
BASE58_INVALID_PREFIX = '17VZNX1SN5NtKa8UQFxwQbFeFc3iqRYhem'
BASE58_INVALID_CHECKSUM = 'PbES2crq6ksXDrTEyepNAwfRBpjhtwxH2f'
BASE58_INVALID_LENGTH = '2VKf7XKMrp4bVNVmuRbyCewkP8FhGLP2E54LHDPakr9Sq5mtU2'

INVALID_ADDRESS = 'asfah14i8fajz0123f'
INVALID_ADDRESS_2 = '1q049ldschfnwystcqnsvyfpj23mpsg3jcedq9xv'

class InvalidAddressErrorMessageTest(BitcoinPurpleTestFramework):
    def add_options(self, parser):
        self.add_wallet_options(parser)

    def set_test_params(self):
        self.setup_clean_chain = True
        self.num_nodes = 1

    def check_valid(self, addr):
        info = self.nodes[0].validateaddress(addr)
        assert info['isvalid']
        assert 'error' not in info
        assert 'error_locations' not in info

    def check_invalid(self, addr, error_str, error_locations=None):
        res = self.nodes[0].validateaddress(addr)
        assert not res['isvalid']
        assert_equal(res['error'], error_str)
        if error_locations:
            assert_equal(res['error_locations'], error_locations)
        else:
            assert_equal(res['error_locations'], [])

    def test_validateaddress(self):
        # Invalid Bech32
        self.check_invalid(BECH32_INVALID_SIZE, 'Invalid Bech32 address data size')
        self.check_invalid(BECH32_INVALID_PREFIX, 'Invalid or unsupported Segwit (Bech32) or Base58 encoding.')
        self.check_invalid(BECH32_INVALID_BECH32, 'Version 1+ witness address must use Bech32m checksum')
        self.check_invalid(BECH32_INVALID_BECH32M, 'Version 0 witness address must use Bech32 checksum')
        self.check_invalid(BECH32_INVALID_VERSION, 'Invalid Bech32 address witness version')
        self.check_invalid(BECH32_INVALID_V0_SIZE, 'Invalid Bech32 v0 address data size')
        self.check_invalid(BECH32_TOO_LONG, 'Bech32 string too long', list(range(90, 109)))
        self.check_invalid(BECH32_ONE_ERROR, 'Invalid Bech32 checksum', [10])
        self.check_invalid(BECH32_TWO_ERRORS, 'Invalid Bech32 checksum', [23, 40])
        self.check_invalid(BECH32_ONE_ERROR_CAPITALS, 'Invalid Bech32 checksum', [39])
        self.check_invalid(BECH32_NO_SEPARATOR, 'Missing separator')
        self.check_invalid(BECH32_INVALID_CHAR, 'Invalid Base 32 character', [9])
        self.check_invalid(BECH32_MULTISIG_TWO_ERRORS, 'Invalid Bech32 checksum', [20, 31])
        self.check_invalid(BECH32_WRONG_VERSION, 'Invalid Bech32 checksum', [6])

        # Valid Bech32
        self.check_valid(BECH32_VALID)
        self.check_valid(BECH32_VALID_CAPITALS)
        self.check_valid(BECH32_VALID_MULTISIG)

        # Invalid Base58
        self.check_invalid(BASE58_INVALID_PREFIX, 'Invalid or unsupported Base58-encoded address.')
        self.check_invalid(BASE58_INVALID_CHECKSUM, 'Invalid checksum or length of Base58 address (P2PKH or P2SH)')
        self.check_invalid(BASE58_INVALID_LENGTH, 'Invalid checksum or length of Base58 address (P2PKH or P2SH)')

        # Valid Base58
        self.check_valid(BASE58_VALID)

        # Invalid address format
        self.check_invalid(INVALID_ADDRESS, 'Invalid or unsupported Segwit (Bech32) or Base58 encoding.')
        self.check_invalid(INVALID_ADDRESS_2, 'Invalid or unsupported Segwit (Bech32) or Base58 encoding.')

        node = self.nodes[0]

        # Missing arg returns the help text
        assert_raises_rpc_error(-1, "Return information about the given bitcoinpurple address.", node.validateaddress)
        # Explicit None is not allowed for required parameters
        assert_raises_rpc_error(-3, "JSON value of type null is not of expected type string", node.validateaddress, None)

    def test_getaddressinfo(self):
        node = self.nodes[0]

        assert_raises_rpc_error(-5, "Invalid Bech32 address data size", node.getaddressinfo, BECH32_INVALID_SIZE)
        assert_raises_rpc_error(-5, "Invalid or unsupported Segwit (Bech32) or Base58 encoding.", node.getaddressinfo, BECH32_INVALID_PREFIX)
        assert_raises_rpc_error(-5, "Invalid or unsupported Base58-encoded address.", node.getaddressinfo, BASE58_INVALID_PREFIX)
        assert_raises_rpc_error(-5, "Invalid or unsupported Segwit (Bech32) or Base58 encoding.", node.getaddressinfo, INVALID_ADDRESS)

    def run_test(self):
        self.test_validateaddress()

        if self.is_wallet_compiled():
            self.init_wallet(node=0)
            self.test_getaddressinfo()


if __name__ == '__main__':
    InvalidAddressErrorMessageTest().main()
