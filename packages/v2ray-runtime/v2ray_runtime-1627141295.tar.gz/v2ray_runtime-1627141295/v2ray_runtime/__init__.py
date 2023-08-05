import sys
import subprocess


def GetCurrentOS():
    temp = sys.platform
    if temp == 'win32':
        return 'Windows'
    if temp == 'cygwin':
        return 'Cygwin'
    if temp == 'darwin':
        return 'Mac'
    return 'Linux'


if GetCurrentOS() == 'Windows':
    install = 'v2ray_runtime_windows'
    uninstall = 'v2ray_runtime_linux'
else:
    install = 'v2ray_runtime_linux'
    uninstall = 'v2ray_runtime_windows'

subprocess.Popen("pip3 uninstall %s" % (uninstall), shell=True).wait()
subprocess.Popen("pip3 install --upgrade %s" % (install), shell=True).wait()
import v2ray

V2RAY_RUNTIME_DIR = v2ray.V2RAY_RUNTIME_DIR
V2RAY_RUNTIME_NAME = v2ray.V2RAY_RUNTIME_NAME
V2RAY_RUNTIME_PATH = v2ray.V2RAY_RUNTIME_PATH
