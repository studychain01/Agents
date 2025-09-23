import { useState } from "react";
import { ChatProvider } from "../state/ChatContext";
import ChatWindow from "../components/ChatWindow";
import { ChatComposer } from "../components/ChatComposer";
import { ConversationList } from "../components/ConversationList";

export default function ChatPage() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <ChatProvider>
      <div className="h-screen bg-white flex">
        {/* Sidebar */}
        <div className={`${sidebarOpen ? 'w-64' : 'w-0'} transition-all duration-300 bg-gray-900 overflow-hidden`}>
          <ConversationList />
        </div>
        
        {/* Sidebar Toggle */}
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="w-8 h-8 bg-gray-900 hover:bg-gray-800 text-white flex items-center justify-center transition-colors"
        >
          {sidebarOpen ? '←' : '→'}
        </button>
        
        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col bg-white">
          {/* Chat Messages */}
          <ChatWindow />
          
          {/* Message Input */}
          <ChatComposer />
        </div>
      </div>
    </ChatProvider>
  );
}