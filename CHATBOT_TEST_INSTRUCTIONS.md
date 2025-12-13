# Testing Instructions for Humanoid Robotics RAG Chatbot

## Prerequisites
1. Make sure your FastAPI backend is running at `http://127.0.0.1:8000`
2. Ensure your backend has the `/query` endpoint available
3. Have your documentation ingested into the vector database

## How to Test

### 1. Basic Functionality Test
1. Start your Docusaurus development server:
   ```bash
   npm run start
   ```
2. Open your browser to the Docusaurus site
3. Look for the floating neon robot button in the bottom-right corner
4. Click the button to open the chat modal
5. Verify the chat interface appears with the dark cyberpunk theme

### 2. Text Selection Test
1. Navigate to any documentation page
2. Select a paragraph or sentence of text (at least 10 characters)
3. Verify that the chat widget automatically detects the selection
4. If the chat is already open, verify the input field gets pre-filled with "Explain this: [selected text]"
5. If the chat is closed, open it and verify the pre-fill happens

### 3. Query Functionality Test
1. Type a question in the input field or use the auto-filled "Explain this:..." text
2. Click the send button or press Enter
3. Verify the loading indicator appears
4. Wait for the response from your backend
5. Verify the response appears in the chat window

### 4. API Integration Test
1. Open browser developer tools (F12)
2. Go to the Network tab
3. Send a message through the chatbot
4. Verify a POST request is made to `http://127.0.0.1:8000/query`
5. Check that the request body contains both `query` and `selected_text` fields
6. Verify the response is properly handled

### 5. Mobile Responsiveness Test
1. Open the site in a mobile browser or use browser dev tools to simulate mobile
2. Verify the chatbot widget is visible and functional
3. Test that the modal appears correctly on smaller screens
4. Verify text selection still works on mobile

### 6. Additional Features Test
1. Test the clear chat button
2. Test the close button
3. Verify the remove selection button works
4. Test typing multiple messages in succession
5. Verify the auto-scroll to the latest message works

## Troubleshooting

### If the chatbot doesn't appear:
- Verify the Layout wrapper is properly implemented
- Check browser console for errors
- Ensure the component files are in the correct locations

### If API requests fail:
- Verify your backend is running at `http://127.0.0.1:8000`
- Check that the `/query` endpoint is accessible
- Verify your backend supports CORS from `http://localhost:3000`

### If text selection doesn't work:
- Ensure you're selecting at least 10 characters
- Check browser console for JavaScript errors
- Verify the selection event listeners are working

## Expected Behavior
- The floating button should pulse with a neon cyan glow
- When text is selected, it should appear in the input field with "Explain this:" prefix
- Messages should appear with proper styling (user messages in cyan, bot responses in dark)
- Loading indicators should show when waiting for responses
- The interface should be fully responsive on mobile devices