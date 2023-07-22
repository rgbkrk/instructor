# Citation with Extraction

This repository contains a FastAPI application that uses GPT-4 to answer questions based on a given context and extract relevant facts with correct and exact citations. The extracted facts are returned as JSON events using Server-Sent Events (SSE).

## How it Works

The FastAPI app defines an endpoint `/extract` that accepts a POST request with JSON data containing a `context` and a `query`. The `context` represents the text from which the question is being asked, and the `query` is the question itself.

The app leverages GPT-4, an advanced language model, to generate answers to the questions and extract relevant facts. It ensures that the extracted facts include direct quotes from the given context.

## Example Usage

To use the `/extract` endpoint, send a POST request with `curl` or any HTTP client with the following format:

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "context": "In 1969, NASA astronauts Neil Armstrong and Buzz Aldrin became the first humans to land and walk on the Moon during the Apollo 11 mission.",
  "query": "Who were the first humans to land on the Moon?"
}' -N http://localhost:8000/extract
```

Replace `http://localhost:8000` with the actual URL of your FastAPI app if it's running on a different host and port. The API will respond with Server-Sent Events (SSE) containing the extracted facts in real-time.

## Requirements

To run this application, ensure you have the following Python packages installed:

```bash
pip install -r requirements.txt
```

## Running the App

To run the FastAPI app, execute the following command:

```bash
uvicorn main:app --reload
```

This will start the server, and the `/extract` endpoint will be available at `http://localhost:8000/extract`.

## Note

Ensure that you have a valid API key for GPT-4 from OpenAI. If you don't have one, you can obtain it from the OpenAI website.

Please use this application responsibly and be mindful of any usage limits or restrictions from OpenAI's API usage policy.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it as you see fit.