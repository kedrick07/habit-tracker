# Habit Tracker Application - Project Documentation

## 📋 Project Overview

### Purpose
A web-based habit tracking application that allows users to create, manage, and monitor their daily habits. Users can track their progress, view streaks, and analyze their consistency over time.

### Target Users
- Individuals looking to build positive habits
- People trying to break bad habits
- Anyone wanting to track personal goals and maintain accountability

### Technology Stack
- **Frontend Framework:** Streamlit (Python-based web framework)
- **Backend Language:** Python 3.11
- **Database:** MongoDB Atlas (Cloud NoSQL database)
- **Authentication:** Bcrypt (Password hashing)
- **Environment Management:** Conda

---

## 🎯 Core Functionality

### 1. User Authentication System

#### Registration (Sign Up)
- User provides: Name, Email, Password, Confirm Password
- System validates:
  - Email format is correct
  - Password meets minimum requirements (at least 6 characters)
  - Password and confirm password match
  - Email doesn't already exist in database
- System creates new user account:
  - Password is hashed using bcrypt (never stored as plain text)
  - User record is saved to MongoDB Users collection
  - User is automatically logged in after registration

#### Login
- User provides: Email, Password
- System validates:
  - Email exists in database
  - Password matches hashed password in database
- System creates user session:
  - User information is stored in Streamlit session state
  - User remains logged in until they log out or close browser

#### Logout
- User clicks logout button
- System clears session state
- User is redirected to login page

#### Session Management
- When user is logged in, their user_id is stored in session
- All database operations use this user_id to ensure data isolation
- If user refreshes page, session persists (until browser closes)

---

### 2. Habit Management (CRUD Operations)

#### Create Habit
**User Journey:**
1. User navigates to "Add New Habit" page
2. User fills out form:
   - Habit Name (required) - e.g., "Morning Exercise"
   - Category (required) - dropdown: Health, Productivity, Finance, Learning, Fitness, Mindfulness, Other
   - Description (optional) - e.g., "30 minutes of yoga"
   - Start Date (required) - defaults to today
3. User clicks "Create Habit" button
4. System validates inputs (name not empty, valid date)
5. System saves habit to database with logged-in user's user_id
6. User sees success message
7. Habit appears in user's habit list

**Database Operation:**
- Insert new document into Habits collection
- Document includes: user_id, name, category, description, start_date, created_at

---

#### Read/View Habits
**User Journey:**
1. User navigates to Dashboard or "My Habits" page
2. System queries database for all habits belonging to logged-in user
3. System displays habits in organized format:
   - **Dashboard View:** Cards or table showing all habits with quick stats
   - **Today's Check-in View:** List of habits with checkboxes for today
   - **Individual Habit View:** Detailed page showing single habit with full history

**What User Sees:**
- Habit name and category
- Description
- Start date
- Current streak (consecutive days completed)
- Total completions
- Completion rate (percentage)
- Calendar/history of past completions

**Database Operation:**
- Query Habits collection where user_id matches logged-in user
- Query Completions collection to calculate statistics
- Join data and display to user

---

#### Update/Edit Habit
**User Journey:**
1. User navigates to "My Habits" page
2. User clicks "Edit" button next to a habit
3. System loads habit details into edit form
4. Form is pre-filled with existing data:
   - Habit Name
   - Category
   - Description
   - Start Date
5. User modifies desired fields
6. User clicks "Update Habit" button
7. System validates inputs
8. System updates habit in database
9. User sees success message
10. Updated habit appears in habit list

**Database Operation:**
- Find habit document by habit_id and user_id (security check)
- Update document with new values
- Return success/failure status

---

#### Delete Habit
**User Journey:**
1. User navigates to "My Habits" page
2. User clicks "Delete" button next to a habit
3. System shows confirmation dialog: "Are you sure you want to delete this habit? This will also delete all completion history."
4. User confirms deletion
5. System removes habit and all associated completions from database
6. User sees success message
7. Habit is removed from habit list

**Database Operation:**
- Delete habit document from Habits collection (matching habit_id and user_id)
- Delete all completion documents from Completions collection (matching habit_id)
- Cascade delete ensures no orphaned data

---

### 3. Daily Check-in and Completion Tracking

#### Mark Habit as Complete
**User Journey:**
1. User navigates to "Today's Check-in" page
2. System displays list of all user's habits
3. For each habit, system checks if already completed today:
   - If completed: checkbox is checked, shows green checkmark
   - If not completed: checkbox is unchecked
4. User clicks checkbox to mark habit as complete/incomplete for today
5. System immediately saves completion to database
6. System recalculates streak
7. User sees updated streak counter (with celebration animation if streak increased)
8. Optional: User can add a quick note about the completion (e.g., "Felt great!")

**Database Operation:**
- Check if completion record exists for this habit_id + today's date
- If exists and user unchecks: Update completed = false
- If doesn't exist and user checks: Insert new completion record with completed = true
- If exists and user checks: Update completed = true
- Include optional note field

---

#### View Completion History
**User Journey:**
1. User clicks on a specific habit to view details
2. System displays:
   - Calendar view showing which days habit was completed (visual heatmap)
   - List view showing chronological history with dates and notes
   - Statistics panel showing:
     - Current streak (e.g., "7 days")
     - Longest streak (e.g., "15 days")
     - Total completions (e.g., "45 times")
     - Completion rate for last 7/30/90 days (e.g., "85%")

**Database Operation:**
- Query Completions collection for all records matching habit_id
- Sort by date descending
- Calculate statistics:
  - Current streak: Count consecutive days from today backwards where completed = true
  - Longest streak: Find longest sequence of consecutive completed days
  - Total completions: Count all records where completed = true
  - Completion rate: (completed days / total days since start) * 100

---

### 4. Progress Tracking & Analytics

#### Dashboard Overview
**What User Sees:**
- Welcome message with user's name
- Summary statistics:
  - Total active habits
  - Today's completion rate (e.g., "5 out of 8 habits completed today")
  - Overall completion rate for the week
- Quick access to:
  - Today's habits that need to be done
  - Habits with active streaks (motivational)
  - Recent activity feed

---

#### Habit-Specific Analytics
**What User Sees (Per Habit):**
- **Streak Information:**
  - Current streak with visual indicator (fire emoji, progress bar)
  - Longest streak achieved (personal best)
  - Streak history chart showing ups and downs
  
- **Completion Patterns:**
  - Calendar heatmap (like GitHub contribution graph)
  - Days of week analysis (e.g., "You complete this habit most on Mondays")
  - Time-based trends (improving, declining, stable)

- **Performance Metrics:**
  - 7-day completion rate
  - 30-day completion rate
  - 90-day completion rate
  - All-time completion rate

---

## 🗄️ Database Architecture

### Collection 1: Users
**Purpose:** Store user account information

**Document Structure:**
```
{
  _id: ObjectId (auto-generated unique identifier)
  email: String (unique, user's email address)
  password: String (bcrypt hashed password)
  name: String (user's display name)
  created_at: DateTime (when account was created)
}
```

**Key Fields:**
- `_id`: Primary key, uniquely identifies each user
- `email`: Used for login, must be unique across all users
- `password`: Never stored as plain text, always hashed
- `name`: Displayed in UI (e.g., "Welcome back, John!")
- `created_at`: For analytics and account age tracking

**Relationships:**
- One user can have many habits (one-to-many)
- One user can have many completions (one-to-many)

---

### Collection 2: Habits
**Purpose:** Store habit definitions and metadata

**Document Structure:**
```
{
  _id: ObjectId (auto-generated unique identifier)
  user_id: ObjectId (reference to Users collection)
  name: String (habit name, e.g., "Morning Meditation")
  category: String (Health, Productivity, Finance, etc.)
  description: String (optional details about the habit)
  start_date: Date (when user wants to start tracking)
  created_at: DateTime (when habit was created in system)
}
```

**Key Fields:**
- `_id`: Primary key, uniquely identifies each habit
- `user_id`: Foreign key linking to Users collection (ensures data isolation)
- `name`: What the habit is called
- `category`: Groups similar habits together
- `description`: Additional context or motivation
- `start_date`: User-defined start (may differ from created_at)
- `created_at`: System timestamp

**Relationships:**
- Many habits belong to one user (many-to-one)
- One habit can have many completions (one-to-many)

---

### Collection 3: Completions
**Purpose:** Store daily completion records for each habit

**Document Structure:**
```
{
  _id: ObjectId (auto-generated unique identifier)
  habit_id: ObjectId (reference to Habits collection)
  user_id: ObjectId (reference to Users collection)
  completion_date: Date (which day this completion is for)
  completed: Boolean (true if done, false if skipped/failed)
  note: String (optional user note, e.g., "Felt energized!")
  logged_at: DateTime (when user marked it in system)
}
```

**Key Fields:**
- `_id`: Primary key, uniquely identifies each completion record
- `habit_id`: Foreign key linking to Habits collection
- `user_id`: Foreign key linking to Users collection (redundant but useful for queries)
- `completion_date`: The actual day being tracked (not when it was logged)
- `completed`: Boolean status
- `note`: Optional user reflection
- `logged_at`: System timestamp (may differ from completion_date if user logs retroactively)

**Relationships:**
- Many completions belong to one habit (many-to-one)
- Many completions belong to one user (many-to-one)

**Important Notes:**
- One completion record per habit per day
- If user marks today as complete, then unchecks, we update the same record (not create new one)
- completion_date is the date being tracked, logged_at is when it was entered

---

### Database Relationships Diagram

```
Users Collection
    |
    | (one user has many habits)
    |
    └──> Habits Collection
             |
             | (one habit has many completions)
             |
             └──> Completions Collection
```

**Example Data Flow:**
1. User "John" (user_id: 123) creates habit "Morning Exercise" (habit_id: 456)
2. John marks habit complete for today → Creates completion record:
   - habit_id: 456 (links to Morning Exercise)
   - user_id: 123 (links to John)
   - completion_date: 2025-10-14
   - completed: true

**Queries:**
- "Show me all of John's habits" → Query Habits where user_id = 123
- "Show me completion history for Morning Exercise" → Query Completions where habit_id = 456
- "Show me all completions John made today" → Query Completions where user_id = 123 AND completion_date = today

---

## 🔐 Security & Data Privacy

### Password Security
- **Never Store Plain Text Passwords:** All passwords are hashed using bcrypt before storage
- **Salt Rounds:** Bcrypt automatically adds salt to prevent rainbow table attacks
- **One-Way Hashing:** Impossible to reverse hash back to original password
- **Login Validation:** System compares hash of entered password with stored hash

### Data Isolation
- **User-Specific Queries:** Every database query includes user_id filter
- **No Cross-User Access:** User A cannot see or modify User B's data
- **Session-Based Access:** Only logged-in users can perform operations
- **Validation Checks:** Before updating/deleting, system verifies resource belongs to user

### Session Management
- **Streamlit Session State:** Stores user_id and authentication status
- **Session Expiry:** Session clears when user closes browser or logs out
- **No Session Hijacking:** Session data stored server-side, not in cookies

---

## 🎨 User Interface Pages

### Page 1: Login/Signup Page
**Purpose:** Authentication entry point

**Components:**
- Tab 1: Login Form
  - Email input field
  - Password input field (masked)
  - "Login" button
  - Link to switch to Signup tab
  
- Tab 2: Signup Form
  - Name input field
  - Email input field
  - Password input field (masked)
  - Confirm Password input field (masked)
  - "Create Account" button
  - Link to switch to Login tab

**User Flow:**
- New users start on Signup tab
- Returning users use Login tab
- After successful auth → Redirect to Dashboard

---

### Page 2: Dashboard (Home)
**Purpose:** Overview of user's habits and progress

**Components:**
- Header: "Welcome back, [User Name]!"
- Logout button (top-right)
- Statistics cards:
  - Total habits count
  - Today's completion progress bar
  - This week's completion rate
- "Today's Habits" section:
  - Quick checklist of habits due today
  - Checkboxes to mark complete
- "Your Habits" section:
  - Grid/table of all habits
  - Each habit shows: name, category, current streak
- Navigation sidebar:
  - Links to all other pages

**User Flow:**
- First page after login
- Central hub for quick actions
- Navigate to other pages via sidebar

---

### Page 3: Add New Habit
**Purpose:** Create a new habit

**Components:**
- Form with fields:
  - Habit Name (text input, required)
  - Category (dropdown select, required)
  - Description (text area, optional)
  - Start Date (date picker, defaults to today)
- "Create Habit" button
- "Cancel" button (returns to Dashboard)

**User Flow:**
1. Fill out form
2. Click Create
3. See success message
4. Redirected to Dashboard or My Habits page

---

### Page 4: My Habits
**Purpose:** View and manage all habits

**Components:**
- List/table of all user's habits
- For each habit:
  - Habit name (clickable to view details)
  - Category badge
  - Current streak indicator
  - "Edit" button (opens edit form)
  - "Delete" button (shows confirmation dialog)
- Search/filter bar (optional)
  - Filter by category
  - Search by name

**User Flow:**
- Browse all habits
- Click habit name → View details page
- Click Edit → Modify habit
- Click Delete → Confirm and remove

---

### Page 5: Edit Habit
**Purpose:** Modify existing habit details

**Components:**
- Pre-filled form with current habit data:
  - Habit Name (editable)
  - Category (editable dropdown)
  - Description (editable)
  - Start Date (editable)
- "Update Habit" button
- "Cancel" button

**User Flow:**
1. Change desired fields
2. Click Update
3. See success message
4. Return to My Habits page

---

### Page 6: Today's Check-in
**Purpose:** Daily completion tracking

**Components:**
- Date display (e.g., "Monday, October 14, 2025")
- List of all habits:
  - Habit name and category
  - Large checkbox (check = complete, uncheck = incomplete)
  - If completed: shows green checkmark + time completed
  - Optional: Note input field for each habit
  - Current streak display (updates in real-time)
- "Save All" button (if using batch save)
- Progress indicator: "X out of Y habits completed today"

**User Flow:**
1. User sees all habits for the day
2. Checks off completed habits
3. Optionally adds notes
4. Sees instant feedback (streak updates, animations)
5. Returns later in day to check more

---

### Page 7: Habit Details
**Purpose:** Deep dive into single habit with full analytics

**Components:**
- Habit information:
  - Name, category, description
  - Start date, days active
  - Edit and Delete buttons
  
- Statistics panel:
  - Current streak (large, prominent display)
  - Longest streak
  - Total completions
  - Completion rates (7/30/90 day)
  
- Completion history:
  - Calendar heatmap (visual representation)
  - Scrollable list of all completions with dates and notes
  - Charts showing trends over time

**User Flow:**
1. Click on habit from Dashboard or My Habits
2. View comprehensive statistics
3. Analyze patterns and trends
4. Option to edit or delete habit
5. Return to previous page

---

### Page 8: Profile/Settings (Optional)
**Purpose:** Manage user account

**Components:**
- User information:
  - Name (editable)
  - Email (display only)
  - Member since date
- Change password section
- Logout button
- Optional: Theme preferences, notification settings

---

## 🔄 Application Flow Diagram

```
START
  │
  ├─ Not Logged In → Login/Signup Page
  │                      │
  │                      ├─ Login Success ─┐
  │                      │                  │
  │                      └─ Signup Success ─┤
  │                                         │
  └─ Already Logged In ──────────────────> Dashboard
                                             │
                                             ├─> Add New Habit → Create → Back to Dashboard
                                             │
                                             ├─> My Habits ─┬─> View Habit Details
                                             │              ├─> Edit Habit → Update → Back
                                             │              └─> Delete Habit → Confirm → Back
                                             │
                                             ├─> Today's Check-in → Mark Completions → Dashboard
                                             │
                                             ├─> Analytics (optional)
                                             │
                                             └─> Logout → Login/Signup Page
```

---

## 🚀 Implementation Phases

### Phase 1: Foundation (Week 1)
- Set up MongoDB connection
- Create database helper functions
- Implement user authentication (signup, login, logout)
- Build basic session management
- Test user registration and login flow

### Phase 2: Core CRUD (Week 2)
- Implement Create Habit functionality
- Implement Read/View Habits (list view)
- Implement Update Habit functionality
- Implement Delete Habit functionality
- Build habit details page

### Phase 3: Completion Tracking (Week 3)
- Build Today's Check-in page
- Implement mark complete/incomplete functionality
- Calculate and display current streaks
- Show completion history
- Add optional notes feature

### Phase 4: Analytics & Polish (Week 4)
- Calculate all statistics (longest streak, completion rates)
- Build calendar heatmap visualization
- Create dashboard with overview stats
- Add data validation and error handling
- Improve UI/UX with better styling
- Test entire application flow

### Phase 5: Optional Enhancements
- Search and filter habits
- Export data to CSV
- Advanced charts and visualizations
- Category-based analytics
- Habit templates
- Dark mode theme

---

## 📊 Key Calculations & Logic

### Streak Calculation Algorithm
```
Current Streak:
1. Start from today's date
2. Check if habit was completed today
   - If no: current streak = 0
   - If yes: continue to step 3
3. Count backwards day by day
4. For each day, check if habit was completed
   - If yes: increment streak counter
   - If no: stop counting, return current streak
5. Stop at habit's start_date

Example:
- Today (Oct 14): ✓ Completed
- Oct 13: ✓ Completed
- Oct 12: ✓ Completed
- Oct 11: ✗ Not completed
→ Current Streak = 3 days
```

### Longest Streak Algorithm
```
1. Get all completion records for habit
2. Sort by date ascending
3. Initialize: current_run = 0, longest_run = 0
4. Loop through dates:
   - If consecutive day and completed:
     increment current_run
   - Else:
     if current_run > longest_run:
       longest_run = current_run
     reset current_run = 0
5. Return longest_run
```

### Completion Rate Calculation
```
Completion Rate = (Days Completed / Total Days) × 100

For specific period (e.g., last 30 days):
1. Count days from (today - 30 days) to today
2. Count how many of those days have completed = true
3. Calculate percentage

Example:
- Period: Last 30 days
- Days completed: 24
- Completion Rate = (24 / 30) × 100 = 80%
```

---

## 🎯 Success Criteria

### Must Have (MVP)
- ✅ User can register and login securely
- ✅ User can create, read, update, delete habits
- ✅ User can mark habits as complete/incomplete for any date
- ✅ User can view current streak for each habit
- ✅ User can see basic completion history
- ✅ Data is persisted in MongoDB
- ✅ Users can only access their own data

### Should Have
- ✅ Dashboard with overview statistics
- ✅ Calendar heatmap visualization
- ✅ Longest streak calculation
- ✅ Completion rate percentages
- ✅ Category-based organization
- ✅ Optional notes on completions

### Nice to Have
- Advanced analytics and charts
- Search and filter functionality
- Export data feature
- Habit templates
- Social features (share progress)
- Mobile responsive design

---

## 🐛 Common Edge Cases to Handle

### Authentication
- User tries to register with existing email → Show error
- User enters wrong password → Show error message
- User leaves password field empty → Show validation error
- Passwords don't match during signup → Show error

### Habit Management
- User tries to create habit with empty name → Prevent submission
- User deletes habit with completion history → Confirm with warning
- User sets start date in the future → Allow but don't show in "today's" list
- User has no habits → Show empty state with "Create your first habit" message

### Completion Tracking
- User marks same habit complete twice in one day → Update existing record
- User marks habit complete for date before habit's start date → Prevent or warn
- User marks future date as complete → Allow (for planning) or prevent
- Habit deleted but completions remain → Cascade delete to avoid orphaned data

### Streaks
- Habit completed today but not yesterday → Streak resets to 1
- Habit just created today → Streak can be 0 or 1 based on first completion
- Streak calculation spans across months → Handle date arithmetic correctly

---

## 📝 Future Monetization Ideas

### Freemium Model
**Free Tier:**
- Up to 5 active habits
- Basic tracking and streaks
- 30 days of history

**Premium Tier ($4.99/month):**
- Unlimited habits
- Unlimited history
- Advanced analytics
- Export data
- Priority support
- Remove ads (if any)

### Additional Features
- Habit coaching/consulting services
- Premium habit templates marketplace
- Team/family plans
- API access for developers
- White-label solution for businesses

---

## 🔧 Technical Requirements Summary

### Development Environment
- Python 3.11+
- Conda environment manager
- VS Code (or preferred IDE)

### Required Libraries
- streamlit (web framework)
- pymongo (MongoDB driver)
- bcrypt (password hashing)
- python-dotenv (environment variables)
- pandas (data manipulation)

### External Services
- MongoDB Atlas (free tier)
- Internet connection (for cloud database)

### Browser Requirements
- Modern web browser (Chrome, Firefox, Safari, Edge)
- JavaScript enabled
- Cookies enabled (for session management)

---

## 📚 Reference Documentation

### Official Documentation Links
- Streamlit: https://docs.streamlit.io
- MongoDB: https://docs.mongodb.com
- PyMongo: https://pymongo.readthedocs.io
- Bcrypt: https://github.com/pyca/bcrypt

### Key Concepts to Understand
- CRUD operations (Create, Read, Update, Delete)
- NoSQL databases and document structure
- Password hashing and authentication
- Session management in web applications
- Frontend-backend communication
- Data validation and error handling

---

## 🎓 Learning Objectives

By completing this project, you will learn:
1. **Full-Stack Development:** Building complete web application
2. **Database Design:** Structuring collections and relationships
3. **Authentication:** Implementing secure user systems
4. **CRUD Operations:** Mastering database interactions
5. **UI/UX Design:** Creating intuitive user interfaces
6. **Data Visualization:** Displaying statistics and trends
7. **State Management:** Handling user sessions
8. **Problem Solving:** Debugging and handling edge cases

---

## ✅ Project Checklist

### Setup Phase
- [ ] Install required software and libraries
- [ ] Create MongoDB Atlas account and cluster
- [ ] Set up environment variables
- [ ] Test database connection

### Development Phase
- [ ] Implement user authentication
- [ ] Build habit CRUD operations
- [ ] Create completion tracking
- [ ] Develop analytics features
- [ ] Design user interface
- [ ] Test all features

### Documentation Phase
- [ ] Write code comments
- [ ] Create user guide
- [ ] Document API/database structure
- [ ] Prepare demo presentation

### Deployment Phase (Optional)
- [ ] Deploy to Streamlit Cloud or Heroku
- [ ] Set up production database
- [ ] Test in production environment
- [ ] Share with users for feedback

---

**End of Documentation**

This document should be used as a reference throughout development. Share this with AI assistants, teammates, or instructors to provide context about your project.