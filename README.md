README - Project Setup and Running Instructions
=========================================

# Prerequisites
Ensure you have the following installed:
- Python (latest version recommended)
- Node.js and npm
- Virtual environment tool (optional but recommended)

# Backend Setup and Running
1. Navigate to the backend directory:
   ```sh
   cd backend
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the backend server:
   ```sh
   python main.py
   ```

# Frontend Setup and Running
1. Navigate to the frontend directory:
   ```sh
   cd frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Run the frontend application:
   ```sh
   npm start
   ```

# Running in Both Frontend and Backend Modes
To run the application fully:
1. Open two terminal windows.
2. Start the backend in one terminal as per the above steps.
3. Start the frontend in another terminal as per the above steps.
4. Access the application via the frontend URL (default: `http://localhost:3000/`).

# Notes
- Ensure all dependencies are installed before running the application.
- Check environment variables if required.
- Modify configurations in `.env` files if applicable.

For any issues, check logs or consult the documentation.

