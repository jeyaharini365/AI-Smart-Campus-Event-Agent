# MongoDB Schema Design Document: AI Smart Campus Event Registration Agent

This document details the database layer design using MongoDB Atlas. The collections are designed to support structured transactions, semantic vector search, stateful conversational logs, and system notifications.

---

## 1. Collection Design Specification

### 1.1. `users` Collection
Stores authentication, authorization (roles), and profile preferences.

* **Database Type:** BSON Document
* **Fields & Descriptions:**
  * `_id` (ObjectId): Primary Key.
  * `email` (String): Unique campus email address.
  * `hashed_password` (String): Securely hashed user password.
  * `full_name` (String): User's legal first and last name.
  * `role` (String): Access control role (`student`, `organizer`, `admin`).
  * `profile` (Subdocument): Profile preferences for recommendations.
    * `department` (String): Student's major department (e.g., "Computer Science").
    * `academic_year` (Int32): Current year of study (1 to 4).
    * `skills` (Array of Strings): Student's self-declared skills (e.g., `["Python", "React"]`).
    * `interests` (Array of Strings): Student's area of interests (e.g., `["Machine Learning", "Hackathons"]`).
  * `created_at` (DateTime): Timestamp of account registration.
  * `updated_at` (DateTime): Timestamp of last profile update.
* **Validation Rules:**
  * `email` must match regex pattern: `^[a-zA-Z0-9._%+-]+@campus\.edu$` (or general email pattern).
  * `role` must be restricted to enum values: `["student", "organizer", "admin"]`.
  * `academic_year` must be an integer between 1 and 5.
* **Indexes:**
  * Unique Single-Field Index on `email`: `{ "email": 1 }` (Unique: true).
  * Single-Field Index on `role`: `{ "role": 1 }`.
* **Relationships:**
  * Referenced by `registrations.student_id` (1-to-Many).
  * Referenced by `chat_sessions.user_id` (1-to-1).
  * Referenced by `notifications.user_id` (1-to-Many).

---

### 1.2. `events` Collection
Stores metadata, schedules, vector embeddings, and FAQs.

* **Database Type:** BSON Document
* **Fields & Descriptions:**
  * `_id` (ObjectId): Primary Key.
  * `title` (String): Event name.
  * `description` (String): In-depth event description.
  * `organizer_id` (ObjectId): Reference to organizer `users._id`.
  * `category` (String): Grouping tag (`workshop`, `seminar`, `sports`, `cultural`).
  * `venue` (String): Location name (e.g., "Auditorium A").
  * `start_time` (DateTime): Start timestamp of the event.
  * `end_time` (DateTime): End timestamp of the event.
  * `capacity` (Int32): Maximum seats available.
  * `registered_count` (Int32): Current number of confirmed registrations.
  * `registration_fields` (Array of Subdocuments): Custom forms schema:
    * `name` (String): Field key name.
    * `type` (String): Data type (`string`, `number`, `boolean`).
    * `required` (Boolean): Mandatory flag.
  * `embedding` (Array of Double): 768-dimension vector for semantic search.
  * `faqs` (Array of Subdocuments): Questions & Answers list:
    * `question` (String): FAQ title.
    * `answer` (String): FAQ reply.
  * `schedule` (Array of Subdocuments): Event schedule timeline:
    * `time_slot` (String): E.g., "10:00 AM - 11:00 AM".
    * `title` (String): Activity name.
    * `description` (String): Activity summary.
    * `speaker` (String, optional): Guest speaker name.
  * `status` (String): State (`draft`, `published`, `cancelled`).
  * `created_at` (DateTime): Timestamp of creation.
* **Validation Rules:**
  * `status` must match: `["draft", "published", "cancelled"]`.
  * `category` must match: `["workshop", "seminar", "sports", "cultural"]`.
  * `registered_count` must be $\le$ `capacity`.
* **Indexes:**
  * Compound Index on category and start time: `{ "category": 1, "start_time": -1 }`.
  * Single-Field Index on `organizer_id`: `{ "organizer_id": 1 }`.
  * **MongoDB Atlas Vector Index** on `embedding`:
    * Vector dimensions: 768
    * Similarity metric: Cosine
* **Relationships:**
  * Reference relationship: `organizer_id` references `users._id` (Many-to-1).
  * Referenced by `registrations.event_id` (1-to-Many).

---

### 1.3. `registrations` Collection
Manages transactional tickets and check-in statuses.

* **Database Type:** BSON Document
* **Fields & Descriptions:**
  * `_id` (ObjectId): Primary Key.
  * `event_id` (ObjectId): Reference to `events._id`.
  * `student_id` (ObjectId): Reference to student `users._id`.
  * `custom_fields_responses` (Document): Key-value pairs for dynamic fields responses.
  * `ticket_code` (String): Unique cryptographic hash used for the check-in QR code.
  * `status` (String): Ticket state (`registered`, `checked_in`, `cancelled`).
  * `checked_in_at` (DateTime, Nullable): Check-in timestamp logs.
  * `created_at` (DateTime): Registration timestamp.
* **Validation Rules:**
  * `status` must match: `["registered", "checked_in", "cancelled"]`.
* **Indexes:**
  * Unique Compound Index (prevents double registrations): `{ "event_id": 1, "student_id": 1 }` (Unique: true).
  * Unique Single-Field Index on `ticket_code`: `{ "ticket_code": 1 }` (Unique: true).
* **Relationships:**
  * Reference relationship: `event_id` references `events._id` (Many-to-1).
  * Reference relationship: `student_id` references `users._id` (Many-to-1).

---

### 1.4. `chat_sessions` Collection
Stores chat history for active sessions, providing contextual memory.

* **Database Type:** BSON Document
* **Fields & Descriptions:**
  * `_id` (ObjectId): Primary Key.
  * `user_id` (ObjectId): Reference to student `users._id`.
  * `messages` (Array of Subdocuments): Conversational message list:
    * `role` (String): Sender (`user`, `assistant`, `system`, `tool`).
    * `content` (String): Raw textual message or tool results.
    * `timestamp` (DateTime): Message creation time.
  * `agent_state` (Document): Serialized LangGraph memory state snapshot.
  * `updated_at` (DateTime): Session heartbeat update timestamp.
* **Validation Rules:**
  * `messages.role` must match: `["user", "assistant", "system", "tool"]`.
* **Indexes:**
  * Single-Field Index on `user_id`: `{ "user_id": 1 }`.
  * TTL Index on `updated_at` (automatically clears idle guest sessions after 30 days): `{ "updated_at": 1 }` (expireAfterSeconds: 2592000).
* **Relationships:**
  * Reference relationship: `user_id` references `users._id` (Many-to-1).

---

### 1.5. `notifications` Collection
Manages alerts sent to users regarding upcoming events, schedule changes, or registration status.

* **Database Type:** BSON Document
* **Fields & Descriptions:**
  * `_id` (ObjectId): Primary Key.
  * `user_id` (ObjectId): Target recipient, references `users._id`.
  * `title` (String): Notification header.
  * `message` (String): Textual content of the alert.
  * `type` (String): Category (`info`, `alert`, `reminder`).
  * `is_read` (Boolean): Read status flag.
  * `created_at` (DateTime): Creation timestamp.
* **Validation Rules:**
  * `type` must match: `["info", "alert", "reminder"]`.
* **Indexes:**
  * Compound Index for fast lookup of unread alerts: `{ "user_id": 1, "is_read": 1 }`.
  * TTL Index on `created_at` (purges old notifications after 90 days): `{ "created_at": 1 }` (expireAfterSeconds: 7776000).
* **Relationships:**
  * Reference relationship: `user_id` references `users._id` (Many-to-1).
