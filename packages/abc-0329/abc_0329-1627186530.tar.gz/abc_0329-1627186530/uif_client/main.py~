import subprocess
import sys
import os
import time

import fire
import psutil
import v2ray_runtime
import caddy_runtime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = BASE_DIR.replace('\\', '/')


def GetCurrentOS():
    temp = sys.platform
    if temp == 'win32':
        return 'Windows'
    if temp == 'cygwin':
        return 'Cygwin'
    if temp == 'darwin':
        return 'Mac'
    return 'Linux'


def DoCMD(cmd, is_wait=True):
    print('\n\n==', cmd, '\n')
    if is_wait:
        subprocess.Popen(cmd, shell=True).wait()
    else:
        subprocess.Popen(cmd, shell=True)


def Log(msg):
    print(msg)


def IsProcessExist(name):
    pids = psutil.pids()
    for pid in pids:
        try:
            p = psutil.Process(pid)
            temp = p.name()
            if name == temp:
                return p
        except Exception as e:
            pass
    # Log("process '%s' is not exist." % (name))
    return False


class UIFClient(object):
    def Run(self, use_cloudfare=False, domain=None, with_free_port=True):
        if use_cloudfare is True and domain is None:
            raise ValueError('Need domain to enable cloudfare.')

        is_v2ray_running = IsProcessExist(v2ray_runtime.V2RAY_RUNTIME_NAME)
        is_caddy_running = IsProcessExist(caddy_runtime.CADDY_RUNTIME_NAME)

        if is_v2ray_running:
            Log('v2ray_running')
            is_v2ray_running.kill()
        if is_caddy_running:
            Log('caddy_running')
            is_caddy_running.kill()

        DoCMD('fuser -k -n tcp 80')  # for linux

        if with_free_port is False:
            caddy_config_file_path = BASE_DIR + '/caddy_config/tls_ws.txt'
        else:
            caddy_config_file_path = BASE_DIR + '/caddy_config/tls_ws_with_free.txt'

        v2ray_config_file_path = BASE_DIR + '/v2ray_config/default.json'

        # run v2ray first
        DoCMD('%s -config "%s"' %
              (v2ray_runtime.V2RAY_RUNTIME_PATH, caddy_config_file_path),
              is_wait=False)

        time.sleep(5)

        DoCMD('%s run -config "%s" -adapter caddyfile' %
              (caddy_runtime.CADDY_RUNTIME_PATH, caddy_config_file_path),
              is_wait=False)

    def Stop(self):
        pass

    def Restart(self):
        if use_cloudfare is False and domain is None:
            raise ValueError('Need domain to enable cloudfare.')


def Main():
    if GetCurrentOS() == 'Linux':
        cmd = "sudo chmod -R 750 " + BASE_DIR
        DoCMD(cmd)
        cmd = "sudo chmod -R 750 " + caddy_runtime.CADDY_RUNTIME_DIR
        DoCMD(cmd)
        cmd = "sudo chmod -R 750 " + v2ray_runtime.V2RAY_RUNTIME_DIR
        DoCMD(cmd)
    fire.Fire(UIFClient)


if __name__ == '__main__':
    Main()
