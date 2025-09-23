import { ChatProvider } from './state/ChatContext'
import ChatPage from './pages/ChatPage'

function App() {
  return (
    <ChatProvider>
      <div className="h-screen bg-gray-50">
        <ChatPage />
      </div>
    </ChatProvider>
  )
}

export default App
