# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 jinwoo
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import socket
import os
import json
import binascii
import codecs
import mimetypes
import re
from io import BytesIO
from datetime import datetime
from functools import partial, wraps

from halo import Halo
from devtools import debug
import time
import sys

try:
    from .__version__ import __version__
except:
    from __version__ import __version__

writer = codecs.lookup("utf-8")[3]


class ResponseField:
    status_code = 999
    text = ""
    json = {}
    elapsed = 0
    state = {}
    error = None

    def __init__(self, status_code=None, text=None, json=None, state=None, error=None):
        if status_code:
            self.status_code = status_code
        if text:
            self.text = text
        if json:
            self.json = json
        if state:
            self.state = state
        if error:
            self.error = error

    def __repr__(self):
        return '<Response [%s]> %s' % (self.status_code, self.text)

    def get_json(self, key=None):

        if isinstance(self.text, dict):
            result = self.text
        else:
            try:
                result = json.loads(self.text)
            except:
                result = {
                    "text": self.text
                }

        if isinstance(result, dict):
            result["error"] = self.error

        if key:
            return result.get(key)

        return result

    def set_dict(self, obj=None):
        if isinstance(obj, dict):
            self.json = obj
            self.text = obj

    def get(self, key=None):
        return self.get_json(key)


class ConnectSock:
    def __init__(self, unix_socket="/var/run/docker.sock", timeout=10, debug=False, headers=None, wait_socket=False, retry=3):
        self.unix_socket = unix_socket
        self.timeout = timeout
        self.method = "GET"
        self.url = "/"
        self.wait_socket = wait_socket

        if isinstance(headers, dict):
            self.default_headers = headers
        else:
            self.headers = {
                "Host": "*",
                "Accept": "*/*",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            self.default_headers = self.headers

        self.sock = None
        self.debug = debug
        self._initialize_vars()
        self.connect_error = None
        self.retry = retry

        if debug:
            self.about = {}
            here = os.path.abspath(os.path.dirname(__file__))
            with open(os.path.join(here, '__version__.py'), mode='r', encoding='utf-8') as f:
                exec(f.read(), self.about)
            # print(f"{self.about['__title__']} v{self.about['__version__']}")

    def _initialize_vars(self):
        # self.headers = self.default_headers
        self.headers = self.default_headers.copy()
        self.r_headers = []
        self.r_headers_string = ""
        self.r_body = []
        self.r_body_string = ""
        self.return_merged_values = {}
        self.state = {}
        self.payload = {}
        self.files = {}
        self.detail = False
        self.inspect = False
        self.Response = ResponseField()

    # def _decorator_check_connect(func):
    #     def connect_health_sock(self, *args, **kwargs):
    #         if self.wait_socket:
    #             wait_count = 0
    #             # while os.path.exists(self.unix_socket) is False:
    #             while self.health_check() is False:
    #                 print(f"[{wait_count}] Wait for \'{self.unix_socket}\' to be created")
    #                 time.sleep(1)
    #                 wait_count += 1
    #             # print(f"Successfully \'{self.unix_socket}\' to be created")
    #         func(self, *args, **kwargs)
    #
    #         return
    #     return connect_health_sock

    def health_check(self):
        text = {}
        error_message = ""

        self.connect_error = None
        mandatory_items = ["buildVersion", "buildTags"]
        try:
            health = self._health_check()
            if health:
                res = self.request(url="/system", method="GET")
                status_code = 200
                text = res.get_json()

                for item in mandatory_items:
                    if text.get(item) is None:
                        error_message += f"{item} not found, "
                        status_code = 500
            else:
                status_code = 500
                error_message = self.connect_error
        except Exception as e:
            error_message = e
            status_code = 500

        if error_message:
            text['error'] = error_message

        return ResponseField(status_code=status_code, text=text)

    def _health_check(self):
        if os.path.exists(self.unix_socket) is False:
            self.connect_error = f"_health_check '{self.unix_socket}' socket file not found"
            # print(red(self.connect_error))
            return False
        try:
            self.sock = None
            self._connect_sock_with_exception()
            self.sock.close()
        except Exception as e:
            self.connect_error = f"_health_check cannot connect a socket: {e}"
            # print(red(self.connect_error))
            return False
        return True

    # @_decorator_check_connect
    def _connect_sock(self, timeout=None):
        if self.wait_socket or self.retry >= 0:
            wait_count = 1
            # while os.path.exists(self.unix_socket) is False:
            while self._health_check() is False:
                message = f"[{wait_count}/{self.retry}] Wait for \'{self.unix_socket}\' to be created"
                if self.logger:
                    self.logging(message)
                else:
                    print(message)
                time.sleep(1)
                wait_count += 1
                if self.retry and isinstance(self.retry, int) and self.retry < wait_count:
                    break

            # print(f"Successfully \'{self.unix_socket}\' to be created")
            self._connect_sock_with_exception(timeout=timeout)

        elif self._health_check():
            self._connect_sock_with_exception(timeout=timeout)

        else:
            return False

    def _connect_sock_with_exception(self, timeout=None):
        if timeout:
            connect_timeout = timeout
        else:
            connect_timeout = self.timeout

        if self.unix_socket and os.path.exists(self.unix_socket):
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(connect_timeout)
            sock.connect(self.unix_socket)
            self.sock = sock
        else:
            raise Exception(red(f"[ERROR] Unix Domain Socket not found - '{self.unix_socket}', wait={self.wait_socket}"))

    def _dict_key_title(self, data):
        """
        A case-insensitive ``dict``-like object.
        content-type -> Content-Type
        :param data:
        :return:
        """
        if isinstance(data, dict):
            return {k.title(): self._dict_key_title(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._dict_key_title(v) for v in data]
        else:
            return data

    def _prepare_header(self):
        self.r_headers = [
            f"{self.method} http://*{self.url} HTTP/1.0",
        ]
        if "HTTP/1.1" in self.r_headers[0]:
            self.headers['Connection'] = "close"

        if self.headers:
            for header_k, header_v in self.headers.items():
                self.r_headers.append(f"{header_k}: {header_v}")
        self.r_headers_string = "\r\n".join(self.r_headers)
        self.r_headers_string = _append_new_line(self.r_headers_string, "\r\n")

    def _prepare_body(self, payload=None, files=None):

        if files:
            self.r_body_string, content_type, content_length = self.encode_multipart_formdata(files)
            self.headers['Content-Type'] = content_type
            self.headers['Content-Length'] = content_length
            self.headers['Connection'] = "close"
        elif payload:
            try:
                payload = json.dumps(payload)
                is_json = True
            except:
                is_json = False
                pass

            body_bytes = payload.encode("utf-8")

            if is_json and self.headers.get('Content-Type') is None:
                self.headers['Content-Type'] = "application/json"
            self.headers['Content-Length'] = len(body_bytes)
            self.r_body = [
                f"",
                f"{payload}"
            ]
            self.r_body_string = "\r\n".join(self.r_body)

    def get_encoded_request_data(self):
        """
        Convert header and body into a string that contains "\r\n" and is encoded.
        :return:
        """
        if not isinstance(self.r_headers_string, bytes):
            # self.r_headers_string = f"{self.r_headers_string}\r\n".encode("utf-8")
            self.r_headers_string = f"{self.r_headers_string}".encode("utf-8")
        if not isinstance(self.r_body_string, bytes):
            self.r_body_string = f"{self.r_body_string}\r\n\r\n".encode("utf-8")
        return self.r_headers_string + self.r_body_string

    def encode_multipart_formdata(self, fields, boundary=None):
        """
        Encode the multipart/form-data.
        Uploaded samples.

        --9bc00c50b8fde01d0cd1e50643dbc08c \r\n
        Content-Disposition: form-data; name="json" \r\n\r\n
        JSON data
        --9bc00c50b8fde01d0cd1e50643dbc08c \r\n
        Content-Disposition: form-data; name="genesisZip"; filename="gs.zip"\r\n\r\n
        --9bc00c50b8fde01d0cd1e50643dbc08c \r\n
        multipart/form-data; boundary=9bc00c50b8fde01d0cd1e50643dbc08c

        :param fields:
        :param boundary:
        :return:
        """
        body = BytesIO()
        if boundary is None:
            boundary = choose_boundary()
        for field in _iter_field_objects(fields):
            body.write(b("\r\n--%s\r\n" % (boundary)))
            writer(body).write(field.render_headers())
            data = field.data
            if isinstance(data, int):
                data = str(data)  # Backwards compatibility

            if isinstance(data, str):
                writer(body).write(data)
            else:
                body.write(data)

            body.write(b"\r\n")
        body.write(b("--%s--\r\n" % (boundary)))
        content_type = str("multipart/form-data; boundary=%s" % boundary)
        content_length = body.__sizeof__()
        self.r_body_string = body.getvalue()
        return body.getvalue(), content_type, content_length

    def _decorator_timing(func):
        """
        Decorator to get the elapsed time.
        :return:
        """

        def from_kwargs(self, **kwargs):
            start_time = time.time()
            result = func(self, **kwargs)
            end_time = round(time.time() - start_time, 3)
            # print(f"elapsed = {end_time}")
            # print(f"result = {result} , {type(result)}")
            # if isinstance(result, dict):
            #     result['result']
            if isinstance(result, ResponseField):
                result.elapsed = end_time
                # result.state = self.state
            elif isinstance(result, dict):
                result['elapsed'] = end_time
            return result
        return from_kwargs

    @_decorator_timing
    def request(self, method="GET", url=None, headers={}, payload={}, files={}, return_dict=False, timeout=None):
        """
        Create an HTTP request and send it to the unix domain socket.
        :param method:
        :param url:
        :param headers:
        :param payload:
        :param files: upload the file using 'multipart/form-data'
        :param return_dict: if response is a list type, change to dictionary => e.g., [{"cid":"232"}]  -> {"cid": "232"}
        :return:
        """
        self._initialize_vars()

        if self.debug:
            print(f"unix_socket={self.unix_socket}, url={url}, method={method}, headers={headers}, payload={payload}, files={files}")

        self._connect_sock(timeout=timeout)
        if self.sock:
            self.method = method.upper()

            if url:
                self.url = url

            self.headers.update(self._dict_key_title(headers))
            self._prepare_body(payload, files)
            self._prepare_header()
            request_data = self.get_encoded_request_data()

            if self.debug:
                debug("<<< request_data >>>", request_data)

            self.sock.send(request_data)
            contents = ""
            while True:
                response_data = self.sock.recv(1024)
                if not response_data:
                    break
                contents += str(response_data.decode())
            self.sock.close()
            # debug(contents)
            return self._parsing_response(contents, return_dict=return_dict)
        else:
            return ResponseField(status_code=500, text=f"[ERROR] fail to connection, {self.connect_error}")

    def _parsing_response(self, response, return_dict=False):
        """
        Parse the response value and returns it to a ResponseField model
        :param response: raw response data
        :param return_dict: if response is a list type, change to dictionary => e.g., [{"cid":"232"}]  -> {"cid": "232"}
        :return:
        """
        if response:
            response_lines = response.split('\r\n')
            if response_lines:
                try:
                    status = response_lines[0].split(" ")[1]
                    text = response_lines[-1].strip()
                except:
                    status = 999
                    text = ""

                try:
                    json_dict = json.loads(response_lines[-1])
                    if return_dict and isinstance(json_dict, list):
                        json_dict = json_dict[0]
                        if text.startswith("[") and text.endswith("]"):
                            text = text.strip("[]")
                except Exception as e:
                    json_dict = {}

                self.Response.status_code = int(status)
                self.Response.json = json_dict
                self.Response.text = text
                self.debug_resp_print(self.Response)
        return self.Response
        # return self.response

    def debug_print(self, text, color="blue"):
        if self.debug:
            # version_info = f"{self.about['__title__']} v{self.about['__version__']}"
            version_info = f"v{self.about['__version__']}"
            color_print(f"[{version_info}][DBG] {text}", color)

    def debug_resp_print(self, result):
        if self.debug:
            text = result.text.split("\n")
            if result.status_code == 200:
                color = "green"
                if result.json:
                    debug(result.json)
                elif result.text:
                    debug(result.text)
            else:
                color = "fail"
            self.debug_print(f"status_code={result.status_code} url={self.url}, payload={self.payload}, payload={self.files}, result={text[0]}", color)


class ControlChain(ConnectSock):
    success_state = {
        "backup": "backup done",
        "restore": "success",
        "start": "started",
        "stop": "stopped",
        "import_stop": "import_icon finished"
    }

    def __init__(
            self,
            unix_socket="/app/goloop/data/cli.sock",
            url="/", cid=None, timeout=10,
            debug=False, auto_prepare=True, wait_state=True,
            increase_sec=0.5,
            wait_socket=False,
            logger=None,
            check_args=True,
            retry=3
    ):
        """
        ChainControl class init

        :param unix_socket: Path of file based unix domain socket
        :param url: reuqest url
        :param cid: channel id for goloop
        :param timeout: Maximum time in seconds that you allow the connection to the server to take
        :param debug: debug mode
        :param auto_prepare: Prepare before execution. e.g., Backup should be done after stopping.
        :param wait_state: Wait until the required state(success_state dict) is reached.
        """

        self.headers = {
            "Host": "*",
            "Accept": "*/*",
            "Content-Type": "application/json",
            "User-Agent": "socket-request"
        }

        super().__init__(unix_socket=unix_socket, timeout=timeout, debug=debug, headers=self.headers, wait_socket=wait_socket)
        self.url = url
        self.unix_socket = unix_socket
        self.cid = cid
        # self.action_model = ChainActionModel()

        self.payload = {}
        self.files = {}
        self.detail = False
        self.debug = debug
        self.auto_prepare = auto_prepare
        self.wait_state = wait_state
        self.state = {}
        self.gs_file = None
        self.increase_sec = increase_sec
        self.logger = logger
        self.check_args = check_args

        self.retry = retry

        self.last_block = {}

        self.logging(f"Load ControlChain Version={__version__}")

        if self.cid is None and self._health_check():
            self.debug_print("cid not found. Guess it will get the cid.")
            self.cid = self.guess_cid()
            self.debug_print(f"guess_cid = {self.cid}")

    # def _get_args_dict(fn, args, kwargs):
    #     args_names = fn.__code__.co_varnames[:fn.__code__.co_argcount]
    #     return {**dict(zip(args_names, args)), **kwargs}

    def logging(self, message=None, level="info"):
        if self.logger:
            if level == "info" and hasattr(self.logger, "info"):
                self.logger.info(f"[SR] {message}")
            elif level == "error" and hasattr(self.logger, "error"):
                self.logger.error(f"[SR] {message}")

    def _decorator_stop_start(func):
        def stop_start(self, *args, **kwargs):
            if self.auto_prepare:
                self.stop(*args, **kwargs)
                ret = func(self, *args, **kwargs)
                func_name = func.__name__
                if func_name == "restore":
                    exec_function = self.get_restore_status
                else:
                    exec_function = self.view_chain
                if self.wait_state and self.success_state.get(func_name):
                    wait_state_loop(
                        exec_function=exec_function,
                        check_key="state",
                        wait_state=self.success_state.get(func_name),
                        increase_sec=self.increase_sec,
                        description=f"'{func_name}'",
                        logger=self.logger
                    )
                self.start(*args, **kwargs)
            else:
                ret = func(self, **kwargs)
            return ret
        return stop_start

    def _decorator_wait_state(func):
        def wait_state(self, *args, **kwargs):
            func_name = func.__name__
            ret = func(self, *args, **kwargs)
            if self.wait_state and self.success_state.get(func_name):
                wait_state_loop(
                    exec_function=self.view_chain,
                    check_key="state",
                    wait_state=self.success_state.get(func_name),
                    increase_sec=self.increase_sec,
                    description=f"'{func_name}'",
                    logger=self.logger
                )
            return ret
        return wait_state

    def get_restore_status(self):
        return self.request(url="/system/restore",  method="GET", return_dict=True)

    def _decorator_kwargs_checker(check_mandatory=True):
        def real_deco(func):
            @wraps(func)
            def from_kwargs(self, *args, **kwargs):
                func_name = func.__name__
                if func_name != "stop_start":
                    self.debug_print(f"Start '{func_name}' function", "WHITE")
                    # color_print(f"['{func_name}'] Start function ", "WHITE")
                # defined default value for function

                if self.auto_prepare:
                    if func_name not in ["view_chain", "join"]:
                        self.view_chain()
                    if self.state.get("state") and self.success_state.get(func_name) == self.state.get("state"):
                        # print(red(f"Already {self.state.get('state')}"))
                        # return f"Already {self.state.get('state')}"
                        return ResponseField(status_code=202, text=f"Already {self.state.get('state')}")

                if check_mandatory is not True:
                    func_params = get_function_parameters(func)

                    # input parameters for function
                    func_params['kwargs'].update(**kwargs)
                    for key, value in func_params.get("kwargs").items():
                        if value is not None:
                            setattr(self, key, value)
                        default_param = getattr(self, key)

                        if (self.check_args and check_mandatory and True) and value is None and (default_param is None or default_param == {} or default_param == []):
                            raise Exception(red(f"Required '{key}' parameter for {func_name}()"))

                    self.debug_print(f"_decorator_kwargs_checker(), kwargs = {kwargs}")

                ret = func(self, *args, **kwargs)
                self.payload = {}
                self.files = []
                self.r_headers = []
                self.r_headers_string = ""
                self.r_body = []
                self.r_body_string = ""
                self.gs_file = ""
                return ret
            return from_kwargs
        # return real_deco
        return real_deco(check_mandatory) if callable(check_mandatory) else real_deco

    @_decorator_kwargs_checker(check_mandatory=False)
    def guess_cid(self):
        res = self.view_chain()
        if res.json and res.get_json("cid"):
            self.state = res.get_json()
            self.cid = res.get_json('cid')
            return self.cid

    @_decorator_kwargs_checker
    def _kwargs_test(self, cid=None):
        print(self.cid)

    def _is_cid(self, cid=None):
        if cid:
            self.cid = cid
        if self.cid:
            return self.cid
        else:
            print("[ERROR] Required cid")
            return False

    # def get_state(self):
    #     if self._health_check():
    #         res = self.view_chain().get_json()
    #         if isinstance(res, list) and len(res) == 0:
    #             self.state = {}
    #         else:
    #             self.state = res
    #     else:
    #         self.state = {
    #             "error": self.connect_error
    #         }
    #     return self.state

    def get_state(self):
        # res = self.view_chain().get_json()
        result = self.view_chain()
        if result.status_code == 200:
            res = self.view_chain().get_json()
            if isinstance(res, list) and len(res) == 0:
                self.state = {}
            else:
                self.state = res
                if self.state.get("cid"):
                    self.cid = self.state["cid"]
        else:
            self.state['error'] = result.text
        return self.state

    @_decorator_wait_state
    @_decorator_kwargs_checker
    def start(self, cid=None, **kwargs):
        if cid:
            self.cid = cid
        if self.cid is None:
            self.guess_cid()

        res = self.request(url=f"/chain/{self.cid}/start", payload={}, method="POST")
        return res

    @_decorator_wait_state
    @_decorator_kwargs_checker
    def stop(self, cid=None, **kwargs):
        if cid:
            self.cid = cid
        if self.cid is None:
            self.guess_cid()
        res = self.request(url=f"/chain/{self.cid}/stop", payload={}, method="POST")
        return res

    @_decorator_kwargs_checker
    def import_finish(self, cid=None, **kwargs):
        if cid:
            self.cid = cid
        if self.cid is None:
            self.guess_cid()

        stop_res_1 = None
        stop_res_2 = None

        try:
            stop_res_1 = self.import_stop()
            time.sleep(3)
            stop_res_2 = self.stop()
            time.sleep(3)
            if stop_res_1.status_code == 200 and stop_res_2.status_code == 200:
                color_print("Congrats! Successfully imported")
                color_print(f"{self.get_state()}")
            else:
                color_print(f"[FAIL] stop_res_1={stop_res_1}, stop_res_2={stop_res_2}", "red")
        except Exception as e:
            color_print(f"{self.get_state()}, e={e}")
        return stop_res_2

    @_decorator_wait_state
    @_decorator_kwargs_checker
    def import_stop(self, cid=None, **kwargs):
        if cid:
            self.cid = cid
        if self.cid is None:
            self.guess_cid()

        res = self.request(url=f"/chain/{self.cid}/stop", payload={}, method="POST")
        return res

    @_decorator_kwargs_checker
    def reset(self, cid=None):
        if cid:
            self.cid = cid
        if self.cid is None:
            self.guess_cid()

        self.stop(cid)
        res = self.request(url=f"/chain/{self.cid}/reset", payload={}, method="POST")
        return res

    def import_icon(self, payload=None):
        res = self.request(
            url=f"/chain/{self.cid}/import_icon",
            payload=payload,
            method="POST",
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        self.guess_cid()
        return res

    @_decorator_kwargs_checker
    def join(self,
             seedAddress=[],
             role=3,
             maxBlockTxBytes=2048000,
             normalTxPool=10000,
             channel="icon_dex",
             autoStart=True,
             platform="icon",
             gs_file="config/icon_genesis.zip",
             dbType="rocksdb",
             txTimeout=60000,
             nodeCache="small"
             ):

        config_payload = dict(
            seedAddress=",".join(seedAddress),
            role=int(role),
            maxBlockTxBytes=int(maxBlockTxBytes),
            normalTxPool=int(normalTxPool),
            channel=channel,
            autoStart=autoStart,
            platform=platform,
            dbType=dbType,
            txTimeout=int(txTimeout),
            nodeCache=nodeCache
        )

        if not seedAddress:
            raise Exception(red(f"[ERROR] seedAddress is None"))

        if not os.path.exists(self.gs_file):
            raise Exception(red(f"[ERROR] Genesis file not found - '{gs_file}'"))

        with open(gs_file, "rb") as genesis_fd:
            fd_data = genesis_fd.read()

        files = {
            "json": (None, json.dumps(config_payload)),
            "genesisZip": (os.path.basename(gs_file), fd_data)
        }

        res = self.request(url=f"/chain", payload={}, method="POST", files=files)
        self.guess_cid()
        debug(res.status_code)
        return res
        # else:
        #     print(f"[ERROR] Required files")

    # @_decorator_kwargs_checker
    def leave(self, cid=None):
        if cid:
            self.cid = cid
        if self.cid is None:
            self.guess_cid()

        if self.cid is None:
            return ResponseField(status_code=400, text=f"Already leave, cid not found")

        res = self.request(url=f"/chain/{self.cid}", payload={}, method="delete")
        return res

    @_decorator_kwargs_checker
    @_decorator_stop_start
    def backup(self, cid=None):
        res = self.request(url=f"/chain/{self.cid}/backup", payload={}, method="POST")
        return res

    @_decorator_kwargs_checker
    def backup_list(self, cid=None):
        res = self.request(url=f"/system/backup", payload={}, method="GET")
        return res

    @_decorator_kwargs_checker
    @_decorator_stop_start
    def restore(self, name=None, cid=None):
        payload = {
            "name": name,
            "overwrite": True
        }
        res = self.request(url=f"/system/restore", payload=payload, method="POST")
        return res

    # @_decorator_kwargs_checker
    def view_chain(self, cid=None, detail=False, inspect=False):
        payload = {}
        if cid:
            self.cid = cid

        if self.cid and inspect:
            url = f"/chain/{self.cid}"
            # payload = {"informal": "true"}
        elif self.cid and detail:
            url = f"/chain/{self.cid}/configure"
        else:
            url = f"/chain"
        res = self.request(url=url, payload=payload, method="GET", return_dict=True)

        if res.status_code != 200:
            self.logging(f"view_chain res.status_code={res.status_code}, res = {res.text}")
        if hasattr(res, 'json'):
            self.state = res.json
            try:
                self.get_tps()
                res.set_dict(self.state)
            except:
                pass
            # self.connect_error = res.get('error')
        else:
            self.state = {}
            self.connect_error = res.text
        return res

    def get_tps(self):
        if self.state.get("height"):
            if self.last_block.get('height') is None:
                self.last_block = {
                    "height": self.state.get("height"),
                    "time": time.time()
                }

            diff_block = self.state['height'] - self.last_block['height']
            diff_time = time.time() - self.last_block['time']
            tps = diff_block / diff_time
            # print(diff_block, diff_time, tps)
            self.state['tps'] = round(tps)
            self.last_block = {
                "height": self.state.get("height"),
                "time": time.time()
            }

    @_decorator_kwargs_checker
    @_decorator_stop_start
    def chain_config(self, payload=None):
        # payload = _payload_bool2string(payload)

        # res = self.request(url=f"/chain/{self.cid}/configure", payload=payload,  method="POST")
        result = {
            "state": "OK",
            "payload": payload,
            "error": []
        }

        status_code = 201

        if not isinstance(payload, dict):
            raise Exception(red(f"[ERROR] Invalid payload '{payload}'"))

        for key, value in payload.items():

            if isinstance(value, bool):
                value = bool2str(value)
            elif isinstance(value, int):
                value = str(value)
            elif isinstance(value, float):
                value = str(value)

            debug(key, value) if self.debug else False
            each_payload = {"key": key, "value": value}
            res = self.request(url=f"/chain/{self.cid}/configure", payload=each_payload,  method="POST")
            debug(res) if self.debug else False

            if res.status_code != 200:
                if len(res.text) > 1:
                    return_text = res.text.split("\n")[0]
                else:
                    return_text = res.text
                result['error'].append({
                    "key": key,
                    "value": value,
                    "message": return_text
                })
                result['state'] = "FAIL"
                status_code = 400

        return ResponseField(status_code=status_code, text=result)
        # return result

    def view_system_config(self, detail=True):
        if detail:
            url = "/system"
        else:
            url = "/system/configure"
        res = self.request(url=url,  method="GET")
        return res

    @_decorator_kwargs_checker
    def system_config(self, payload=None):
        payload = _payload_bool2string(payload)
        res = self.request(url="/system/configure",  payload=payload, method="POST")
        return res


class DockerSock(ConnectSock):
    def __init__(self, unix_socket="/var/run/docker.sock", url="/", timeout=5, debug=False, auto_prepare=False, wait_state=False):
        super().__init__(unix_socket=unix_socket, timeout=timeout, debug=debug)
        self.url = url
        self.unix_socket = unix_socket
        # self.action_model = ChainActionModel()
        self.headers = {
            "Host": "*",
            "Accept": "*/*",
            "Content-Type": "application/json",
            "User-Agent": "socket-request"
        }
        self.payload = {}
        self.files = {}
        self.detail = False
        self.debug = debug
        self.simple_name = True
        self.auto_prepare = auto_prepare
        self.wait_state = wait_state

    def get_docker_images(self, return_type="each", simple_name=True):
        self.request(url="/containers/json")
        self.simple_name = simple_name
        return_values = []
        if self.Response.json:
            for image in self.Response.json:
                return_values.append(dict(
                    # names=image.get("Names")[0][1:],
                    images=image.get("Image"),
                    state=image.get("State"),
                    status=image.get("Status")
                ))

        if return_type == "merge" and len(return_values) > 0:
            self.return_merged_values = {key: "" for key in return_values[0].keys()}
            for values in return_values:
                for r_key, r_val in values.items():
                    self._merge_value(r_key, self.get_simple_image_name(r_val))
            return self.return_merged_values

        return return_values

    def get_simple_image_name(self, name):
        if self.simple_name:
            if "/" in name:
                name_arr = name.split("/")
                return name_arr[-1]
        return name

    def _merge_value(self, key, value, separator="|"):
        # jmon_lib.cprint(self.return_merged_values.get(key))
        prev_value = self.return_merged_values.get(key)
        if prev_value:
            self.return_merged_values[key] = f"{prev_value}{separator}{value}"
        else:
            self.return_merged_values[key] = f"{value}"


class RequestField(object):
    """
    A data container for request body parameters.

    :param name:
        The name of this request field. Must be unicode.
    :param data:
        The data/value body.
    :param filename:
        An optional filename of the request field. Must be unicode.
    :param headers:
        An optional dict-like object of headers to initially use for the field.
    """

    def __init__(
            self,
            name,
            data,
            filename=None,
            headers=None,
    ):
        self._name = name
        self._filename = filename
        self.data = data
        self.headers = {}
        if headers:
            self.headers = dict(headers)

    @classmethod
    def from_tuples(cls, fieldname, value):
        """
        A :class:`~urllib3.fields.RequestField` factory from old-style tuple parameters.

        Supports constructing :class:`~urllib3.fields.RequestField` from
        parameter of key/value strings AND key/filetuple. A filetuple is a
        (filename, data, MIME type) tuple where the MIME type is optional.
        For example::

            'foo': 'bar',
            'fakefile': ('foofile.txt', 'contents of foofile'),
            'realfile': ('barfile.txt', open('realfile').read()),
            'typedfile': ('bazfile.bin', open('bazfile').read(), 'image/jpeg'),
            'nonamefile': 'contents of nonamefile field',

        Field names and filenames must be unicode.
        """
        if isinstance(value, tuple):
            if len(value) == 3:
                filename, data, content_type = value
            else:
                filename, data = value
                content_type = _guess_content_type(filename)
        else:
            filename = None
            content_type = None
            data = value

        request_param = cls(
            fieldname, data, filename=filename,
        )
        request_param.make_multipart(content_type=content_type)

        return request_param

    def _render_part(self, name, value):
        """
        Overridable helper function to format a single header parameter. By
        default, this calls ``self.header_formatter``.

        :param name:
            The name of the parameter, a string expected to be ASCII only.
        :param value:
            The value of the parameter, provided as a unicode string.
        """

        # return self.header_formatter(name, value)
        return u'%s="%s"' % (name, value)

    def _render_parts(self, header_parts):
        """
        Helper function to format and quote a single header.

        Useful for single headers that are composed of multiple items. E.g.,
        'Content-Disposition' fields.

        :param header_parts:
            A sequence of (k, v) tuples or a :class:`dict` of (k, v) to format
            as `k1="v1"; k2="v2"; ...`.
        """
        parts = []
        iterable = header_parts
        if isinstance(header_parts, dict):
            iterable = header_parts.items()

        for name, value in iterable:
            if value is not None:
                parts.append(self._render_part(name, value))

        return u"; ".join(parts)

    def render_headers(self):
        """
        Renders the headers for this request field.
        """

        lines = []

        sort_keys = ["Content-Disposition", "Content-Type", "Content-Location"]
        for sort_key in sort_keys:
            if self.headers.get(sort_key, False):
                lines.append(u"%s: %s" % (sort_key, self.headers[sort_key]))

        for header_name, header_value in self.headers.items():
            if header_name not in sort_keys:
                if header_value:
                    lines.append(u"%s: %s" % (header_name, header_value))

        lines.append(u"\r\n")
        return u"\r\n".join(lines)

    def make_multipart(
            self, content_disposition=None, content_type=None, content_location=None
    ):
        """
        Makes this request field into a multipart request field.

        This method overrides "Content-Disposition", "Content-Type" and
        "Content-Location" headers to the request parameter.

        :param content_type:
            The 'Content-Type' of the request body.
        :param content_location:
            The 'Content-Location' of the request body.

        """
        self.headers["Content-Disposition"] = content_disposition or u"form-data"
        self.headers["Content-Disposition"] += u"; ".join(
            [
                u"",
                self._render_parts(
                    ((u"name", self._name), (u"filename", self._filename))
                ),
            ]
        )
        self.headers["Content-Type"] = content_type
        self.headers["Content-Location"] = content_location


def b(s):
    return s.encode("latin-1")


def iteritems(d, **kw):
    return iter(d.items(**kw))


def _append_new_line(data, check_string="\r\n"):
    if data.endswith(check_string) is False:
        return f"{data}{check_string}"


def choose_boundary():
    return binascii.hexlify(os.urandom(16)).decode("ascii")


def _iter_field_objects(fields):
    """
    Iterate over fields.

    Supports list of (k, v) tuples and dicts, and lists of
    :class:`~urllib3.fields.RequestField`.

    """
    if isinstance(fields, dict):
        i = iteritems(fields)
    else:
        i = iter(fields)

    for field in i:
        if isinstance(field, RequestField):
            yield field
        else:
            yield RequestField.from_tuples(*field)


def _guess_content_type(filename, default="application/octet-stream"):
    """
    Guess the "Content-Type" of a file.

    :param filename:
        The filename to guess the "Content-Type" of using :mod:`mimetypes`.
    :param default:
        If no "Content-Type" can be guessed, default to `default`.
    """
    if filename:
        return mimetypes.guess_type(filename)[0] or default
    return default


def _replace_multiple(value, needles_and_replacements):
    def replacer(match):
        return needles_and_replacements[match.group(0)]

    pattern = re.compile(
        r"|".join([re.escape(needle) for needle in needles_and_replacements.keys()])
    )

    result = pattern.sub(replacer, value)

    return result


def wait_state_loop(
        exec_function=None,
        func_args=[],
        check_key="status",
        wait_state="0x1",
        timeout_limit=30,
        increase_sec=0.5,
        health_status=None,
        description="",
        force_dict=True,
        logger=None
):
    start_time = time.time()
    count = 0
    # arguments 가 한개만 있을 때의 예외
    # if type(func_args) is str:
    if isinstance(func_args, str):
        tmp_args = ()
        tmp_args = tmp_args + (func_args,)
        func_args = tmp_args

    exec_function_name = exec_function.__name__
    # classdump(exec_function.__qualname__)
    # print(exec_function.__qualname__)
    act_desc = f"desc={description}, function={exec_function_name}, args={func_args}"
    spinner = Halo(text=f"[START] Wait for {description} , {exec_function_name}, {func_args}", spinner='dots')
    if logger and hasattr(logger, "info"):
        logger.info(f"[SR] [START] {act_desc}")

    spinner.start()

    while True:
        if isinstance(func_args, dict):
            response = exec_function(**func_args)
        else:
            response = exec_function(*func_args)

        if not isinstance(response, dict):
            response = response.__dict__

        if force_dict:
            if isinstance(response.get("json"), list):
                response['json'] = response['json'][0]

        check_state = ""
        error_msg = ""

        if response.get("json") or health_status:
            response_result = response.get("json")
            check_state = response_result.get(check_key, "")
            response_status = response.get("status_code")
            if check_state == wait_state or health_status == response_status:
                status_header = bcolors.OKGREEN + "[DONE]" + bcolors.ENDC
                text = f"\t[{description}] count={count}, func={exec_function_name}, args={str(func_args)[:30]}, wait_state='{wait_state}', check_state='{check_state}'"
                if health_status:
                    text += f", health_status={health_status}, status={response_status}"
                spinner.succeed(f'{status_header} {text}')
                spinner.stop()
                spinner.clear()
                # spinner.stop_and_persist(symbol='🦄'.encode('utf-8'), text="[DONE]")
                break
            else:
                if type(response_result) == dict or type(check_state) == dict:
                    if response_result.get("failure"):
                        if response_result.get("failure").get("message"):
                            print("\n\n\n")
                            spinner.fail(f'[FAIL] {response_result.get("failure").get("message")}')
                            spinner.stop()
                            spinner.clear()
                            break

        text = f"[{count:.1f}s] Waiting for {exec_function_name} / {func_args} :: '{wait_state}' -> '{check_state}' , {error_msg}"
        spinner.start(text=text)

        if logger and hasattr(logger, "info"):
            logger.info(f"[SR] {text}")

        try:
            assert time.time() < start_time + timeout_limit
        except AssertionError:
            text = f"[{count:.1f}s] [{timeout_limit}s Timeout] Waiting for {exec_function_name} / '{func_args}' :: '{wait_state}' -> {check_state} , {error_msg}"
            spinner.start(text=text)

            if logger and hasattr(logger, "error"):
                logger.info(f"[SR] {text}")

        count = count + increase_sec
        time.sleep(increase_sec)

        spinner.stop()

    if logger and hasattr(logger, "info"):
        logger.info(f"[SR] [DONE] {act_desc}")

    if health_status:
        return response

    # return {
    #     "elapsed": time.time() - start_time,
    #     "json": response.get("json"),
    #     "status_code": response.get("status_code", 0),
    # }


def get_function_parameters(func=None):
    if func:
        keys = func.__code__.co_varnames[:func.__code__.co_argcount][::-1]
        sorter = {j: i for i, j in enumerate(keys[::-1])}
        if func.__defaults__ is None:
            func.__defaults__ = ()
        values = func.__defaults__[::-1]
        kwargs = {i: j for i, j in zip(keys, values)}
        sorted_args = tuple(
            sorted([i for i in keys if i not in kwargs], key=sorter.get)
        )
        sorted_kwargs = {
            i: kwargs[i] for i in sorted(kwargs.keys(), key=sorter.get)
        }
        return {
            "args": sorted_args,
            "kwargs": sorted_kwargs
        }
    else:
        return {}


def _payload_bool2string(payload=None):
    """
    In goloop, boolean values ​​must be string.
    :param payload:
    :return:
    """
    if payload and isinstance(payload, dict):
        for k, v in payload.items():
            payload[k] = bool2str(v)
    return payload


def bool2str(v):
    if type(v) == bool:
        if v:
            return "true"
        elif v:
            return "false"

        else:
            return "false"
    else:
        return v


def str2bool(v):
    if v is None:
        return False
    elif type(v) == bool:
        return v
    if v.lower() in ('yes', 'true',  't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        return False


class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    OKGREEN = '\033[92m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[97m'


def get_bcolors(text, color, bold=False, width=None):
    if width and len(text) <= width:
        text = text.center(width, ' ')
    return_text = f"{getattr(bcolors, color)}{text}{bcolors.ENDC}"
    if bold:
        return_text = f"{bcolors.BOLD}{return_text}"
    return str(return_text)


def classdump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            value = getattr(obj, attr)
            print(bcolors.GREEN + f"obj.{attr} = " + bcolors.WARNING + f"{value}" + bcolors.ENDC)


def color_print(text, color="GREEN", date=True, **kwargs):
    date_string = ""
    if date:
        date_string = todaydate("ms")
    if isinstance(text, dict) or isinstance(text,list):
        text = str(text)

    print(f"{get_bcolors(date_string +' '+ text, color.upper())}", **kwargs)


def red(text):
    return get_bcolors(f"{text}", "FAIL")


def todaydate(type=None):
    if type is None:
        return '%s' % datetime.now().strftime("%Y%m%d")
    elif type == "ms":
        return '[%s]' % datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    elif type == "ms_text":
        return '%s' % datetime.now().strftime("%Y%m%d-%H%M%S%f")[:-3]


class Table:
    def __init__(self, title, headers, rows, view_header=True):
        title = bcolors.WARNING + title + bcolors.ENDC
        self.title = title
        self.headers = headers
        self.rows = rows
        self.view_header = view_header
        self.nrows = len(self.rows)
        self.fieldlen = []

        self.warn_string = ["stopped","unused"]
        self.ok_string = ["running"]

        ncols = len(headers)

        for i in range(ncols):
            max = 0
            for j in rows:
                if len(str(j[i])) > max:
                    max = len(str(j[i]))
            self.fieldlen.append(max)

        for i in range(len(headers)):
            if len(str(headers[i])) > self.fieldlen[i]:
                self.fieldlen[i] = len(str(headers[i]))

        self.width = sum(self.fieldlen)+(ncols-1)*3+4

    def __str__(self):
        bar = "-"*self.width
        # title = "| "+self.title+" "*(self.width-3-(len(self.title)))+"|"
        title = "| "+self.title+" "*(self.width+6-(len(self.title)))+"|"
        out = [bar, title, bar]
        header = ""
        for i in range(len(self.headers)):
            header += "| %s" % (str(self.headers[i])) + " " * \
                      (self.fieldlen[i]-len(str(self.headers[i])))+" "
        header += "|"

        if self.view_header:
            out.append(header)
            out.append(bar)
        for i in self.rows:
            line = ""
            for j in range(len(i)):
                column = str(i[j])
                # for item in self.warn_string:
                #     if (line.find(item)) != -1:
                # column = bcolors.FAIL + column + bcolors.ENDC

                # for item in self.warn_string:
                #     if (item.find(item)) != -1:
                #         column = bcolors.FAIL + column + bcolors.ENDC
                #         is_warn_string = 1

                # for item in self.ok_string:
                #     if (line.find(item)) != -1:
                #         is_ok_string = 1


                # if intersection(i, self.warn_string):
                #     column = bcolors.FAIL + column + bcolors.ENDC
                # if intersection(i, self.ok_string):
                #     column = bcolors.OKGREEN + column + bcolors.ENDC

                line += "| %s" % (column) + " " * \
                        (self.fieldlen[j]-len(column))+" "

            for item in self.warn_string:
                if (line.find(item)) != -1:
                    line = bcolors.FAIL + line + bcolors.ENDC
            for item in self.ok_string:
                if (line.find(item)) != -1:
                    line = bcolors.OKGREEN + line + bcolors.ENDC

            out.append(line+"|")
        out.append(bar)
        return "\r\n".join(out)


def minimize_names(object_dict):
    replace_dest = {
        "consensus_height": "bh",
        "duration": "d",
        "network": "net",
        "txlatency_commit": "tx_com",
        "txlatency_finalize": "tx_fin",
        "txpool": "tx",
        "user": "usr",
        "consensus_round": "c_rnd"
    }
    new_dict = {}
    if isinstance(object_dict, dict):
        for key, value in object_dict.items():
            new_key = key
            for k2, v2 in replace_dest.items():
                if k2 in key:
                    new_key = new_key.replace(k2, v2)
            new_dict[new_key] = value
            print(new_key, value)
        return new_dict
    else:
        return object_dict


def print_table(title, source_dict=None, view_header=True, vertical=False):
    rows = []
    columns = []
    source_dict = minimize_names(source_dict)
    try:
        source_input = source_dict.keys()
        columns = list(source_input)
        print(columns)
        is_dict = 1
    except:
        source_input = source_dict
        is_dict = 0
    index = 0
    for item in source_input:
        if is_dict:
            columns_list = [source_dict.get(col, None) for col in columns]
        else:
            columns_list = [item.get(col, None) for col in columns]
        index += 1
        columns_list.insert(0, index)
        rows.append(columns_list)
        if is_dict:
            break

    columns.insert(0, "idx")
    print(Table(title, columns, rows, view_header))


def is_hex(s):
    try:
        int(s, 16)
        return True
    except:
        return False


def dump(obj, nested_level=0, output=sys.stdout, hex_to_int=False):
    spacing = '   '
    def_spacing = '   '
    if type(obj) == dict:
        print('%s{' % (def_spacing + (nested_level) * spacing))
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print(bcolors.OKGREEN + '%s%s:' % (def_spacing + (nested_level + 1) * spacing, k) + bcolors.ENDC, end="")
                dump(v, nested_level + 1, output, hex_to_int)
            else:
                # print >>  bcolors.OKGREEN + '%s%s: %s' % ( (nested_level + 1) * spacing, k, v) + bcolors.ENDC
                print(bcolors.OKGREEN + '%s%s:' % (def_spacing + (nested_level + 1) * spacing, k) + bcolors.WARNING + ' %s' % v + bcolors.ENDC,
                      file=output)
        print('%s}' % (def_spacing + nested_level * spacing), file=output)
    elif type(obj) == list:
        print('%s[' % (def_spacing + (nested_level) * spacing), file=output)
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v, nested_level + 1, output, hex_to_int)
            else:
                print(bcolors.WARNING + '%s%s' % (def_spacing + (nested_level + 1) * spacing, v) + bcolors.ENDC, file=output)
        print('%s]' % (def_spacing + (nested_level) * spacing), file=output)
    else:
        if hex_to_int and is_hex(obj):
            print(bcolors.WARNING + '%s%s' % (def_spacing + nested_level * spacing, str(round(int(obj, 16)/10**18, 8)) + bcolors.ENDC))
        else:
            print(bcolors.WARNING + '%s%s' % (def_spacing + nested_level * spacing, obj) + bcolors.ENDC)
