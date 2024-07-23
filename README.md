# Gemini API competition

Homepage: https://ai.google.dev/competition
Rules:

1. Build an app with the [Gemini API](https://ai.google.dev/gemini-api?authuser=1)
2. Create a demo video
3. Publish and [submit](https://ai.google.dev/competition/submission) to the competition

[Gemini API docs](https://ai.google.dev/gemini-api/docs?authuser=1)

## Idea: "CCTV" logger

This is a {mobile,web} app that connects to a camera in your home (on your dorbell, on a window) and provides you with a summary of main events:

- people, cars, animals passing by
- time of day, sunlight
- repeated events (e.g. "This man has passed by your door 3 times in the last hour")
- other?

## Technical scoping

Requirements

- Cheap amazon camera like baby monitor or home CCTV
  - Important thing is to have a simple API to access the frames
- Backend uses Gemini API
  - Send (prompt, image) every `n` frames (or video footage?), get JSON back
  - Response should be of the form:
    ```
    {
      "description": "Later afternoon, man walking dog, two white vans parked in front, bycicle on pavement."
      "entities": {
        "people": 1,
        "animals": 1,
        "vehicle": 3,
      },
      "sunlight": "afternoon",
      ...
    }
    ```
- Results are parsed and stored in (sqlite?) database
- Business logic decide whether to send notification to the frontend
- Frontend renders history of notifications, sends push notification according to business logic
  - (optional) frontend renders last frame

Further thoughts:

- Maybe always send a reference image (e.g. last frame) so that the LLM has a reference to compare the current image with ("what changed" is more relevant than "what you can see")
- Possibility of using another model in conjunction to extract more features

---

## First steps

Install the relevant packages under a python virtual environment:

```bash
cd /path/to/gemini-api-competition
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

As a quick test that we can use the api, generate your Google Cloud API token, save it under `.api_token` (or wherever you want, this is just a convenient place safe under `.gitignore`), and run

```bash
GOOGLE_API_KEY=$(cat .api_token) python hello_world.py
```

To test the basic functionality of the model, use the `test_model.py` script e.g.

```bash
python test_model.py --model 1.5_flash --images /path/to/image.jpg /path/to/another_image.jpg --api_token $(cat .api_token)
```

If one has a MongoDB instance running (perhaps through `sudo systemctl start mongodb`), the flag `--db` stores the results from the model to that database after computing all the model responses (Not intended for production as it's not online, just for testing).

## Running the application

We use the [Twisted Application Framework](https://docs.twisted.org/en/stable/core/howto/application.html) as our engine. To run the application, you will have to specify the full path to your virtual environment:

$ GOOGLE_API_KEY=$(cat .api_token) /path/to/.venv/bin/twistd --python twistd.py --nodaemon

TODO:

- [ ] Write service that takes picture, sends to model, stores in the db
- [ ] Write service that replies to HTTP requests
- [ ] Write client
- [ ] Add method to use `1.0` to take a description and convert it to JSON (not sure if possible or useful, but 1.0 is cheaper)
