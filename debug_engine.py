import http.client
import json

def test_raw_engine():
    print("🛰️ Sending raw HTTP request directly to local Ollama server...")
    
    connection = http.client.HTTPConnection("localhost", 11434)
    
    payload = {
        "model": "gemma4:26b",
        "messages": [
            {
                "role": "user", 
                "content": "Generate a list of 3 target vocabulary words for an elementary English lesson."
            }
        ],
        "stream": False
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        connection.request("POST", "/api/chat", json.dumps(payload), headers)
        response = connection.getresponse()
        data = response.read().decode()
        
        print(f"\nStatus Code: {response.status}")
        parsed_data = json.loads(data)
        print("\n🤖 ENGINE RESPONSE:")
        print(parsed_data['message']['content'])
        
    except Exception as e:
        print(f"\n❌ ENGINE CRASHED: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    test_raw_engine()