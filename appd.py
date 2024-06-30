from fastapi import FastAPI
import httpx

from checks import ERRORS, assign_score, validate_visitor
from schema import VisitorOut
from pydantic import ValidationError

from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(ValidationError)
async def validation_error_handler(request, exc):
    print("exc", exc)
    good_objects = []
    bad_objects = []
    errors = {}
    
    # Iterate over the list of objects
    for index, obj in enumerate(exc.errors()):
        try:
            # Validate the object using pydantic
            validated_obj = VisitorOut(**obj)
            good_objects.append(validated_obj)
        except ValidationError as e:
            # If validation error, add the object to bad objects
            # and the error message to errors dictionary
            bad_objects.append(obj)
            errors[index] = e.errors()
    
    # Upload all good objects to the database
    #upload_to_database(good_objects)
    
    # Return the response with the list of good and bad objects
    # and their errors, if any
    print("custommerror", errors, good_objects, bad_objects)
    return JSONResponse(
        status_code=exc.code,
        content={"message": f"Exception Occurred! Reason -> {exc.message}"},
    )
    #return {"good_objects": good_objects, "bad_objects": bad_objects, "errors": errors}


timeout = httpx.Timeout(60, connect=60, read=60, write=30)

#https://test-be.free.beeceptor.com/api/hello?visitor_name=Tom
@app.get("/")
async def root():
    return {"client": "Hello World"}   

# the test API
@app.get("/api/hello")
async def test(visitor_name: str = "Tom"):
    return {"client_ip": "34.67.45.67", "location": "GHk", "greeting": f"No where {visitor_name}"}

async def call_api(api_url: str):
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(api_url)
        print("async", response)
        print("resp json", response.json())

        visitor_name = response.request.url.params.get("visitor_name")
        print(visitor_name)

        if response.status_code != 200:
            print("error validation", response.json())


        print(response.json())    
        return response.json() | {"visitor_name": visitor_name}


@app.get("/grade-task-one")
async def grade(api_url: str):
    print(api_url)
    response = await call_api(api_url)
    print(response)

    errors = validate_visitor(response) 
    print("errors", errors)

    if errors:
        print("errors", ERRORS)


    data = VisitorOut(**response)

    score = assign_score(data.model_dump())
    print("score", score)

    return {"message": "task one passed", "score": score}