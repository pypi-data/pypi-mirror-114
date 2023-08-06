import io
import os
import unittest
import tempfile
import functools
from unittest import mock
from urllib.error import HTTPError, URLError

from test.test_gpg import (
    CN_UID,
    CN_FINGERPRINT,
    UMLAUTS_UID,
    UMLAUTS_FINGERPRINT,
    CN_PUB_KEY,
    UMLAUTS_PUB_KEY,
    SGT_HARTMANN_PUB_KEY,
    IntegrationTest,
    ENV_WITH_GPG,
    KEY_SERVER,
)

import gpg_lite as gpg
from gpg_lite import keyserver


ENV_KEY_SERVER = os.environ.get("KEY_SERVER", None)
KEY_SERVER = "http://hagrid.hogwarts.org:11371"

# Variables holding different types of errors to simulate non-responding
# keyserver or bad response from keyserver.
URLError = URLError("timeout")
HTTPError_404 = HTTPError(url=KEY_SERVER, code=404, msg="not found", hdrs=None, fp=None)
HTTPError_401 = HTTPError(
    url=KEY_SERVER, code=401, msg="unauthorized", hdrs=None, fp=None
)


class TestKeyserver(unittest.TestCase):
    def test_parse_search_keyserver(self):
        response = io.BytesIO(
            b"""info:1:1
pub:CB5A3A5C2C4419BB09EFF879D6D229C51AB5D107:1:2048:1550241679::
uid:Chuck Norris <chuck.norris@roundhouse.gov>:1550241679::

pub:F119E26211119BB09EFF879D6D229C51AB5D107C:1:2048:1550241679::
uid:With Uml%C3%A4uts <with.umlauts@umlauts.info>:1550241679::

pub:DB5A3A5C2C4419BB09EFF879D6D229C51AB5D107:1:4096:1550241679:1850241679:
uid:Chuck Norris <chuck.norris@roundhouse.gov>:1650241679::
"""
        )
        keys = list(keyserver.parse_search_keyserver(response))
        self.assertEqual(
            keys,
            [
                gpg.KeyInfo(
                    uid=CN_UID,
                    fingerprint=CN_FINGERPRINT,
                    key_algorithm=1,
                    key_length=2048,
                    creation_date="1550241679",
                    expiration_date=None,
                ),
                gpg.KeyInfo(
                    uid=UMLAUTS_UID,
                    fingerprint=UMLAUTS_FINGERPRINT,
                    key_algorithm=1,
                    key_length=2048,
                    creation_date="1550241679",
                    expiration_date=None,
                ),
                gpg.KeyInfo(
                    uid=CN_UID,
                    fingerprint="DB5A3A5C2C4419BB09EFF879D6D229C51AB5D107",
                    key_algorithm=1,
                    key_length=4096,
                    creation_date="1550241679",
                    expiration_date="1850241679",
                ),
            ],
        )

    def test_normalize_fingerprint(self):
        for length in (8, 16, 32, 40):
            fp = "A" * length
            self.assertEqual(keyserver.normalize_fingerprint(fp), f"0x{fp}")
            self.assertEqual(keyserver.normalize_fingerprint(f"0x{fp}"), f"0x{fp}")
        self.assertEqual(keyserver.normalize_fingerprint("123 af  47a"), "0x123af47a")
        with self.assertRaises(ValueError):
            keyserver.normalize_fingerprint("A" * 7)
        with self.assertRaises(ValueError):
            keyserver.normalize_fingerprint("Z" * 8)

    def test_search_keyserver(self):
        # Check that passing a non-existing keyserver value raises the correct
        # type of error.
        search_keyserver = functools.partial(
            keyserver.search_keyserver,
            search_term=CN_FINGERPRINT,
            keyserver=KEY_SERVER,
        )
        with self.assertRaises(keyserver.KeyserverError):
            list(search_keyserver(url_opener=mock.Mock(side_effect=URLError)))

        # Check that a missing key does not raises an error, and that any other
        # type of HTTPError does raise an error.
        list(search_keyserver(url_opener=mock.Mock(side_effect=HTTPError_404)))
        with self.assertRaises(keyserver.KeyserverError):
            list(search_keyserver(url_opener=mock.Mock(side_effect=HTTPError_401)))

    def test_download_key(self):
        # Check that an urllib error of type URLError or HTTPError raises the
        # correct type of error.
        download_key = functools.partial(
            keyserver.download_key,
            fingerprint=CN_FINGERPRINT,
            keyserver=KEY_SERVER,
        )
        with self.assertRaises(keyserver.KeyserverError):
            download_key(url_opener=mock.Mock(side_effect=URLError))
        with self.assertRaises(keyserver.KeyserverKeyNotFoundError):
            download_key(url_opener=mock.Mock(side_effect=HTTPError_404))
        with self.assertRaises(keyserver.KeyserverError):
            download_key(url_opener=mock.Mock(side_effect=HTTPError_401))

    def test_upload_keys(self):
        # Check that an urllib error of type URLError raises the correct type
        # of error.
        upload_keys = functools.partial(
            keyserver.upload_keys,
            keys_as_ascii_armor=CN_PUB_KEY,
            keyserver=KEY_SERVER,
        )
        with self.assertRaises(keyserver.KeyserverError):
            upload_keys(url_opener=mock.Mock(side_effect=URLError))


def to_info(key):
    return gpg.KeyInfo(
        uid=key.uids[0],
        fingerprint=key.fingerprint,
        key_algorithm=key.pub_key_algorithm,
        creation_date=key.creation_date,
        expiration_date=key.expiration_date,
        key_length=key.key_length,
    )


@unittest.skipUnless(ENV_KEY_SERVER is not None and ENV_WITH_GPG, "Key Server Tests")
class TestKeyserverIntegration(IntegrationTest):
    def test_send_search(self):
        self.s.import_file(CN_PUB_KEY)
        self.s.import_file(UMLAUTS_PUB_KEY)
        key_a, key_b = self.s.list_pub_keys()

        self.s.send_keys(key_a.key_id, key_b.key_id, keyserver=ENV_KEY_SERVER)

        keys = keyserver.search_keyserver(
            key_a.uids[0].full_name, keyserver=ENV_KEY_SERVER
        )
        self.assertEqual(list(keys), [to_info(key_a)])

        keys = keyserver.search_keyserver(
            key_b.uids[0].full_name, keyserver=ENV_KEY_SERVER
        )
        self.assertEqual(list(keys), [to_info(key_b)])

        # By fingerprint
        keys = keyserver.search_keyserver(key_b.fingerprint, keyserver=ENV_KEY_SERVER)
        self.assertEqual(list(keys), [to_info(key_b)])

        # By ID
        keys = keyserver.search_keyserver(key_b.key_id, keyserver=ENV_KEY_SERVER)
        self.assertEqual(list(keys), [to_info(key_b)])

    def test_recv_keys(self):
        try:
            with tempfile.TemporaryDirectory() as gpg_temp_dir:
                temp_store = gpg.GPGStore(gpg_temp_dir)
                temp_store.import_file(SGT_HARTMANN_PUB_KEY)
                temp_store.import_file(UMLAUTS_PUB_KEY)
                key_a, key_b = temp_store.list_pub_keys(sigs=True)
                self.assertTrue(key_a.signatures or key_b.signatures)
                temp_store.send_keys(
                    key_a.key_id, key_b.key_id, keyserver=ENV_KEY_SERVER
                )
        except FileNotFoundError:
            pass
        self.s.recv_keys(key_a.key_id, key_b.fingerprint, keyserver=ENV_KEY_SERVER)
        keys = set(self.s.list_pub_keys(sigs=True))
        self.assertEqual({key_a, key_b}, keys)
