import requests

url = 'http://127.0.0.1:8000'
def send_json(data: str) -> bool:
        """
        Sends a post request to the WebSocket server. Returns True if no exceptions were raised. False otherwise.
        """
        try:
            requests.post(url + '/post/', data=data, timeout=3)
            return True
        except requests.exceptions.ConnectionError:
            print("Server could not be found")
        except requests.exceptions.ReadTimeout:
            print("Connection timed out")
        return False