import unittest

from gosu.gosu import env_from_sourcing, get_project_root


class TestBasicMethods(unittest.TestCase):
    def test_get_env_from_sourcing(self):
        env = env_from_sourcing(f"{get_project_root()}/.venv/bin/activate")
        self.assertGreater(len(env), 0)


if __name__ == "__main__":
    unittest.main()
