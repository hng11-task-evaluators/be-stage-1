from fastapi import FastAPI
import httpx
import re

from checks import is_valid_ip

app = FastAPI()

errors = []
@app.get("/")
async def root():
    return {"client": "Hello World"}   

# the test API
@app.get("/api/hello")
async def test(visitor_name: str = "Tom"):
    return {"client_ip": "127.0.0.1", "location": "Anywhere", "greeting": f"Hello {visitor_name}"}

@app.post("/grade")
async def grade(api_url: str):
    global errors
    errors = []  # Reset errors for each grading request
    score = 10
    response_data = {}

    try:
        # Check if the API URL is reachable and visitor_name is included in the query params
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{api_url}")

        if response.status_code != 200:
            errors.append(f"API did not return 200 OK, but {response.status_code}")
            return {"score": 0, "errors": f"API did not return 200 OK, but {response.status_code}"}
            #raise HTTPException(status_code=400, detail=f"API did not return 200 OK, but {response.status_code}")
        
        visitor_name = response.request.url.params.get("visitor_name")
        # Check if the visitor_name query parameter is present in the request URL
        if not visitor_name:
            errors.append("Query parameter 'visitor_name' is missing")
            score -= 2
            #raise HTTPException(status_code=400, detail="Query parameter 'visitor_name' is missing")

        response_data = response.json()
        print("response_data", response_data)


        # Check if visitor's name is part of the greeting
        if visitor_name and (visitor_name not in response_data.get("greeting")) or (not visitor_name and not response_data.get("greeting")):
            errors.append("Visitor_name is missing in greeting")
            score -= 2

        # Check if JSON response contains the required properties
        if not response_data.get("client_ip") or not is_valid_ip(response_data.get("client_ip")):
            is_variation = False
            for key in response_data.keys():
                if re.match(r"^(client)", key, re.IGNORECASE):
                    # the is_valid_ip() condition would make this loop run even if client_ip exists
                    if key == "client_ip":
                        break
                    is_variation = True
                    errors.append(f"Variation: {key} is not client_ip")
                    break
            if not is_variation:
                errors.append("Client ip is missing or invalid")
            score -= 2

        if not response_data.get("location"):
            errors.append("Location is missing")
            score -= 2

        if not response_data.get("greeting"):
            errors.append("Greeting is missing")
            score -= 2

        return {"score": score, "response": response_data, "errors": errors}

    except Exception as e:
        print("error", e)
        errors.append(str(e))
        return {"score": (score * 0), "response": response_data, "error-type": f"{type(e)}", "errors": errors}
        #raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)