python manage.py loaddata data.json

## Restaurant Menu Voting API

### About
The API provides functionalities for users/employees to vote for their preferred meal of the day. This can be achieved through various endpoints:

- Adding employees: This action is restricted to admin users only. Admin users can add new employees to the system.
- Creating restaurants: Only admin users have the privilege to create new restaurants within the system.
- Creating menus for restaurants: Admin users, with the use of access keys specific to each restaurant, can create menus for the respective establishments.
- Fetching a user token: Users created in the previous step can obtain a user token through this endpoint. The token is necessary for authentication purposes.
- Fetching menus for the current day: Users with a valid token can retrieve menus available for the current day.
- Voting for a preferred menu: Users with a valid token can vote for the menu they like by submitting their choice.
- Fetching menu votes for the current day: Users with a valid token can access the vote results for menus on the current day.

Additionally, the API includes an admin panel that is exclusively accessible to admin users. This panel offers privileged features and functionalities intended for administrative purposes.

#### Tools used:
1. Django">=3.2,<3.3" (This is an LTS version hence stability)
2. Django Rest Framework
3. Python 3.7.13 (environment used)
4. Postgres (Production) & Sqlite (Development)
5. Docker
6. Flake8 (Linting)

#### Setup:
1. Development:
    - make sure you have python installed, we advise use of version mentioned
    - `git clone` the project and `cd` into it
    - create a virtual-environment `python -m venv venv`
    - inside the project, there's a `.env.example` file, copy it to `.env` in the same directory and edit it according to your environment
    - start your virtual-environment and install the requirements in `requirements.txt` file
    - please run `pre-commit install` to install the flake* pre-commit-hook
    - once you are sure the database has been connected properly, run the migrations
    - IMPORTANT: there's a Model called MenuScore (app is menu_scores), this needs fixtures to populate its database table
    - run the following to populate table with fixture: `python manage.py loaddata menus_scores/fixtures/scores.json`
    - create a superuser so you can do admin tasks `python manage.py createsuperuser`
    - after that, app should be ready, do `python manage.py runserver`
    - if everything is fine, visiting `http://127.0.0.1/admin`, should show the admin, you can login with your superuser
    - check if API is working well by visiting `http://127.0.0.1:8000/api/`, expected result should return text or json with 'working'


2. Production:
   - Setup is similar to development, but change the `IS_PRODUCTION` field in .env to True
   - make sure postgres is running
   - use `gunicorn` as your web server gateway
   - take note of the number of workers you assign and the worker timeout


3. Docker:
   - TBD

## API Reference
The API is organized around `REST`. Our API has predictable resource-oriented URLs, accepts json-encoded request payload, returns JSON-encoded responses, and uses standard HTTP response `codes`, `authentication`, and `verbs`.

Base URL:
```js
http://<your.server.domain>/api/
```

1. Create an Employee/User
   - This can be done via `admin` or API. Only a user marked as `is_staff` in admin can perform this action.
   - A user created via API is automatically saved as NOT staff i.e `is_staff=False`
     - ```js
       Method: POST
       Endpoint: "/api/user/create/"
       Headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer <YOUR_JWT_TOKEN_FROM_TOKEN_ENDPOINT>"
       }
       Payload: {
          "username": string [required],
          "email": string [required, email_string],
          "password": string [required, strong_password],
          "first_name": string [optional],
          "last_name": string [optional]
       }
       Success [HTTP_CODE: 201]: 
       {
         "username": "<passed_value>",
         "first_name": "<passed_value>",
         "last_name": "<passed_value>",
         "email": "<passed_value>"
       }
       Failure:
       Validation Response [HTTP_CODE: 400]:
         {
             "username": [
                 "A user with that username already exists."
             ],
             "password": [
                 "This field may not be blank."
             ],
             "email": [
                 "This field must be unique."
             ]
         }
       Permissions Error [HTTP_CODE 403]:
          {
            "detail": "<error message here>"
          }
       Other Errors [HTTP_CODE 400]:
          {
            "detail": "<error message here>"
          }
       
         Bonus Endpoints:
         View All Users [GET]: "/api/user/"
         View Single User [GET]: "/api/user/<user_id>"
         ```
     
2. Get a user token (Authentication)
   - Any user created in the system can request a token with their proper credentials.
      - ```js
          Method: POST
          Endpoint: "/api/token/"
          Headers: {
             "Content-Type": "application/json",
             "X-App-Version": "<APP_VERSION_HERE>"
          }
          Payload: {
             "username": string [required],
             "password": string [required, strong_password]
          }
          Success [HTTP_CODE: 200]: 
          {
            "refresh": "<JWT_REFRESH_TOKEN>", // @todo: this is still to be implemented
            "access": "<JWT_ACCESS_TOKEN>" // This is the one you need
          }
          Failure:
          Unauthorized Response [HTTP_CODE: 401]:
            {
                "detail": "No active account found with the given credentials"
            }
         ```
        
3. Create a restaurant:
   - This is only done by an Admin or `is_staff` user.
   - A successful request will return ACCESS-KEYS for a restaurant. Please keep these safe and share with any third parties that need to perform restaurant menu Admin actions.
      - ```js
          Method: POST
          Endpoint: "/api/restaurant/create/"
          Headers: {
             "Content-Type": "application/json",
             "Authorization": "Bearer <YOUR_JWT_TOKEN_FROM_TOKEN_ENDPOINT>"
          }
          Payload: {
             "label": string [required] -- the name of restaurant
          }
          Success [HTTP_CODE: 201]:
          ADMIN:
          {
            "uuid": "<GENERATED_UUID>",
             "label": "<NAME_PASSED>", 
              "access_key": {
                 "resource_key": "<ALLOCATED_ACCESS_KEY>",
                 "secret_key": "<ALLOCATED_SECRET_KEY>"
              }
          }
        
          Failure:
          Validation Response [HTTP_CODE: 400]:
            {
                "label": [
                    "This field may not be blank."
                ]
            }
          Permissions Error [HTTP_CODE 403]:
             {
               "detail": "<error message here>"
             }
          Other Errors [HTTP_CODE 400]:
             {
               "detail": "<error message here>"
             }
          
            Bonus Endpoints:
            View All Restaurants [GET]: "/api/restaurant/"
            View Single Restaurant [GET]: "/api/restaurant/<restaurant_uuid>"
         ```
        
4. Adding Menu for a restaurant:
   - This can only be done by Admin or `is_staff` user. 
   - To perform this action, you need to pass 2 additional headers `X-Access-Key` and `X-Secret-Key`
   - You can get these keys ONLY after creating restaurant and should be kept SAFE.
      - ```js
          Method: POST
          Endpoint: "/api/menu/create/"
          Headers: {
             "Content-Type": "application/json",
             "Authorization": "Bearer <YOUR_JWT_TOKEN_FROM_TOKEN_ENDPOINT>",
             "X-Access-Key": "<YOUR_ALLOCATED_ACCESS_KEY>",
             "X-Secret-Key": "<YOUR_ALLOCATED_SECRET_KEY>"
          }
          Payload: {
             "title": string [required] -- the title/name of the menu,
             "restaurant": string [required] -- the uuid of restaurant associated with menu,
             "description": string [required] -- the main description of the menu, html is supported,
          }
          Success [HTTP_CODE: 201]:
             {
                "title": "<PASSED_VALUE>",
                 "restaurant": "<PASSED_VALUE>",
                 "description": "<PASSED_VALUE>",
                 "uuid": "<GENERATED_UUID>"
             }
        
          Failure:
          Validation Response [HTTP_CODE: 400]:
            {
                "title": [
                    "This field may not be blank."
                ]
            }
          Permissions Error [HTTP_CODE 403]:
             {
               "detail": "<error message here>"
             }
          Other Errors [HTTP_CODE 400 | 404]:
             {
               "detail": "<error message here>"
             }
          
            Bonus Endpoints:
            View All Menus [GET]: "/api/menu/"
            View Single Menu [GET]: "/api/menu/<menu_uuid>"
         ```
        
5. Get Menus for the current day (today):
   - Any user with valid token can perform this action.
      - ```js
          Method: GET
          Endpoint: "/api/menu/today/"
          Headers: {
             "Content-Type": "application/json",
             "Authorization": "Bearer <YOUR_JWT_TOKEN_FROM_TOKEN_ENDPOINT>",
             "X-App-Version": "<YOUR_APP_VERSION>"
          }
          Success [HTTP_CODE: 201]:
            Example Response (NOTE: An Admin user will have 'access_keys' field for restaurant)
             [
               {
                  "uuid": "ee97835d8a",
                  "title": "bunny chow",
                  "restaurant": {
                     "uuid": "a3a5346d050c46ce9d733eaaa60a0001",
                     "label": "manitoba"
                  },
                  "description": "good food here"
               },
               {
                  "uuid": "c37dc1d962",
                  "title": "burger king",
                  "restaurant": {
                     "uuid": "a3a5346d050c46ce9d733eaaa60a0001",
                     "label": "manitoba"
                  },
                  "description": "good burger here"
               }
            ]
        
          Failure:
          Permissions Error [HTTP_CODE 403]:
             {
               "detail": "<error message here>"
             }
          Other Errors [HTTP_CODE 400 | 404]:
             {
               "detail": "<error message here>"
             }
         ```
        
6. Voting for a restaurant Menu *(New V2 endpoint)*:
   - Any user with valid token can perform this action.
   - To perform this action, you may need to check the Menu Scores API (`/api/menu/scores`), to know the valid score uuid to pass.
      - ```js
          Method: POST
          Endpoint: "/api/v2/menu/create/"
          Headers: {
             "Content-Type": "application/json",
             "Authorization": "Bearer <YOUR_JWT_TOKEN_FROM_TOKEN_ENDPOINT>",
             "X-App-Version": "<YOUR_APP_VERSION>"
          }
          Payload: {
             "user": string [required] -- the user_id of the app user,
             "menus": [
                {
                    "menu": string [required] -- the uuid of the menu,
                    "score": string [required] -- the uuid of the menu_score
                },
                {
                    "menu": string [required] -- the uuid of the menu,
                    "score": string [required] -- the uuid of the menu_score
                },
                ...
            ]
          }
        
          Success [HTTP_CODE: 201]:
             {
                "detail": "Success",
             }
        
          Failure:
          Validation Response [HTTP_CODE: 400]:
            {
                "user": [
                    "This field may not be blank."
                ]
            }
          Permissions Error [HTTP_CODE 403]:
             {
               "detail": "<error message here>"
             }
          Other Errors [HTTP_CODE 400 | 404]:
             {
               "error": "Failed to add vote"
             }
         ```
        
7. Voting for a restaurant Menu *(Mapped V1 endpoint)*:
   - Any user with valid token can perform this action.
      - ```js
          Method: POST
          Endpoint: "/api/v1/menu/create/"
          Headers: {
             "Content-Type": "application/json",
             "Authorization": "Bearer <YOUR_JWT_TOKEN_FROM_TOKEN_ENDPOINT>",
             "X-App-Version": "<YOUR_APP_VERSION>"
          }
          Payload: {
             "user": string [required] -- the user_id of the app user,
             "menu": string [required] -- the uuid of the menu
          }
        
          Success [HTTP_CODE: 201]:
             {
                "user": "<PASSED_ID>",
                "menu": "<PASSED_UUID>"
             }
        
          Failure:
          Validation Response [HTTP_CODE: 400]:
            {
                "user": [
                    "This field may not be blank."
                ],
                ...
            }
          Permissions Error [HTTP_CODE 403]:
             {
               "detail": "<error message here>"
             }
          Other Errors [HTTP_CODE 400 | 404]:
             {
               "detail": "<error message here>"
             }
         ```
        
8. Voting for a restaurant Menu *(Deprecated endpoint)*:
   - Any user with valid token can perform this action.
   - This API has been deprecated and is only used for LEGACY Apps
   - The API is directly mapped to the `v1` endpoint in point 7 (previous endpoint)
   - All the parameters are the same, please refer to `/api/v1/menu/create/`
   - For newer apps, this is not going to work please use `v2`
      - ```js
        Endpoint: "api/menu/vote/"
        ```
        
9. Fetch all vote results of current day:
   - Any user with valid token can perform this action.
   - This returns a list of all votes, ordered/grouped by most favorable menu to the least.
      - ```js
          Method: GET
          Endpoint: "/api/menu/vote/today/"
          Headers: {
             "Content-Type": "application/json",
             "Authorization": "Bearer <YOUR_JWT_TOKEN_FROM_TOKEN_ENDPOINT>",
             "X-App-Version": "<YOUR_APP_VERSION>"
          }
          Success [HTTP_CODE: 201]:
            Example Response (NOTE: An Admin user will have 'access_keys' field for restaurant)
             [
               {
                  "user": "mrstark",
                  "menu": {
                      "uuid": "47b35a9b4e",
                      "title": "chicken quarter",
                      "restaurant": {
                          "uuid": "a3a5346d050c46ce9d733eaaa60a0001",
                          "label": "manitoba"
                      },
                      "description": "very nice menu"
                  },
                  "score": {
                      "label": "love it (1)",
                      "uuid": "55fcfe532d"
                  },
                  "created_at": "2023-05-22T11:04:24.180095Z"
               },
                ...
            ]
        
          Failure:
          Permissions Error [HTTP_CODE 403]:
             {
               "detail": "<error message here>"
             }
          Other Errors [HTTP_CODE 400 | 404]:
             {
               "detail": "<error message here>"
             }
         ```
        
10. Fetch list of allowed scores:
    - Any user with valid token can perform this action.
    - This returns a list of all scores allowed when voting for a menu.
       - ```js
           Method: GET
           Endpoint: "/api/menu/scores/"
           Headers: {
              "Content-Type": "application/json",
              "Authorization": "Bearer <YOUR_JWT_TOKEN_FROM_TOKEN_ENDPOINT>",
              "X-App-Version": "<YOUR_APP_VERSION>"
           }
           Success [HTTP_CODE: 201]:
             Example Response (NOTE: An Admin user will have 'access_keys' field for restaurant)
              [
                {
                   "user": "mrstark",
                   "menu": {
                       "uuid": "47b35a9b4e",
                       "title": "chicken quarter",
                       "restaurant": {
                           "uuid": "a3a5346d050c46ce9d733eaaa60a0001",
                           "label": "manitoba"
                       },
                       "description": "very nice menu"
                   },
                   "score": {
                       "label": "love it (1)",
                       "uuid": "55fcfe532d"
                   },
                   "created_at": "2023-05-22T11:04:24.180095Z"
                },
                 ...
             ]
        
           Failure:
           Permissions Error [HTTP_CODE 403]:
              {
                "detail": "<error message here>"
              }
           Other Errors [HTTP_CODE 400 | 404]:
              {
                "detail": "<error message here>"
              }
          ```
         
### Improvements that can be done:
- Implement token refresh endpoint
- Use Sentry for error logging/monitoring
- Add Middleware to validate required headers
- Implement a Custom JsonResponse method to make ALL API Responses uniform e.g:
    ```js
    {
        "code": [Any HTTP_CODE],
        "data": [Response Payload]
    }
    ```
- Add an API Auditing Middleware, such as seperate database to track all API requests and responses, so as to know whats happening in the main database, incase we need to track problems.
- Can use a logging platform like Loggly
- Add API throttling, to avoid DDOS attacks
- Encrypt user data like emails, before database storage
- Implement Swagger for API documentation and easy API testing
- Implement Redis for data frequently fetched like Menus

## High Availability (HA) Cloud Architecture Schema
The high-availability (HA) cloud architecture for the application can be set up using `Azure` with the following components:

1. `Load Balancer`:
   - A load balancer can be configured to distribute incoming traffic across multiple instances of the application to ensure load distribution and high availability.
   - The load balancer can perform health checks on the application instances and route traffic to healthy instances.

2. `Virtual Machines (VMs) or App Service`:
   - Multiple VMs or Azure App Service instances can be provisioned to host the application.
   - The application instances should be spread across different availability zones or regions for redundancy and fault tolerance.
   - Auto-scaling can be enabled to automatically adjust the number of instances based on traffic load.

3. `Azure Database Service`:
   - Utilize Azure Database service (e.g., Azure SQL/Postgres Database) to store and manage the application's database.
   - Configure the database for high availability, such as enabling geo-replication or deploying a database failover group across different regions.

4. `Azure Blob Storage`:
   - Use Azure Blob Storage to store static assets, media files, or other large data.
   - Configure replication and redundancy options to ensure data availability and durability.

5. `Caching and CDN`:
   - Implement Azure Cache for Redis or Azure CDN (Content Delivery Network) to improve application performance and reduce latency.
   - Caching can be utilized for frequently accessed data, while CDN can help distribute content globally.

6. `Monitoring and Logging`:
   - Implement Azure Monitor and Azure Application Insights to monitor the health, performance, and availability of the application and underlying infrastructure.
   - Configure alerts and notifications to proactively identify and address any issues.

7. `Disaster Recovery and Backup`:
   - Set up disaster recovery mechanisms such as Azure Site Recovery or backups to ensure data protection and the ability to recover in case of any failures.


![HA Cloud Architecture](assets/High%20Availability%20(HA)%20Cloud%20Architecture%20Schema.drawio.png)