import subprocess
import json
import os
import sys

def test_server():
    server_path = os.path.join(os.getcwd(), "server.py")
    
    # Start the server process
    process = subprocess.Popen(
        [sys.executable, server_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=os.getcwd()
    )

    print("Server process started. Sending initialization request...")

    # MCP Initialization Request
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0"}
        }
    }

    try:
        # Write to stdin
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()

        # Read response line by line
        while True:
            line = process.stdout.readline()
            if not line:
                break
            
            # FastMCP might output debug info to stdout if not careful, but usually it should be JSON-RPC
            try:
                response = json.loads(line)
                if response.get("id") == 1:
                    print("✅ Received Initialization Response:")
                    print(json.dumps(response, indent=2))
                    
                    # Now try asking for tools
                    tools_request = {
                        "jsonrpc": "2.0",
                        "id": 2,
                        "method": "tools/list",
                        "params": {}
                    }
                    process.stdin.write(json.dumps(tools_request) + "\n")
                    process.stdin.flush()
                
                elif response.get("id") == 2:
                    print("✅ Received Tools List:")
                    print(json.dumps(response, indent=2))
                    process.terminate()
                    return

            except json.JSONDecodeError:
                # Ignore non-JSON lines (like banners if they leaked to stdout, though they should be stderr)
                # print(f"Ignored stdout: {line.strip()}")
                pass

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        process.terminate()
        # Print stderr for debugging
        stderr_output = process.stderr.read()
        if stderr_output:
            print("\nServer Stderr/Logs:")
            print(stderr_output)

if __name__ == "__main__":
    test_server()
