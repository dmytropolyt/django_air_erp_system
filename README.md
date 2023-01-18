DjangoAir ERP System
--
Application like a service for management of the airline

ERP system union a few services in the one. 

The first service is a booking ticket and check-in. This service have two independent web interfaces. One interface will use by customers. Another interface will use by staff. 

The customer interface
--
The welcome screen has four input fields. The first two fields for selection of destination(from and to), the second for the date picker, and last for a count of passengers.

The next screen provides information about price, available seats and opportunity choice options like lunch, luggage. The last screen is a final step for booking tickets. After finish booking, a customer should get tickets and bill on email. 

Also, the customer will get a credentials on email for a personal cabinet. The personal cabinet shows information about the future and previous flights, balance and provides service for online check-in.

User can login via Google.

The staff interface
--
There is a separate custom admin page for staff interface (url - "staff/").

The staff interface has access by roles.

There is a list of staff roles sorted by hierarchy:
+ Gate manager
+ Check-in manager
+ Supervisor

Gate manager can register the boarding of the passenger at the gate using the ticket code.

Check-in manager makes check-in passenger, add options and take a fee for luggage.

The supervisor can do everything that do gate manager and check-in manager. And he can add or remove the gate manager and check-in manager. Also, he can create and cancel a flight, add or remove options.

Webhook
--
There is webhook for notify customer about upcoming flight tomorrow.
It is mock using flask for catching webhooks

Stack
--
+ Backend: Python(Django, Flask)
+ Database: PostgreSQL
+ Virtualization: Docker
+ Background Task Queue: Celery
+ Broker: Redis
+ Frontend: Webpack, Bootstrap
+ Server: Nginx
