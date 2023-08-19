
аrom checkout import ssh_checkout
from sshcheckers import ssh_checkout, upload_files
import yaml

with open('config.yaml') as f:
    # читаем документ YAML
    data = yaml.safe_load(f)


def test_step0():
    res = []
    upload_files(data["host"], data["user2"], "1111", "{}/p7zip-full.deb".format(data["local_path"]), '{}/p7zip-full.deb'.format(data["remote_path"]))
    res.append(ssh_checkout(data["host"], data["user2"], "1111", "echo '1111' | sudo -S dpkg -i  {}/p7zip-full.deb".format(data["remote_path"], "Настраивается пакет")))
    res.append(ssh_checkout(data["host"], data["user2"], "1111", "echo '1111' | sudo -S dpkg -s p7zip-full", "Status: install ok installed"))
    assert all(res)


def test_step1(make_folders, clear_folders, make_files):
    # test1
    res1 = ssh_checkout(data["host"], data["user2"],"1111","cd {}; 7z a {}/arx1.7z".format([folder_in], [folder_out]), "Everything is Ok"), "Test1 Fail"
    res2 = ssh_checkout(data["host"], data["user2"],"1111","ls {}".format(folder_out), "arx1.7z"), "Test1 Fail"
    assert res1 and res2, "Test Fail"


def test_step2(clear_folders, make_files):
    # test2
    res = []
    res.append(ssh_checkout(data["host"], data["user2"],"1111","cd {}; 7z a {}/arx1.7z".format(folder_in, folder_out), "Everything is Ok"))
    res.append(ssh_checkout(data["host"], data["user2"],"1111","cd {}; 7z e arx1.7z -o{} -y".format(folder_out, folder_ext), "Everything is Ok"))
    for item in make_files:
        res.append(ssh_checkout(data["host"], data["user2"],"1111","ls {}".format(folder_ext), item))
    assert all(res)


def test_step3():
    # test3
    assert ssh_checkout(data["host"], data["user2"],"1111","cd {}; 7z t {}/arx1.7z".format(folder_in, folder_out), "Everything is Ok"), "Test1 Fail"


def test_step4():
    # test4
    assert ssh_checkout(data["host"], data["user2"],"1111","cd {}; 7z u {}/arx1.7z".format(folder_in, folder_out), "Everything is Ok"), "Test1 Fail"


def test_step5(clear_folders, make_files):
    # test5
    res = []
    res.append(ssh_checkout(data["host"], data["user2"],"1111","cd {}; 7z a {}/arx1.7z".format(folder_in, folder_out), "Everything is Ok"))
    for item in make_files:
        res.append(ssh_checkout(data["host"], data["user2"],"1111","cd {}; 7z l arx1.7z".format(folder_out), item))
    assert all(res)


def test_step6():
    # test6
    res = []
    res.append(checkout(data["host"], data["user2"],"1111","cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]),
                        "Everything is Ok"))
    res.append(checkout(data["host"], data["user2"],"1111","cd {}; 7z x arx.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext2"]),
                        "Everything is Ok"))
    for i in make_files:
        res.append(checkout(data["host"], data["user2"],"1111","ls {}".format(data["folder_ext2"]), i))
    res.append(checkout(data["host"], data["user2"],"1111","ls {}".format(data["folder_ext2"]), make_subfolder[0]))
    res.append(checkout(data["host"], data["user2"],"1111","ls {}/{}".format(data["folder_ext2"], make_subfolder[0]), make_subfolder[1]))
    assert all(res), "test6 FAIL"


def test_step7():
    assert ssh_checkout(data["host"], data["user2"],"1111","7z d {}/arx1.7z".format(folder_out), "Everything is Ok"), "Test1 Fail"
