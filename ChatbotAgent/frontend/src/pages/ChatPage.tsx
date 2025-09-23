import { ChatProvider } from "../state/ChatContext";
import ChatWindow from "../components/ChatWindow";
import ChatComposer from "../components/ChatComposer";
import ConversationList from "../components/ConversationList.tsx";

export default function ChatPage() {
  return (
    <ChatProvider>
      <div className="h-screen bg-gray-50">
        <div className="flex h-full">
          {/* Sidebar */}
          <div className="w-64 bg-white border-r border-gray-200 shadow-sm">
            <ConversationList />
          </div>
          
          {/* Main Chat Area */}
          <div className="flex-1 flex flex-col">
            {/* Chat Header */}
            <div className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm">
              <h1 className="text-xl font-semibold text-gray-900">AI Assistant</h1>
              <p className="text-sm text-gray-500">How can I help you today?</p>
            </div>
            
            {/* Chat Messages */}
            <ChatWindow />
            
            {/* Message Input */}
            <ChatComposer />
          </div>
        </div>
      </div>
    </ChatProvider>
  );
}
