import { useEffect, useRef } from "react";
import { useChatContext, type Message } from "../state/ChatContext";

interface MessageBubbleProps {
  message: Message;
}

function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";
  
  return (
    <div className="py-2 bg-white">
      <div className="max-w-4xl mx-auto px-4">
        <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
          {/* Message Bubble */}
          <div className={`max-w-xs lg:max-w-md ${isUser ? 'ml-12' : 'mr-12'}`}>
            <div 
              className={`px-3 py-2 rounded-2xl ${
                isUser 
                  ? 'bg-blue-500 text-white rounded-br-md' 
                  : 'bg-gray-200 text-gray-900 rounded-bl-md'
              }`}
              style={{
                backgroundColor: isUser ? '#3b82f6' : '#f8f9fa',
                color: isUser ? 'white' : '#111827',
                padding: '8px 12px',
                borderRadius: '16px',
                marginLeft: isUser ? '48px' : '0px',
                marginRight: isUser ? '0px' : '48px',
                maxWidth: '280px',
                wordWrap: 'break-word',
                border: isUser ? 'none' : '1px solid #e1e5e9',
                boxShadow: isUser ? '0 1px 2px rgba(0,0,0,0.1)' : 'none'
              }}
            >
              <div className="text-sm leading-relaxed break-words overflow-wrap-anywhere">
                {message.content}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function ChatWindow() {
  const { state } = useChatContext();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [state.messages]);

  return (
    <div className="flex-1 overflow-y-auto">
      {state.messages.length === 0 ? (
        <div className="h-full flex items-center justify-center bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
          <div className="text-center max-w-md mx-auto px-4">
            <div className="w-20 h-20 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-3">How can I help you today?</h1>
            <p className="text-gray-600 text-lg">Start a conversation by typing a message below.</p>
          </div>
        </div>
      ) : (
        <div>
          {state.messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
          
          {/* Loading indicator */}
          {state.status === "streaming" && (
            <div className="py-2 bg-white">
              <div className="max-w-4xl mx-auto px-4">
                <div className="flex justify-start">
                  <div className="max-w-xs lg:max-w-md mr-12">
                    <div className="px-4 py-2 bg-gray-200 rounded-2xl rounded-bl-md">
                      <div className="flex items-center space-x-1">
                        <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: "0.1s" }}></div>
                        <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      )}
    </div>
  );
}