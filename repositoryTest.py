import unittest
from unittest.mock import patch, Mock

from ssw567assignment3_1 import get_repositories


class TestGitHubAPI(unittest.TestCase):

    @patch("ssw567assignment3_1.requests.get")
    def test_valid_user(self, mock_get):
        repositories_response = Mock()
        repositories_response.status_code = 200
        repositories_response.text = '[{"name": "Triangle567"}, {"name": "Square567"}]'

        commits_response_1 = Mock()
        commits_response_1.status_code = 200
        commits_response_1.text = '[{"id": "1"}, {"id": "2"}, {"id": "3"}]'

        commits_response_2 = Mock()
        commits_response_2.status_code = 200
        commits_response_2.text = '[{"id": "1"}, {"id": "2"}]'

        mock_get.side_effect = [
            repositories_response,
            commits_response_1,
            commits_response_2
        ]

        result = get_repositories("testuser")

        expected = [
            ("Triangle567", 3),
            ("Square567", 2)
        ]

        self.assertEqual(result, expected)

    @patch("ssw567assignment3_1.requests.get")
    def test_invalid_user(self, mock_get):
        response = Mock()
        response.status_code = 404

        mock_get.return_value = response

        result = get_repositories("invaliduser123456")

        self.assertEqual(result, [])

    @patch("ssw567assignment3_1.requests.get")
    def test_user_with_no_repositories(self, mock_get):
        response = Mock()
        response.status_code = 200
        response.text = "[]"

        mock_get.return_value = response

        result = get_repositories("emptyuser")

        self.assertEqual(result, [])

    @patch("ssw567assignment3_1.requests.get")
    def test_repository_with_no_commits(self, mock_get):
        repositories_response = Mock()
        repositories_response.status_code = 200
        repositories_response.text = '[{"name": "EmptyRepo"}]'

        commits_response = Mock()
        commits_response.status_code = 200
        commits_response.text = "[]"

        mock_get.side_effect = [
            repositories_response,
            commits_response
        ]

        result = get_repositories("testuser")

        expected = [
            ("EmptyRepo", 0)
        ]

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()