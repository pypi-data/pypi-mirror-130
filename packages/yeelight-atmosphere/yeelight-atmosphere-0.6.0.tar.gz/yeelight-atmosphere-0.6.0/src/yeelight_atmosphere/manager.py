"""
Module of manager for managing multiple bulbs.
"""
import logging
import platform
import subprocess
import threading
import time
from copy import copy
from queue import Queue
from typing import List

import ifaddr
from sqlalchemy import func
from yeelight import discover_bulbs, BulbException

from .bulb import Bulb, session
from .color import Color
from .exception import BulbConnectionLostException
from .generator import ColorGenerator


class ThreadExtension:
    """ Container for threading objects """

    def __init__(self):
        self.polling_thread = None
        self.polling_thread_exit_event = threading.Event()
        self.events_queue = Queue()


class BulbManager:
    """
    Class for managing bulbs.
    """

    def __init__(self, use_last_bulb: bool, bulb_ip_address: str,
                 effect: str = 'smooth', timeout: int = 5):
        self.use_last_bulb = use_last_bulb
        self.effect = effect
        self.bulb_ip_address = bulb_ip_address
        self.timeout = timeout
        self.cached_bulbs = None
        self.chosen_bulbs = set()
        self.thread_ext = ThreadExtension()
        self.cmd_map = {}
        self._init_cmd_map()

    def run_atmosphere(self, strategy, delay) -> None:
        """
        Main entrypoint. Chooses bulb, starts colors polling thread.
        :param strategy: defines screens areas to capture
        :param delay: delay (secs) between generator yield colors
        :return:
        """
        self.choose()

        if isinstance(self.thread_ext.polling_thread, threading.Thread):
            # Stop current thread.
            self.thread_ext.polling_thread_exit_event.set()
            logging.info("Waiting for thread exit.")
            time.sleep(1)

        self.thread_ext.polling_thread_exit_event.clear()
        self.thread_ext.polling_thread = threading.Thread(
            target=self._colors_polling,
            args=(strategy, delay, self.thread_ext.polling_thread_exit_event))
        self.thread_ext.polling_thread.setDaemon(True)
        self.thread_ext.polling_thread.start()

    def gather_commands(self) -> None:
        """
        Entrypoint for interaction with running program.
        :return:
        """
        desc = self._get_cmd_description()
        while True:
            cmd = input(desc)
            cmd_num = int(cmd) if cmd.isnumeric() else None
            if cmd_num in self.cmd_map:
                cmd_execution = self.cmd_map[cmd_num]
                func_cmd = cmd_execution["f"]
                func_args = cmd_execution["args"]
                func_kwargs = cmd_execution["kwargs"]
                func_cmd(*func_args, **func_kwargs)
            else:
                logging.info("Bad command.")

    def choose(self, reset=False) -> Bulb:
        """
        Choose bulbs to interact with.
        :param reset:
        :return:
        """
        result = None
        if reset:
            self.use_last_bulb = False
            self.bulb_ip_address = None
            self.cached_bulbs = None

        if self.use_last_bulb:
            last_bulb = self.get_last_bulb()
            if last_bulb and last_bulb.is_valid():
                last_bulb.last_ip = self.get_current_ip_by_bulb_id(last_bulb.id)
                last_bulb.last_usage = func.now()
                self.send_to_db(last_bulb)
                result = last_bulb
            else:
                logging.info("Last bulb was not found.")
        elif self.bulb_ip_address:
            if self.is_bulb_alive(self.bulb_ip_address):
                result = self.get_bulb_by_ip(self.bulb_ip_address)
            else:
                logging.info("IP %s is not active.", self.bulb_ip_address)

        if not result:
            result = self.choose_alive()
        if result and not self.bulb_chosen(result):
            self.chosen_bulbs.add(result)
        return result

    def choose_alive(self) -> (Bulb, None):
        """
        Command line function to choose bulb.
        :return: chosen bulb
        """
        while True:
            try:
                bulbs = self.get_alive_bulbs()
                variants = set()
                for i, bulb in enumerate(bulbs):
                    print(f"{i}) {bulb.get('ip', None)}")
                    variants.add(str(i))
                while True:
                    inp = input("Enter bulb number ('' for none): ")
                    if inp == '':
                        return None
                    if inp in variants:
                        break
                choice = bulbs[int(inp)]
                new_bulb = self.new_bulb_from_dict(choice)
                if not self.bulb_chosen(new_bulb):
                    new_bulb.init_obj(new_bulb.last_ip, self.effect)

                self.send_to_db(new_bulb)
                break
            except BulbConnectionLostException:
                time.sleep(3)
                self.get_alive_bulbs(True)

        return new_bulb

    def add_bulb(self) -> Bulb:
        """
        Chose alive bulb and add to chosen set.
        :return:
        """
        result = self.choose_alive()
        if result and not self.bulb_chosen(result):
            self.chosen_bulbs.add(result)
        return result

    def get_alive_bulbs(self, reset=False) -> List[dict]:
        """
        :param reset: flag to reset cached list of bulbs
        :return: result of discover_bulbs(), list of dicts:
        {'ip': '192.168.1.4', 'port': 55443, 'capabilities': {...}}
        """
        if (not self.cached_bulbs) or reset:
            tmp_res = []
            srt_adapters = sorted(
                ifaddr.get_adapters(), key=lambda a: tuple(sorted(
                    [ip.ip for ip in a.ips if isinstance(ip.ip, str)]
                )),
                reverse=True)  # Sorting of adapters by IP, to visit local 192.* first
            for adapter in srt_adapters:
                logging.info("Start discover bulbs with %s s timeout "
                             "at interface %s.",
                             self.timeout, adapter.nice_name)
                try:
                    tmp_res = discover_bulbs(self.timeout, adapter.name)
                except OSError:
                    tmp_res = []
                if tmp_res:
                    break
            self.cached_bulbs = tmp_res
            logging.info("Found %s bulbs.", len(self.cached_bulbs))
        return self.cached_bulbs

    def get_current_ip_by_bulb_id(self, id_) -> str:
        """
        :param id_: bulb id given by discover_bulbs(), example: '0x00000000129f22a6'
        :return: ip address string
        """
        alive_bulbs = self.get_alive_bulbs()
        current_ip = None
        for bulb_d in alive_bulbs:
            capabilities = bulb_d.get('capabilities', None)
            if isinstance(capabilities, dict):
                cur_id = capabilities.get('id', None)
                if cur_id == id_:
                    cur_ip = bulb_d.get("ip", None)
                    current_ip = cur_ip

        return current_ip

    def get_bulb_by_ip(self, ip_address) -> Bulb:
        """
        :param ip_address:
        :return: dict from discover_bulbs() representing a bulb
        """
        bulbs = self.get_alive_bulbs()
        res = None
        for bulb in bulbs:
            if bulb.get('ip') == ip_address:
                res = bulb
                break

        new_bulb = None
        if res:
            new_bulb = self.new_bulb_from_dict(res)
            if not self.bulb_chosen(new_bulb):
                new_bulb.init_obj(new_bulb.last_ip, self.effect)
            self.send_to_db(new_bulb)

        return new_bulb

    @staticmethod
    def get_last_bulb() -> Bulb:
        """
        :return: last used bulb from database
        """
        max_query = session.query(func.max(Bulb.last_usage))
        bulb = session.query(Bulb).filter(Bulb.last_usage == max_query.scalar_subquery()).first()
        if bulb and bulb.last_ip is None:
            bulb = None

        return bulb if bulb else None

    def is_bulb_alive(self, ip_address) -> bool:
        """
        :param ip_address: ip address of bulb
        :return: True if a bulb is pinging
        """
        res = self._ping_bulb(ip_address)
        return res

    def bulb_chosen(self, bulb: Bulb) -> bool:
        """
        Check if bulb is already chosen by its IP.
        :param bulb:
        :return:
        """

        return bulb.last_ip in [b.last_ip for b in self.chosen_bulbs]

    @staticmethod
    def send_to_db(inst: Bulb) -> None:
        """
        Saves instance to database.
        :param inst: instance of Bulb
        :return: None
        """
        session.merge(inst)
        session.commit()

    @staticmethod
    def new_bulb_from_dict(b_dict) -> Bulb:
        """
        Create Bulb object from dictionary (given by discover_bulbs())
        :param b_dict: dict of bulb
        :return: Bulb object
        """
        tmp_bulb = Bulb()
        caps = b_dict.get("capabilities", {})
        tmp_bulb.id = caps.get("id", '')
        tmp_bulb.name = caps.get("name", '')
        tmp_bulb.last_usage = func.now()
        tmp_bulb.last_ip = b_dict.get("ip", '')

        return tmp_bulb

    def change_color(self, color: Color, bulb: Bulb = None) -> None:
        """
        Interface of changing bulb color, with catching connection errors.
        :param color: Color object to set.
        :param bulb: Bulb object to be changed,
        if None given operation applies to all chosen bulbs of BulbManager.
        :return: None
        """
        bulbs = self.chosen_bulbs if not bulb else set(bulb)
        # Safe iteration over copy to prevent changing by other threads.
        for bulb_item in copy(bulbs):
            try:
                bulb_item.change_color(color)
            except BulbException:
                logging.info("Connection lost. Retrying... ")
                try:
                    bulb_item.init_obj()
                except BulbConnectionLostException:
                    self.chosen_bulbs.clear()
                    logging.info("Connection was not established.")
                    self.choose(True)

    @staticmethod
    def _ping_bulb(host) -> bool:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', host]
        with subprocess.Popen(command,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              shell=True) as pipe:
            _, errors = pipe.communicate()
        return not errors

    def _colors_polling(self, strategy, delay, stop_event) -> None:
        """
        Creates color generator and changes colors of bulbs
        :param strategy: defines screens areas to capture
        :param delay: delay (secs) between generator yield colors
        :param stop_event: if set the thread stops
        :return:
        """
        for new_color in ColorGenerator(strategy).generator(delay):
            self.change_color(new_color)
            if stop_event.is_set():
                logging.info("Thread %s stopped.", threading.get_ident())
                break

    def _init_cmd_map(self):
        """
        Creates commands map.
        :return:
        """
        self.cmd_map = {
            1: {
                "desc": "Add bulb.",
                "f": self.add_bulb,
                "args": (),
                "kwargs": {}
            },
        }

    def _get_cmd_description(self) -> str:
        """
        :return: String representation of available commands.
        """
        start = "Available commands:"
        lines = []
        for cmd_num, cmd_dict in self.cmd_map.items():
            desc = cmd_dict.get("desc")
            lines.append(f"{cmd_num}. {desc}")
        return "\n".join([start, ] + lines + ["\n", ])
