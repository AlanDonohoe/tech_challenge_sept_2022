# 🎉🎉🎉 Tech Challenge Sept 2022 🎉🎉🎉

This simple API takes user event data and depending upon the current event and that user's event history returns a response with any relevant alert codes.


# 🛠 Running the app locally 🛠

The app depends upon PostGres so it is built as an API service and a PostGres service which are both run as Docker containers via DockerCompose.

So you will need to have Docker and DockerCompose installed 

Download the repo [here](https://github.com/AlanDonohoe/tech_challenge_sept_2022.git) 

Then, in the terminal...

cd into the root of the project wherever you have saved it...

Build the images, by running:
```bash
docker-compose build
```

Then run the containers, by running:

```bash
docker-compose up -d
```

Wait for the containers to both start running...

Then run the db seed script (in the api container) to populate the db with a user whose user_id you will use in subsequent requests to the API:

```bash
docker-compose exec api python3 /usr/src/scripts/seed_db.py
```

Make a note of the user id that you should see either in your terminal or you can view the logs, via:
```bash
docker-compose logs -f
```

#  🙌 Making requests to the end point 🙌 

Now the containers are running and you have populated the db with a user, and grabbed that user's id you can make requests to the API.

Use Postman or curl to make post requests to:

http://0.0.0.0:5000/v1/event

With a json body, such as:

```json
{
    "amount": "146.00",
    "t": "2022-09-27 12:03:26.164292+00",
    "type": "deposit",
    "user_id": THE_UUID_USER_ID_YOU_GRABBED_BEFORE
}

```

You should see a response with the correct alert codes, and other fields, eg:

```json
{
   "alert": true,
   "alert_codes": [30, 123],
   "user_id": 1
}
```



