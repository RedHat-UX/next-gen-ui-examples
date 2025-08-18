# AI Chatbot with PatternFly

A modern AI chatbot interface built with React, TypeScript, Vite, and PatternFly components. This application provides a clean and accessible chat interface following Red Hat's design system guidelines.

## Features

- 🎨 **Modern UI**: Built with PatternFly components for a consistent and professional look
- 🌙 **Dark Mode**: Toggle between light and dark themes with a switch in the header
- 💬 **Interactive Chat**: Real-time messaging interface with user and AI message types
- 📝 **Mock Messages**: Pre-loaded with sample conversation to demonstrate functionality
- 🖥️ **Full-Screen Layout**: Uses PatternFly's Page component for full viewport coverage
- ⌨️ **Keyboard Support**: Press Enter to send messages, Shift+Enter for new lines
- 🔄 **Loading States**: Visual feedback with typing indicators when AI is processing
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices
- ♿ **Accessible**: Follows WCAG guidelines with proper ARIA labels and keyboard navigation
- 🚀 **Fast Performance**: Powered by Vite for instant hot module replacement

## Getting Started

### Prerequisites

- **Node.js (version 18 or higher required)** - Current project uses Vite 7 which requires Node 18+
  - If you're using Node 12 (like v12.22.12), you'll need to upgrade
  - Recommended: Use Node 18 LTS or Node 20 LTS
  - Check your version: `node --version`
  - To upgrade Node.js:
    - **macOS**: Use `brew install node` or download from [nodejs.org](https://nodejs.org/)
    - **Windows**: Download from [nodejs.org](https://nodejs.org/)
    - **Linux**: Use your package manager or [NodeSource](https://github.com/nodesource/distributions)
- npm or yarn package manager
- **Python 3.8+** for the backend API
- **Ollama** for running the AI model locally

### Installation

#### 1. Install Ollama and the AI Model

First, install Ollama and pull the required model:

```bash
# Install Ollama (macOS)
brew install ollama

# Or visit https://ollama.ai/download for other platforms

# Pull the required model
ollama pull llama3.2:3b

# Verify the model is available
ollama list
```

#### 2. Set Up the Backend (FastAPI)

The backend API server needs to run from the parent directory (`ngui-e2e/`):

```bash
# Navigate to the backend directory
cd ..  # Go to ngui-e2e/ (parent of NGUI-e2e/)

# Install Python dependencies (if needed)
pip install fastapi uvicorn langchain-openai

# Start the backend server
uvicorn main:app --reload
```

The backend API will be available at `http://localhost:8000`

#### 3. Set Up the Frontend (React App)

From this directory (`ngui-e2e/NGUI-e2e/`):

```bash
# Install frontend dependencies
npm install

# Start the frontend development server
npm run dev
```

The frontend application will be available at `http://localhost:5173`

### Running the Complete Application

To run the full application, you need to start both services:

1. **Start Ollama** (if not already running):
   ```bash
   ollama serve
   ```

2. **Start the Backend** (from `ngui-e2e/` directory):
   ```bash
   cd ../
   uvicorn main:app --reload
   ```

3. **Start the Frontend** (from `ngui-e2e/NGUI-e2e/` directory):
   ```bash
   npm run dev
   ```

The application will now be fully functional with:
- Frontend at `http://localhost:5173`
- Backend API at `http://localhost:8000`
- AI model running locally via Ollama

### Troubleshooting

#### Node.js Version Issues
If you encounter the error `SyntaxError: Unexpected token '.'` when running `npm run dev`, this means you're using an older version of Node.js. Vite 7 requires Node.js 18 or higher. Please upgrade your Node.js version and try again.

#### Model Issues
- Ensure Ollama is running: `ollama serve`
- Verify the model is available: `ollama list`
- If the model isn't working, try: `ollama run llama3.2:3b`

#### Backend Issues
- Make sure you're running the backend from the correct directory (`ngui-e2e/`, not `ngui-e2e/NGUI-e2e/`)
- Check that all Python dependencies are installed
- Verify the backend is accessible at `http://localhost:8000`

### Build

Create a production build:

```bash
npm run build
```

## Technologies Used

- **React 19** - UI library
- **TypeScript** - Type safety and better developer experience
- **Vite** - Fast build tool and development server
- **PatternFly** - Red Hat's open source design system
  - `@patternfly/react-core` - Core React components
  - `@patternfly/chatbot` - Specialized chatbot components
  - `@patternfly/react-icons` - Icon library
- **ESLint** - Code linting and quality

## Component Architecture

- **ChatBot.tsx**: Main chatbot component featuring:
  - Full-screen layout with PatternFly Page component
  - Dark mode toggle with theme switching
  - Message handling and UI state management
  - Pre-loaded mock messages for demonstration
  - Header toolbar with branding and controls
- **App.tsx**: Root application component with PatternFly styling imports

## Customization

### AI Integration

The current implementation includes a simulated AI response. To integrate with a real AI service:

1. Replace the `setTimeout` simulation in `handleSendMessage` with your AI API call
2. Update the response handling to process your AI service's response format
3. Add error handling for API failures

### Styling

The application uses PatternFly's design tokens and components. You can customize:

- Colors and themes through PatternFly CSS variables
- Component styling by extending PatternFly classes
- Layout and spacing using PatternFly's utility classes

## PatternFly Documentation

This project follows the [PatternFly AI Chatbot guidelines](https://www.patternfly.org/patternfly-ai/chatbot/ui). For more information about PatternFly components and patterns, visit the official documentation.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default tseslint.config([
  globalIgnores(["dist"]),
  {
    files: ["**/*.{ts,tsx}"],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      ...tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      ...tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      ...tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ["./tsconfig.node.json", "./tsconfig.app.json"],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
]);
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from "eslint-plugin-react-x";
import reactDom from "eslint-plugin-react-dom";

export default tseslint.config([
  globalIgnores(["dist"]),
  {
    files: ["**/*.{ts,tsx}"],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs["recommended-typescript"],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ["./tsconfig.node.json", "./tsconfig.app.json"],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
]);
```
