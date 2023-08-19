import random
import string

import pytest
from checkout import ssh_checkout
from sshcheckers import ssh_checkout


folder_in = "/home/user/tst/file"
folder_out = "/home/user/tst/out"
folder_ext = "/home/user/tst/ext"
folder_badarx = "/home/user/tst/badarx"


@pytest.fixture()
def make_folders():
    return ssh_checkout(data["host"], data["user2"], "1111","mkdir {} {} {} {}".format(folder_in, folder_out, folder_ext, folder_badarx), "")


@pytest.fixture()
def clear_folders():
    return ssh_checkout(data["host"], data["user2"], "1111","rm -rf {}/* {}/* {}/* {}/*".format(folder_in, folder_out, folder_ext, folder_badarx), "")


@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(5):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(data["host"], data["user2"], "1111",
                "cd {}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(folder_in, filename),
                ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(data["host"], data["user2"], "1111","cd {}; mkdir {}".format(folder_in, subfoldername), ""):
        return None, None
    if not ssh_checkout(data["host"], data["user2"], "1111",
            "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(folder_in, subfoldername,
                                                                                      testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture()
def make_badarx():
    ssh_checkout(data["host"], data["user2"], "1111","cd {}; 7z a {}/badarx.7z".format(folder_in, folder_badarx), "Everything is Ok"), "Test1 Fail"
    ssh_checkout(data["host"], data["user2"], "1111","truncate -s 1 {}/badarx.7z".format(folder_badarx), "Everything is Ok"), "Test1 Fail"
    yield "badarx"
    ssh_checkout(data["host"], data["user2"], "1111","rm -f {}/badarx.7z".format(folder_badarx), "")
