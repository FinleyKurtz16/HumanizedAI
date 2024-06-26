from requests import post
from requests.exceptions import RequestException

##Verarbeitung
class Completion:
    """
    This class provides methods for generating completions based on prompts.
    """

    def create(self, prompt):
        """
        Create a completion for the given prompt using an AI text generation API.

        **Important Note:** This code snippet relies on an external API that might be discontinued or have security vulnerabilities. It's generally not recommended for production use.

        Args:
            prompt (str): The input prompt for generating the text.

        Returns:
            str: The generated text as a response from the API (if successful).

        Raises:
            requests.exceptions.RequestException: If there is an issue with sending the request or fetching the response.
        """
        try:
            resp = post(
                url="https://api.binjie.fun/api/generateStream",
                headers={
                    "origin": "https://chat.jinshutuan.com",
                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36",
                },
                json={
                    "prompt": prompt,
                    "withoutContext": True,
                    "stream": False,
                },
            )
            resp.encoding = "utf-8"
            return resp.text
        except RequestException as exc:
            raise RequestException("Unable to fetch the response.") from exc
