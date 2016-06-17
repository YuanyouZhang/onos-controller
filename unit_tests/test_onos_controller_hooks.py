from mock import patch
from test_utils import CharmTestCase

with patch('charmhelpers.core.hookenv.config') as config:
    config.return_value = False
    import onos_hook as hooks


TO_PATCH = [
    'check_call',
    'config',
    'relation_set',
    'service_start',
    'shutil',
]

INSTALL_URL = 'https://downloads.onosproject.org/nightly/'\
              'onos-1.6.0-rc1.tar.gz'


class ONOSControllerHooksTests(CharmTestCase):

    def setUp(self):
        super(ONOSControllerHooksTests, self).setUp(hooks, TO_PATCH)

        self.config.__getitem__.side_effect = self.test_config.get
        self.config.get.side_effect = self.test_config.get
        self.install_url = INSTALL_URL
        self.test_config.set('install-url', self.install_url)
        self.test_config.set('profile', 'openvswitch-onos-goldeneye')

    def _call_hook(self, hookname):
        hooks.hooks.execute([
            'hooks/{}'.format(hookname)])

    @patch('os.symlink')
    @patch('os.path.exists')
    @patch('os.listdir')
    def test_install_hook(self, mock_listdir, mock_path_exists, mock_symlink):
        mock_listdir.return_value = ['random-file', 'onos-1.6.0-rc1.tar.gz']
        mock_path_exists.return_value = False
        self._call_hook('install')
        self.shutil.copy.assert_called_with("files/onos.conf", "/etc/init")

    def test_ovsdb_manager_joined_hook(self):
        self._call_hook('ovsdb-manager-relation-joined')
        self.relation_set.assert_called_with(port=6640, protocol="tcp")

    def test_controller_api_relation_joined_hook(self):
        self._call_hook('controller-api-relation-joined')
        self.relation_set.assert_called_with(port=8181,
                                             username="admin",
                                             password="admin")
