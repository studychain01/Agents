import { useEffect, useRef } from "react";
import { useChatContext, type Message } from "../state/ChatContext";

interface MessageBubbleProps {
  message: Message;
}

function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";
  const isSystem = message.role === "system";
  
  return (
    <div className={`flex mb-6 ${isUser ? "justify-end" : "justify-start"}`}>
      <div className={`flex items-start space-x-3 max-w-[80%] ${isUser ? "flex-row-reverse space-x-reverse" : ""}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
          isUser 
            ? "bg-blue-600 text-white" 
            : isSystem
            ? "bg-yellow-500 text-white"
            : "bg-gray-600 text-white"
        }`}>
          {isUser ? "U" : isSystem ? "S" : "AI"}
        </div>
        
        {/* Message Content */}
        <div className={`rounded-2xl px-4 py-3 shadow-sm ${
          isUser 
            ? "bg-blue-600 text-white" 
            : isSystem
            ? "bg-yellow-50 text-yellow-800 border border-yellow-200"
            : "bg-white text-gray-900 border border-gray-200"
        }`}>
          {/* Message text */}
          <div className="whitespace-pre-wrap break-words text-sm leading-relaxed">
            {message.content}
          </div>
          
          {/* Timestamp */}
          <div className={`text-xs mt-2 ${
            isUser ? "text-blue-100" : "text-gray-500"
          }`}>
            {new Date(message.createdAt).toLocaleTimeString([], { 
              hour: '2-digit', 
              minute: '2-digit' 
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function ChatWindow() {
  const { state } = useChatContext();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [state.messages]);

  return (
    <div className="flex-1 overflow-y-auto bg-gray-50">
      <div className="max-w-4xl mx-auto px-6 py-8">
        {state.messages.length === 0 ? (
          <div className="h-full flex items-center justify-center min-h-[400px]">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Welcome to AI Assistant</h3>
              <p className="text-gray-500">Start a conversation by typing a message below.</p>
            </div>
          </div>
        ) : (
          <div>
            {state.messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
            
            {/* Loading indicator when streaming */}
            {state.status === "streaming" && (
              <div className="flex justify-start mb-6">
                <div className="flex items-start space-x-3 max-w-[80%]">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-600 text-white flex items-center justify-center text-sm font-medium">
                    AI
                  </div>
                  <div className="bg-white rounded-2xl px-4 py-3 shadow-sm border border-gray-200">
                    <div className="flex items-center space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0.1s" }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            {/* Scroll anchor */}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>
    </div>
  );
}
