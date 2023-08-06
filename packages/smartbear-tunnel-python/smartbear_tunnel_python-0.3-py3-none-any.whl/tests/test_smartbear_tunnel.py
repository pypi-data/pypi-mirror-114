import unittest
import os.path
from smartbear_tunnel.client import SmartbearTunnel


class TestSmartbearTunnel(unittest.TestCase):
    def test_download_binary(self):
        s = SmartbearTunnel()
        f_path = s._download_binary()
        self.assertTrue(os.path.exists(f_path))

    def test_get_tunnel_history(self):
        s = SmartbearTunnel()
        try:
            s.run()
            history = s._get_tunnel_history(active=False)
            self.assertTrue(len(history) > 0)
        finally:
            s.stop()

    def test_get_tunnel_id(self):
        s = SmartbearTunnel()
        s.run()
        try:
            self.assertTrue(s.tunnel_id is not None)
        finally:
            s.stop()

    def test_tunnel_run(self):
        s = SmartbearTunnel()
        try:
            s.run()
            self.assertTrue(s.is_active())
        finally:
            s.stop()
