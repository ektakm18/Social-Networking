# Social Networking API
This is a social networking API that provides functionalities such as user signup, login, sending and responding to friend requests, searching users, and listing friends.

# Installation
Prerequisites
-Docker
-Docker Compose

Steps
1. Clone the repository:
  git clone https://github.com/your-username/your-repo-name.git

2. Build and run the Docker containers:
   docker-compose up --build

3. Apply migrations:
   docker-compose exec web python manage.py migrate

4. Access the application:
  Open your postman and go to http://localhost:8000

# API Endpoints 
1. Signup
Endpoint: /users/sign_up/
Method: POST
Description: User sign up for social networking.
Request Body:
            {
                "email": "user@example.com",
                "password": "password123",
                "first_name": "John",
                "last_name": "Doe"            #Optional
            }
   
3. Login
Endpoint: /users/login/
Method: POST
Description: Login with email and password.
Request Body:
            {
                "email": "user@example.com",
                "password": "password123"
            }

4. Send Friend Request
Endpoint: /networks/send_request/
Method: POST
Description: Send a friend request to another user.
Request Body:
            {
                "to_request": "friend@example.com"
            }

5. List Pending Friend Requests
Endpoint: /networks/list_pending_friend_request/
Method: GET
Description: Lists the received friend requests which are pending.

6. List Friends
Endpoint: /networks/list_friends/
Method: GET
Description: Lists the friends who have accepted the friend request.

7. Respond to Friend Request
Endpoint: /networks/respond_friend_request/
Method: PUT
Description: Respond to a pending friend request (accept/reject).
Request Body:
             {
                "from_request": "friend@example.com",
                "status": "accept"  // or "reject"
            }

8. Search Users
Endpoint: /networks/search_users/?search=ektatest@gmail.com OR /networks/search_users/?search=ek
Method: GET
Description: Search users by email (exact match) or name (partial match).
Query Parameter: search







