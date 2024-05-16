


## How to execute

# Dependencies
1. Python 3.11
2. Pipenv
3. Docker (up and running)

<br>
<br>

# Execution
1. `$ pipenv install`
2. `$ pipenv shell`
3. `$ docker-compose up -d`
4. `export PYTHONPATH=${pwd}`
5. `python database/init_db.py`
6. `./start.sh`

<br>
<br>

# Validation
1. Open http://localhost:8080/docs
2. Use POST /lead/ to create a new lead, selecting a file and this user input
    ```json
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoer@email.com"
    }
    ```
3. To use the others endpoints just click in Authorize and use {user: admin password: admin}

<br>
<br>

## Result

1. Despite my efforts, I was unable to get the email sending functionality to work. I initially attempted to implement it using Gmail, and later tried with Mailchimp, which seemed more straightforward according to the documentation. Unfortunately, neither approach was successful. So this feature is currently not operational.

2. In the process of generating tokens, I bypassed the typical authentication step, which would involve validating existing user credentials and then generating JWT tokens, since the idea would only guard some apis behind authtorization for this test.

3. It's absolutely crucial not to leave environment variables exposed. However, given that this is a test, I've chosen to simplify the validation process for the time being.


## Necessary enhancements

1. As an alternative to merely validating and informing the user that we've already received their application, we might consider updating certain information, such as `first_name`, `last_name`, and `resume_file`, provided that the application status remains pending. However, this approach could have implications for internal management and would likely require further refinement and alignment with business expectations.

2. For a production-ready solution, we might consider using a file server, such as S3, to store the files instead of storing them directly in the database. We could then simply save the path to the file or even index the files by the lead's email. This approach could potentially offer improved performance and scalability.

3. Consider implementing a Service Dependency Injection approach. This could help reduce code verbosity and promote decoupling, leading to more maintainable and testable code.

4. Consider investing more time in automated testing, including acceptance tests, integration tests, and unit tests. Given more time, we could at least implement the acceptance tests following the acceptance criteria outlined in Notion..