import json
import requests


class HHackServer:
    def __init__(self):
        # Base URL for the SQL API endpoint
        self.url = "https://bioeng-hhack-app.impaas.uk/api/sqlraw"

    def serverRequest(self, SQLrequest):
        """
        Send a SQL query to the server for execution.

        :param SQLrequest: A string containing the SQL query.
        :return: Parsed JSON response or a message.
        """
        headers = {
            "Accept": "application/json",  # Expect JSON responses
            "Content-Type": "text/plain",  # Sending raw SQL as plain text
            "charset": "utf-8"
        }
        try:
            # Send the POST request with the SQL query in the body
            response = requests.post(self.url, data=SQLrequest, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                if response.text.strip():  # Ensure the response body is not empty
                    try:
                        response_json = json.loads(response.text)

                        # If response is a list, return the list directly
                        if isinstance(response_json, list):
                            return response_json

                        # If response is a dictionary, return it directly
                        elif isinstance(response_json, dict):
                            return response_json

                        # For any other type of response, wrap it in a dictionary
                        return {"message": response.text}
                    except json.JSONDecodeError:
                        # If the response is not JSON, return it as plain text
                        return {"message": response.text}
                else:
                    return {"message": "Query executed successfully, no output returned."}
            else:
                return {"error": f"HTTP {response.status_code}: {response.reason}"}
        except Exception as e:
            return {"error": str(e)}

    def serverStatus(self):
        """
        Check the status of the server.

        :return: A message indicating the server status.
        """
        headers = {
            "Accept": "application/json",
            "charset": "utf-8"
        }
        try:
            # Send a GET request to the server
            response = requests.get(self.url, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                return {"message": response.text}
            else:
                return {"error": f"HTTP {response.status_code}: {response.reason}"}
        except Exception as e:
            return {"error": str(e)}
