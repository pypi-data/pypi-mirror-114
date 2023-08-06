import configparser
import copy
import json
import logging
import os
import re
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Optional

import clipboard
import pandas

from tepezza.hotkey import TepezzaHotkey

_PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))


class _Colors:  # TODO: use actual package or logging
    OK = '\033[94m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'


class TepezzaApi:
    """Partially automate data return from tepezza.com.
    This interface allows a user to efficiently scrape data,
    even though the website uses reCaptcha. It does this by
    monitoring network traffic through tshark while the user
    looks up zipcodes.

    :return: A `TepezzaApi` instance. Call the `logger` method for functionality.
    :rtype: TepezzaApi
    """

    _SEARCH_FOR_KEYS = [
        'TSHARK',
        'CHROME',
        'ZIPCODES',
        'CHROME_PROFILE',
        'CHROME_SSL_LOG',
        'JSON_LOG'
    ]

    _RE_JSON_RAW = re.compile('"json_raw": "([a-f0-9]+)"')

    # TODO: add disable hook to hotkey
    def __init__(self, config_dict: Dict[str, str] = {}):
        """Constructor.

        :param config: Configuration options, must be dict of cls._SEARCH_FOR_KEYS, defaults to {}
        :type config: Dict[str, str], optional
        """

        path_to_config = os.path.join(
            _PACKAGE_DIR, 'data', 'default_config.ini')

        config = configparser.ConfigParser()
        config.read(path_to_config)

        config['PATHS'].update(config_dict)

        for k in self._SEARCH_FOR_KEYS:
            v = config['PATHS'][k]
            abs_path = os.path.join(_PACKAGE_DIR, v)
            setattr(self, k, abs_path)

        self._TSHARK_CMD = f'{self.TSHARK} -l -x -i en0 -o ssl.keylog_file:{self.CHROME_SSL_LOG} -Y json -T ek'

        self.zips = pandas.read_csv(self.ZIPCODES, dtype='str')['ZIP_CODE']

        self._thk = TepezzaHotkey()

        self.__exit__()

    def startup(self) -> None:
        """Start the Chrome and tshark subprocesses.
        """

        self.startup_logger = logging.getLogger("startup")
        self._load_chrome(self.startup_logger)

        while True:
            in_ = input(
                f"Is Chrome loaded? Ready to begin? Press {_Colors.YELLOW}(y){_Colors.ENDC}. ")
            if in_ == "y":
                break

        self.network_subp = subprocess.Popen(
            shlex.split(self._TSHARK_CMD), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
        os.set_blocking(self.network_subp.stdout.fileno(), False)
        os.set_blocking(self.network_subp.stderr.fileno(), False)

        # proceeding too quickly will break things. Added a busy wait from self.network_subp.stderr to fix this
        while self.network_subp.stderr.readline() == '':
            pass

        self.startup_logger.info(
            f"{_Colors.OK}Initialization complete; proceed to Tepezza.{_Colors.ENDC}")

    def _load_chrome(self, logger: logging.Logger) -> None:
        """Open new Chrome window in a subprocess,
        so as to have decryption keys go into
        `CHROME_SSL_LOG`.
        """
        Path(self.CHROME_SSL_LOG).touch(exist_ok=True)
        os.environ['SSLKEYLOGFILE'] = self.CHROME_SSL_LOG

        self.chrome_subp = subprocess.Popen(
            [self.CHROME,
             # https://ivanderevianko.com/2020/04/disable-logging-in-selenium-chromedriver
             '--output=/dev/null',
             '--log-level=3',
             '--disable-logging',
             f"--user-data-dir={self.CHROME_PROFILE}"],
            stdout=subprocess.DEVNULL)
        logger.info(
            f"New Chrome profile launched; {_Colors.FAIL}Do not proceed to Tepezza{_Colors.ENDC}.")

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.exit_logger = logging.getLogger("exit cleanup")
        try:
            self.chrome_subp.kill()
        except AttributeError:
            self.exit_logger.debug("No chrome subprocess found")
        else:
            self.exit_logger.debug("Chrome subprocess killed")

        try:
            self.network_subp.kill()
        except AttributeError:
            self.exit_logger.debug("No network subprocess found")
        else:
            self.exit_logger.debug("Network subprocess killed")

        for path in [
            self.CHROME_PROFILE,
            self.JSON_LOG,
            self.CHROME_SSL_LOG
        ]:
            if os.path.exists(path):
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    elif os.path.isfile(path):
                        os.remove(path)
                except PermissionError as e:
                    self.exit_logger.warning(e, exc_info=True)

        self.exit_logger.info(f"{_Colors.OK}Cleanup complete.{_Colors.ENDC}")

    def _watch_network(self, logger: logging.Logger) -> 'JSON':
        counter = 0
        s = b''  # build up `s` from packets that have missing/cutoff JSON
        while True:
            try:
                in_ = bytes(self.network_subp.stdout.readline(), 'utf-8')
                if in_ == b'':
                    continue
                counter += 1
                pkt = json.loads(in_)
                s = b''

            except (json.JSONDecodeError, json.decoder.JSONDecodeError) as e:  # overflowed
                logger.debug(e, exc_info=True)

                s += in_
                try:
                    pkt = json.loads(s)
                except (json.JSONDecodeError, json.decoder.JSONDecodeError):
                    continue
            s = b''
            try:
                match_obj = self._RE_JSON_RAW.search(json.dumps(pkt))
                assert match_obj, "match_obj"

                json_raw = match_obj.group(1)
                assert json_raw, "json_raw"

                d = json.loads(bytearray.fromhex(json_raw).decode('utf-8'))

                assert d['success'], 'success'
                assert 'data' in d, 'data'

                if isinstance(d['data'], dict) and d['data'].get('message') == 'Unable to connect to server':
                    logger.debug("returning empty data")
                    return []

                assert isinstance(d['data'], list), 'data not list'
                assert all(
                    ('PhysicianAttributes' in i for i in d['data'])), 'not doctor data'

                for i in d['data']:
                    i.pop('GeoLocation')
                return d['data']
            except (KeyError, IndexError, AssertionError, TypeError) as e:
                # with open(f'error_{counter}.json', 'wb+') as f:
                # f.write(in_)
                logger.debug(e, exc_info=True)

    def get_data(self, every: int, filepath: str, write_out: bool = True, start_from: Optional[str] = None) -> pandas.DataFrame:
        """Get doctor data from Tepezza.

        :param every: How often a zipcode is sampled.
        :type every: int
        :param filepath: Filepath to read from/write to (if write_out for latter case). Can be None if start_from is not None.
        :type filepath: str
        :param write_out: whether to continually write to filepath (highly recommended), defaults to True
        :type write_out: bool, optional
        :param start_from: What zipcode the program should start from (value must be in 'ZIPCODE' column if not None), defaults to None
        :type start_from: Optional[str], optional
        :return: Dataframe with doctor information.
        :rtype: pandas.DataFrame
        """

        if start_from is None:
            df = pandas.DataFrame(columns=['ZIPCODE'])
            prev = None
            idx = 0
        else:
            df = pandas.read_csv(filepath, dtype='str', index_col=0)
            assert df['ZIPCODE'].isin([start_from]).any(
            ), 'must have start zipcode already in .csv file'
            prev = None  # TODO: make prev = previous dataframe relevant bits for corner case error checking
            idx = self.zips[self.zips == start_from].index.min()

        self.logger = logging.getLogger("get data")
        self.watch_network_logger = logging.getLogger("watch network")

        self._thk.start()

        while idx < len(self.zips):

            target_zip = self.zips.iloc[idx]
            clipboard.copy(target_zip)

            self.logger.info(
                f"{_Colors.YELLOW}Target zip: {target_zip}{_Colors.ENDC}")
            self.logger.info(
                "Optionally use cmd e; otherwise manually paste/enter/delete (easier on captcha).")

            self._thk.zipcode = target_zip
            self._thk.enabled = True

            res = self._watch_network(self.watch_network_logger)
            self._thk.enabled = False

            if prev == res and prev != []:
                # try again
                prev = None

                zip_to_drop = self.zips.iloc[idx]
                df_to_drop = df[df['ZIPCODE'] == zip_to_drop]
                df.drop(df_to_drop.index, inplace=True)
                if write_out:
                    df.to_csv(filepath)

                self.logger.warning(
                    f"Data match previous. Returning to idx = {idx}.")
                continue

            prev = copy.deepcopy(res)

            if res == []:
                res = [{}] * 50
            for i in res:
                i['ZIPCODE'] = target_zip

            self.logger.debug(res)

            pct_done = round((idx + every) / len(self.zips) * 100, 3)
            self.logger.info(
                f"Done with {idx + every} / {len(self.zips)} ({pct_done}%)")
            df = df.append(res, ignore_index=True)
            if write_out:
                df.to_csv(filepath)

            idx += every

        return df


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    try:
        with TepezzaApi() as api:
            api.startup()
            api.get_data(5, 'data/tepezza_raw.csv', True, '05853')

    except KeyboardInterrupt:
        pass
