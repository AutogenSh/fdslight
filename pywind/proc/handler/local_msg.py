#!/usr/bin/env python3
"""本地进程消息"""

import pywind.evtframework.handler.tcp_handler as tcp_handler
import pywind.proc.lib.msg_socket as msg_socket
import socket


class _msgs(tcp_handler.tcp_handler):
    def init_func(self, fileno, cs, address):
        cs = msg_socket.wrap_socket(cs)

        self.set_socket(cs)
        self.register(self.fileno)
        self.add_evt_read(self.fileno)

    def msg_readable(self, message):
        """重写这个方法"""
        pass

    def tcp_readable(self):
        pass


class msgd(tcp_handler.tcp_handler):
    """本地进程消息服务端"""

    def init_func(self, fileno, addr_family, address):
        s = socket.socket(addr_family, socket.SOCK_STREAM)
        s = msg_socket.wrap_socket(s)

        self.set_socket(s)
        self.bind(address)

    def after(self):
        self.listen(10)
        self.register(self.fileno)
        self.add_evt_read(self.fileno)

    def tcp_accept(self):
        pass


class msgc(tcp_handler.tcp_handler):
    """本地进程消息客户端"""

    def init_func(self, fileno, addr_family, address):
        s = socket.socket(addr_family, socket.SOCK_STREAM)
        s = msg_socket.wrap_socket(s)

        self.set_socket(s)
        self.connect(address, 5)

    def connect_ok(self):
        self.register(self.fileno)
        self.add_evt_read(self.fileno)

    def tcp_timeout(self):
        if not self.is_conn_ok():
            self.delete_handler(self.fileno)
            return
        self.set_timeout(self.fileno, 10)

    def msg_readable(self, message):
        """重写这个方法"""
        pass
