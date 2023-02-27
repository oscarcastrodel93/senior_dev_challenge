# Run the app

- Pull the image:

    docker pull ocastro93/senior_dev_challenge

- Create a .env file with following params:
    ```
    secret=GENERATE_YOUR_OWN_SECRET_KEY
    algorithm=HS256
    ```

    Note: You can go to https://www.allkeysgenerator.com/Random/Security-Encryption-Key-Generator.aspx or https://randomkeygen.com/ to generate a random 256bit key.

- At the same .env file directory, run the image:
    ```
    docker run -d --env-file .env --name challenge_container -p 8080:8080 ocastro93/senior_dev_challenge
    ```

- Open the browser and go to http://localhost:8080/admin to manage modules or http://localhost:8080/docs to see API's documentation
