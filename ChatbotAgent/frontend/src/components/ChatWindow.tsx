import { useEffect, useRef } from "react";
import { useChatContext, type Message } from "../state/ChatContext";

interface MessageBubbleProps {
  message: Message;
}

function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";
  const isSystem = message.role === "system";
  
  return (
    <div className={`flex mb-4 ${isUser ? "justify-end" : "justify-start"}`}>
      <div className={`max-w-[70%] rounded-lg px-4 py-2 ${
        isUser 
          ? "bg-blue-600 text-white" 
          : isSystem
          ? "bg-yellow-100 text-yellow-800 border border-yellow-200"
          : "bg-gray-100 text-gray-900"
      }`}>
        {/* Role indicator for non-user messages */}
        {!isUser && (
          <div className="text-xs font-medium mb-1 opacity-70 capitalize">
            {message.role}
          </div>
        )}
        
        {/* Message content */}
        <div className="whitespace-pre-wrap break-words">
          {message.content}
        </div>
        
        {/* Timestamp */}
        <div className={`text-xs mt-1 opacity-70 ${
          isUser ? "text-blue-100" : "text-gray-500"
        }`}>
          {new Date(message.createdAt).toLocaleTimeString()}
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
    <div className="flex-1 overflow-y-auto p-4 bg-white">
      {state.messages.length === 0 ? (
        <div className="h-full flex items-center justify-center">
          <div className="text-center text-gray-500">
            <div className="text-lg font-medium mb-2">Welcome to VenueKonnex Chat</div>
            <div className="text-sm">Start a conversation by typing a message below.</div>
          </div>
        </div>
      ) : (
        <div className="space-y-0">
          {state.messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
          
          {/* Loading indicator when streaming */}
          {state.status === "streaming" && (
            <div className="flex justify-start mb-4">
              <div className="bg-gray-100 rounded-lg px-4 py-2">
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0.1s" }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
                </div>
              </div>
            </div>
          )}
          
          {/* Scroll anchor */}
          <div ref={messagesEndRef} />
        </div>
      )}
    </div>
  );
}
