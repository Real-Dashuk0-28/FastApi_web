import unittest
from storage.redis_tokens_helper import RedisTokensHelper


class RedisTokensHelperTestCase(unittest.TestCase):

    def test_generate_and_save_token(self):
        helper = RedisTokensHelper()
        token = helper.generate_and_save_token()
        self.assertTrue(helper.token_exists(token))