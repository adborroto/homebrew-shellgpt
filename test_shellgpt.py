import unittest
from unittest.mock import patch, MagicMock
import subprocess
import sys
import shellgpt


class TestShellGPT(unittest.TestCase):

    @patch("shellgpt.subprocess.run")
    def test_save_to_defaults(self, mock_run):
        shellgpt._save_to_defaults("com.shellgpt.settings", "APIKey", "test_key")
        mock_run.assert_called_once_with(
            ["defaults", "write", "com.shellgpt.settings", "APIKey", "test_key"],
            check=True,
        )

    @patch("shellgpt.subprocess.check_output")
    def test_read_from_defaults(self, mock_check_output):
        mock_check_output.return_value = "test_value\n"
        result = shellgpt._read_from_defaults("com.shellgpt.settings", "APIKey")
        self.assertEqual(result, "test_value")
        mock_check_output.assert_called_once_with(
            ["defaults", "read", "com.shellgpt.settings", "APIKey"], text=True
        )

    @patch("shellgpt._read_from_defaults")
    def test_load_config(self, mock_read_from_defaults):
        mock_read_from_defaults.side_effect = ["test_api_key", "test_model"]
        config = shellgpt._load_config()
        self.assertEqual(
            config, {"api_key": "test_api_key", "default_model": "test_model"}
        )

    @patch("shellgpt._read_from_defaults")
    def test_load_config_missing(self, mock_read_from_defaults):
        mock_read_from_defaults.side_effect = [None, "test_model"]
        with self.assertRaises(ValueError):
            shellgpt._load_config()

    @patch("shellgpt._save_to_defaults")
    def test_model_command_set(self, mock_save_to_defaults):
        args = MagicMock()
        args.set = "gpt-3.5-turbo"
        args.list = False
        with patch("builtins.print") as mock_print:
            shellgpt.model_command(args)
            mock_save_to_defaults.assert_called_once_with(
                "com.shellgpt.settings", "DefaultModel", "gpt-3.5-turbo"
            )
            mock_print.assert_called_once_with("Default model set to gpt-3.5-turbo")

    @patch("shellgpt._load_config")
    def test_model_command_default(self, mock_load_config):
        args = MagicMock()
        args.set = None
        args.list = False
        mock_load_config.return_value = {"default_model": "gpt-3.5-turbo"}
        with patch("builtins.print") as mock_print:
            shellgpt.model_command(args)
            mock_print.assert_called_once_with("Default model: gpt-3.5-turbo")

    @patch("shellgpt._save_to_defaults")
    def test_init_command(self, mock_save_to_defaults):
        with patch("builtins.print") as mock_print:
            shellgpt.init_command("test_api_key", "gpt-3.5-turbo")
            mock_save_to_defaults.assert_any_call(
                "com.shellgpt.settings", "APIKey", "test_api_key"
            )
            mock_save_to_defaults.assert_any_call(
                "com.shellgpt.settings", "DefaultModel", "gpt-3.5-turbo"
            )
            mock_print.assert_called_once_with("Configuration saved successfully.")


if __name__ == "__main__":
    unittest.main()
