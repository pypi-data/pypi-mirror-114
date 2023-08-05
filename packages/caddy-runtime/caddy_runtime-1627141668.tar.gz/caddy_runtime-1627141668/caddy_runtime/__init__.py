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
    install = 'caddy_runtime_windows'
    uninstall = 'caddy_runtime_linux'
else:
    install = 'caddy_runtime_linux'
    uninstall = 'caddy_runtime_windows'

subprocess.Popen("pip3 uninstall %s" % (uninstall), shell=True).wait()
subprocess.Popen("pip3 install --upgrade %s" % (install), shell=True).wait()
import caddy

CADDY_RUNTIME_DIR = caddy.CADDY_RUNTIME_DIR
CADDY_RUNTIME_NAME = caddy.CADDY_RUNTIME_NAME
CADDY_RUNTIME_PATH = caddy.CADDY_RUNTIME_PATH
