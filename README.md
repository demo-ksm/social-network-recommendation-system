Social Recommendation System
A web-based recommendation system that suggests people and pages based on mutual connections and shared interests, simulating a mini social network like Instagram or Facebook.

#Features
* Suggests **People You May Know** using mutual friends
* Recommends **Pages You Might Like** based on shared interests
* Real-time recommendations from user input
* Error handling for invalid user IDs
* Clean and simple user interface

#Tech Stack
* Python (core logic)
* Flask (backend framework)
* HTML/CSS (frontend UI)

#How It Works:
* The system models users and their connections as a graph.
* Friend Recommendation:
  * Finds friends of friends.
  * Excludes already connected users.
  * Ranks suggestions by number of mutual friends.
* Page Recommendation:
  * Compares user interests using set intersection
  * Suggests pages liked by similar users.

#Preview
<img width="1056" height="720" alt="image" src="https://github.com/user-attachments/assets/22911aa3-aab6-47e8-b814-f386c5c5d6f7" />

#How to Run
1. Clone the repo
2. pip install flask
3. python main_code.py

#Key Concepts Used
* Graph-based relationships
* Set operations (intersection, uniqueness)
* Ranking and scoring logic

#Future Improvements
* Larger and more realistic dataset
* Better UI/UX (cards, dark mode, animations)
* Database integration (instead of static JSON)


#Author
Built as a learning project to explore recommendation systems and foundational web development concepts.
