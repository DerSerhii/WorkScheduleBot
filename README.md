## Specification

It's necessary to develop a telegram bot that provides information about the work 
schedule, which is stored in Google Document. <br>
We can't influence the rules for scheduling Google Document.

It's necessary:
1. Get schedule data from Google Document.
2. Parse received data.
3. Create a telegram bot:
    - *client* part;
    - *moderator* part;
    - *superuser* part.
4. Superuser appoints moderators.
5. Moderator give clients access to their schedule.
6. Client part:
   - have access to the schedule;
   - available selection by:
     - **today**;
     - **tomorrow**;
     - **this week**;
     - **next week**;
     - **statistics**.
7. Create a database.
8. Make an alert when there is a change in the schedule.
