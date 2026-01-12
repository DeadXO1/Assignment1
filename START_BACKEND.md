# How to Start the Backend Server

## Quick Start (Windows PowerShell)

1. **Open PowerShell or Command Prompt**

2. **Navigate to the backend directory:**
   ```powershell
   cd "C:\Users\hp\Desktop\1 ASSIGNMENT\backend"
   ```

3. **Activate the virtual environment:**
   ```powershell
   venv\Scripts\activate
   ```
   You should see `(venv)` at the start of your prompt.

4. **Start the server:**
   ```powershell
   python -m app.main
   ```

5. **You should see output like:**
   ```
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

6. **Keep this terminal open!** The server must stay running.

## If You Get Errors

### "No module named 'app'"
- Make sure you're in the `backend` directory
- Make sure virtual environment is activated (you should see `(venv)`)

### "Module not found" errors
- Run: `pip install -r requirements.txt`

### "Playwright not found"
- Run: `playwright install chromium`

### Port 8000 already in use
- Close the other application using port 8000
- Or change port in `backend/.env` file

## Verify It's Working

1. Open your browser
2. Go to: http://localhost:8000/docs
3. You should see the API documentation page

## Next Steps

Once the backend is running:
- The frontend should automatically connect
- Events will start scraping automatically
- Check the backend terminal for scraping logs

