import os
import requests
import subprocess
import sys
import tempfile
import time


class SmartbearTunnel:
    def __init__(self, username=None, authkey=None, options={}):
        if username is None and 'SMARTBEAR_USERNAME' in os.environ:
            self.username = os.environ['SMARTBEAR_USERNAME']
        else:
            self.username = username

        if authkey is None and 'SMARTBEAR_AUTHKEY' in os.environ:
            self.authkey = os.environ['SMARTBEAR_AUTHKEY']
        else:
            self.authkey = authkey

        if not (self.username and self.authkey):
            raise Exception('Must supply Smartbear username and authorization key.')

        if 'tunnel_path' in options:
            self.tunnel_binary_path = options['tunnel_path']
        else:
            self.tunnel_binary_path = self._download_binary()

        # defaults
        self.domain = 'app.crossbrowsertesting.com'
        self.tunnel_id = None
        self.tunnel_process = None
        self.proxyOptions = {}
        self.tunnel_type = 'internal-websites'
        self.tunnel_name = None
        self.bypass = True
        self.verbose = False
        self.accept_all_certs = False

        # apply options from user
        self._apply_options(options)

        # store requested options if needed
        self.requested_options = options

    def _apply_options(self, options):
        if 'directory' in options:
            self.tunnel_type = 'local-html-files'
        elif 'proxyIp' in options and 'proxyPort' in options:
            self.tunnel_type = 'proxy'
            self.proxy_options = {
                'proxy_ip': options['proxyIp'],
                'proxy_port': options['proxy_port']
            }

        if 'name' in options:
            self.tunnel_name = options['name']

        if 'bypass' in options:
            self.bypass = options['bypass']

        if 'verbose' in options:
            self.verbose = options['verbose']

        if 'acceptAllCerts' in options:
            self.accept_all_certs = options['accept_all_certs']

    def _get_platform(self):
        current_platform = sys.platform
        if current_platform.startswith('win'):
            return 'windows', 'SBSecureTunnel.exe'
        elif current_platform.startswith('linux'):
            return 'linux', 'SBSecureTunnel'
        elif current_platform.startswith('darwin'):
            return 'macos', 'SBSecureTunnel'

        raise NotImplementedError('Unsupported platform')

    def _download_binary(self):
        platform_name, file_name = self._get_platform()
        download_link = 'https://sbsecuretunnel.s3.amazonaws.com/cli/{}/{}'.format(platform_name, file_name)
        target_file_path = os.path.join(tempfile.mkdtemp(), file_name)
        r = requests.get(download_link, stream=True)
        binary_file = open(target_file_path, 'wb')
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                binary_file.write(chunk)
        binary_file.close()
        os.chmod(target_file_path, 0o744)
        return target_file_path

    def _get_tunnel_history(self, active=True):
        WSS_URL = 'https://tunnel.smartbear.com'
        payload = {'email': self.username, 'authkey': self.authkey, 'active': active, 'domain': self.domain}
        r = requests.get('{}/history'.format(WSS_URL), params=payload)
        if r.status_code == 200:
            return r.json()['data']
        else:
            return []

    def _get_tunnel_id(self):
        history = self._get_tunnel_history()
        for tunnel in history:
            if self.tunnel_name is not None and tunnel['tunnelName'] == self.tunnel_name:
                return tunnel['_id']

            if tunnel['tunnelName'] is None and self.tunnel_name is None:
                return tunnel['_id']
        raise Exception('Could not retrieve tunnel ID')

    def is_active(self):
        return self.tunnel_process is not None and self.tunnel_process.poll() is None

    def run(self):
        tunnel_command = [self.tunnel_binary_path, '--username', self.username, '--authkey', self.authkey, '--quiet']
        if self.tunnel_type == 'local-html-files':
            tunnel_command.append('--dir', self.requested_options['directory'])

        if self.tunnel_type == 'proxy':
            tunnel_command.append('--proxyIp', self.requested_options['proxyIp'])
            tunnel_command.append('--proxyPort', self.requested_options['proxyPort'])

        if self.tunnel_name is not None:
            tunnel_command.append('--name', self.tunnel_name)

        if self.bypass:
            tunnel_command.append('--bypass')

        if self.verbose:
            tunnel_command.append('--verbose')

        if self.accept_all_certs:
            tunnel_command.append('--acceptAllCerts')

        self.tunnel_process = subprocess.Popen(tunnel_command)
        i = 0
        while i < 10:
            i += 1
            try:
                self.tunnel_id = self._get_tunnel_id()
            except:
                pass
            if self.tunnel_id is not None:
                break
            else:
                time.sleep(0.5)

    def stop(self):
        if not self.is_active():
            return

        self.tunnel_process.kill()
        i = 0
        while i < 10:
            i += 1
            time.sleep(0.5)
            if self.is_active():
                self.tunnel_process.terminate()
            else:
                break
