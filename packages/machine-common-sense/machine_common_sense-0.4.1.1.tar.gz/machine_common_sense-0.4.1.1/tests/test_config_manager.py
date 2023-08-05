import unittest

from machine_common_sense.config_manager import ConfigManager
from unittest.mock import patch
import os


class TestConfigManager(unittest.TestCase):

    def mock_env(**env_vars):
        return patch.dict(os.environ, env_vars, clear=True)

    @classmethod
    @mock_env()
    def setUpClass(cls):
        cls.config_mngr = ConfigManager(None)
        cls.config_mngr._config[
            cls.config_mngr.CONFIG_DEFAULT_SECTION
        ] = {}

    @classmethod
    def tearDownClass(cls):
        pass

    def test_init(self):
        self.assertEqual(
            self.config_mngr._config_file,
            self.config_mngr.DEFAULT_CONFIG_FILE)

    @mock_env()
    def test_init_with_arg(self):
        file_path = './arg-test.ini'
        config_mngr = ConfigManager(file_path)

        self.assertEqual(config_mngr._config_file, file_path)

    @mock_env(MCS_CONFIG_FILE_PATH='~/somefolder/env-var-test.ini')
    def test_init_with_env_variable(self):
        config_mngr = ConfigManager()

        self.assertEqual(
            config_mngr._config_file,
            '~/somefolder/env-var-test.ini')

    def test_validate_screen_size(self):
        self.config_mngr._config[
            self.config_mngr.CONFIG_DEFAULT_SECTION
        ][
            self.config_mngr.CONFIG_SIZE
        ] = '450'
        self.config_mngr._validate_screen_size()

        self.assertEqual(self.config_mngr.get_size(), 450)

        self.config_mngr._config[
            self.config_mngr.CONFIG_DEFAULT_SECTION
        ][
            self.config_mngr.CONFIG_SIZE
        ] = '449'
        self.config_mngr._validate_screen_size()

        self.assertEqual(self.config_mngr.get_size(),
                         self.config_mngr.SCREEN_WIDTH_DEFAULT)

    def test_get_aws_access_key_id(self):
        self.assertIsNone(self.config_mngr.get_aws_access_key_id())

        self.config_mngr._config[
            self.config_mngr.CONFIG_DEFAULT_SECTION
        ][
            self.config_mngr.CONFIG_AWS_ACCESS_KEY_ID
        ] = 'some_key_id'

        self.assertEqual(
            self.config_mngr.get_aws_access_key_id(),
            'some_key_id')

    def test_get_aws_secret_access_key(self):
        self.assertIsNone(self.config_mngr.get_aws_secret_access_key())

        self.config_mngr._config[
            self.config_mngr.CONFIG_DEFAULT_SECTION
        ][
            self.config_mngr.CONFIG_AWS_SECRET_ACCESS_KEY
        ] = 'some_secret'

        self.assertEqual(
            self.config_mngr.get_aws_secret_access_key(),
            'some_secret')

    def test_get_evaluation_name(self):
        self.assertEqual(self.config_mngr.get_evaluation_name(), '')

        self.config_mngr._config[
            self.config_mngr.CONFIG_DEFAULT_SECTION
        ][
            self.config_mngr.CONFIG_EVALUATION_NAME
        ] = 'test_eval'

        self.assertEqual(
            self.config_mngr.get_evaluation_name(),
            'test_eval')

    @mock_env()
    def test_get_metadata_tier(self):
        self.assertEqual(self.config_mngr.get_metadata_tier(), 'default')

        self.config_mngr._config[
            self.config_mngr.CONFIG_DEFAULT_SECTION
        ][
            self.config_mngr.CONFIG_METADATA_TIER
        ] = 'oracle'

        self.assertEqual(
            self.config_mngr.get_metadata_tier(),
            'oracle')

    @mock_env(MCS_METADATA_LEVEL='level2')
    def test_get_metadata_tier_with_env_variable(self):
        self.assertEqual(self.config_mngr.get_metadata_tier(), 'level2')

    def test_get_s3_bucket(self):
        self.assertIsNone(self.config_mngr.get_s3_bucket())

        self.config_mngr._config[
            self.config_mngr.CONFIG_DEFAULT_SECTION
        ][
            self.config_mngr.CONFIG_S3_BUCKET
        ] = 'some_s3_bucket'

        self.assertEqual(
            self.config_mngr.get_s3_bucket(),
            'some_s3_bucket')

    def test_get_s3_folder(self):
        self.assertIsNone(self.config_mngr.get_s3_folder())

        self.config_mngr._config[
            self.config_mngr.CONFIG_DEFAULT_SECTION
        ][
            self.config_mngr.CONFIG_S3_FOLDER
        ] = 'eval-test-folder'

        self.assertEqual(
            self.config_mngr.get_s3_folder(),
            'eval-test-folder')

    def test_get_seed(self):
        self.assertEqual(self.config_mngr.get_seed(), None)

        self.config_mngr._config[
            self.config_mngr.CONFIG_DEFAULT_SECTION
        ][
            self.config_mngr.CONFIG_SEED
        ] = '1'

        self.assertEqual(self.config_mngr.get_seed(), 1)

    def test_get_size(self):
        self.assertEqual(self.config_mngr.get_size(), 600)

        self.config_mngr._config[
            self.config_mngr.CONFIG_DEFAULT_SECTION
        ][
            self.config_mngr.CONFIG_SIZE
        ] = '800'

        self.assertEqual(self.config_mngr.get_size(), 800)

    def test_get_team(self):
        self.assertEqual(self.config_mngr.get_team(), '')

        self.config_mngr._config[
            self.config_mngr.CONFIG_DEFAULT_SECTION
        ][
            self.config_mngr.CONFIG_TEAM
        ] = 'team-name'

        self.assertEqual(
            self.config_mngr.get_team(),
            'team-name')

    def test_is_evaluation(self):
        self.assertFalse(self.config_mngr.is_evaluation())

        self.config_mngr._config[
            self.config_mngr.CONFIG_DEFAULT_SECTION
        ][
            self.config_mngr.CONFIG_EVALUATION
        ] = 'true'

        self.assertTrue(self.config_mngr.is_evaluation())

        self.config_mngr._config[
            self.config_mngr.CONFIG_DEFAULT_SECTION
        ][
            self.config_mngr.CONFIG_EVALUATION
        ] = 'false'

        self.assertFalse(self.config_mngr.is_evaluation())

    def test_is_history_enabled(self):
        self.assertTrue(self.config_mngr.is_history_enabled())

        self.config_mngr._config[
            self.config_mngr.CONFIG_DEFAULT_SECTION
        ][
            self.config_mngr.CONFIG_HISTORY_ENABLED
        ] = 'false'

        self.assertFalse(self.config_mngr.is_evaluation())

        self.config_mngr._config[
            self.config_mngr.CONFIG_DEFAULT_SECTION
        ][
            self.config_mngr.CONFIG_HISTORY_ENABLED
        ] = 'true'

        self.assertTrue(self.config_mngr.is_history_enabled())

    def test_is_noise_enabled(self):
        self.assertFalse(self.config_mngr.is_noise_enabled())

        self.config_mngr._config[
            self.config_mngr.CONFIG_DEFAULT_SECTION
        ][
            self.config_mngr.CONFIG_NOISE_ENABLED
        ] = 'true'

        self.assertTrue(self.config_mngr.is_noise_enabled())

        self.config_mngr._config[
            self.config_mngr.CONFIG_DEFAULT_SECTION
        ][
            self.config_mngr.CONFIG_NOISE_ENABLED
        ] = 'false'

        self.assertFalse(self.config_mngr.is_noise_enabled())

    def test_is_video_enabled(self):
        self.assertFalse(self.config_mngr.is_video_enabled())

        self.config_mngr._config[
            self.config_mngr.CONFIG_DEFAULT_SECTION
        ][
            self.config_mngr.CONFIG_VIDEO_ENABLED
        ] = 'true'

        self.assertTrue(self.config_mngr.is_video_enabled())

        self.config_mngr._config[
            self.config_mngr.CONFIG_DEFAULT_SECTION
        ][
            self.config_mngr.CONFIG_VIDEO_ENABLED
        ] = 'false'

        self.assertFalse(self.config_mngr.is_noise_enabled())


if __name__ == '__main__':
    unittest.main()
