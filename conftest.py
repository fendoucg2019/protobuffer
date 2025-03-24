#coding=utf-8
import pytest
import socket

@pytest.fixture(scope="session")
def cons():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('120.76.138.211',19999))
    yield s
    s.close()
