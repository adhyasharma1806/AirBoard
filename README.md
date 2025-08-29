✋ AirBoard: A Gesture-Controlled Environment

AirBoard is an AI-powered gesture environment that replaces traditional input devices with hand gestures. It allows users to perform typing, navigation, and control tasks using only their hands, captured via a webcam. This project focuses on creating a hands-free, accessible, and intuitive interface for digital interaction.

🚀 Features

Gesture Recognition – Detects and classifies real-time hand movements.

Air Typing – Type on a virtual keyboard using hand gestures.

Web-Based Interface – Runs directly in the browser with no extra hardware.

High Accuracy – AI-powered gesture filtering to reduce errors.

Accessibility Support – Designed to help users with mobility challenges.

🛠️ Tech Stack

Frontend: React + TailwindCSS

Gesture Recognition: Python + MediaPipe + OpenCV

Backend: Python (Flask or FastAPI)

ML Extensions: TensorFlow / PyTorch (optional for training gestures)

📂 Project Structure

frontend → contains the React application

backend → contains the Python application

app.py (Flask/FastAPI entry point)

requirements.txt (list of dependencies)

gesture/ (gesture recognition logic)

README.md → project documentation

⚡ Getting Started
Step 1: Clone the repository

Download or clone the project folder from GitHub.

Step 2: Setup Frontend

Go to the frontend folder, install dependencies, and start the development server.

Step 3: Setup Backend

Go to the backend folder, create a Python virtual environment, install dependencies, and start the backend server.

Step 4: Run

Frontend will run in the browser (default: http://localhost:5173).

Backend will run locally (default: http://localhost:8000).

🎮 Usage

Open the frontend in your browser.

The backend handles gesture detection and sends results to the frontend.

Perform gestures such as:

Tap Gesture → Select a key

Swipe → Navigation or scrolling

Fist / Palm → Special actions

Your actions appear instantly on the AirBoard interface.

🔮 Future Enhancements

Air Drawing for sketches.

Multi-user collaborative AirBoard.

Custom gesture mappings.

Integration with AR/VR devices.

👨‍💻 Author

Your Name – Developer & Researcher
