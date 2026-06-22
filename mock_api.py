from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.post("/v1/chat/completions")
async def mock_chat_completion(request: dict):
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "yes"
                }
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8084)