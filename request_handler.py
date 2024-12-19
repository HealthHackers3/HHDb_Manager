#USE THIS TO ACCESS THE HHACK SERVER
#Instantiation:
#   s = HHackServer()
#
#serverRequest:
#   input: sql request string that will be executed on the server
#   output: if response is expected it will return a JSON file with responses. This can be printed or individual parts can be accessed.
#   example:
#       print(s.serverRequest(select * from users)['password'])
#       -->admin pass
#
#serverStatus:
#   function: returns a 'message' JSON object that indicates the server status
#   example:
#       print(s.serverStatus()['message'])
#       --> Server Running

import json
import requests

class HHackServer:
    def __init__(self):
        # This URL can be used to check the server status.
        self.url = "https://bioeng-hhack-app.impaas.uk/patients"

    def serverRequest(self, SQLrequest):  # message is a SQL request
        headers = {
            "Accept": "text/html",
            "Content-Type": "application/x-www-form-urlencoded",
            "charset": "utf-8"
        }
        try:
            response = requests.post(self.url, data=SQLrequest.encode('utf-8'), headers=headers)  # Send the POST request

            # Check if the request was successful
            if response.status_code == 200:
                if response.text.strip():  # Check if the response body is not empty
                    try:
                        response_json = json.loads(response.text)

                        # If response is a list (SELECT query), return the first row for key access
                        if isinstance(response_json, list) and response_json:
                            #print("Query Result:", response_json)
                            return response_json  # Return the first row for direct key access
                        elif isinstance(response_json, dict):
                            # For a direct JSON object response
                            #print("Response:", response_json)
                            return response_json
                        else:
                            #print("Non-JSON or unexpected response:", response.text)
                            return {"message": response.text}

                    except json.JSONDecodeError:
                        # For non-JSON responses (e.g., plain text success messages)
                        #print("Server Response:", response.text)
                        return {"message": response.text}
                else:
                    #print("No content returned from server (non-SELECT query).")
                    return {"message": "Query executed successfully, no output returned."}

            else:
                #print(f"Failed to send POST request. Status code: {response.status_code}")
                return {"error": f"HTTP {response.status_code}: {response.reason}"}

        except Exception as e:
            #print(f"An error occurred: {str(e)}")
            return {"error": str(e)}

    def serverStatus(self):
        headers = {
            "Accept": "text/html",
            "charset": "utf-8"
        }

        # Send the GET request
        response = requests.get(self.url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            #print(response.text)  # Print the response content (body of the response)
            return {'message':response.text}
        else:
            #print(f"Server seems to be down. Status code: {response.status_code}")
            return {'message':'No response from server'}