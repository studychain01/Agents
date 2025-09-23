import { useState, useRef, KeyboardEvent } from "react";
import { useChatContext, genId } from "../state/ChatContext";
import { sendChatMessage } from "../services/chatService";

export function ChatComposer() {
  const { state, dispatch } = useChatContext();
  const [message, setMessage] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const isDisabled = state.status === "streaming";

  const handleSubmit = async () => {
    const trimmedMessage = message.trim();
    if (!trimmedMessage || isDisabled) return;

    dispatch({
      type: "ADD_MESSAGE",
      msg: {
        id: genId(),
        role: "user",
        content: trimmedMessage,
        createdAt: Date.now()
      },
    });

    setMessage("");
    dispatch({ type: "SET_STATUS", status: "streaming" });

    try {
      const response = await sendChatMessage(trimmedMessage);
      dispatch({
        type: "ADD_MESSAGE",
        msg: {
          id: genId(),
          role: "assistant",
          content: response.response || "Sorry, I couldn't generate a response.",
          createdAt: Date.now(),
        },
      });
    } catch (error) {
      dispatch({
        type: "ADD_MESSAGE",
        msg: {
          id: genId(),
          role: "assistant",
          content: "Sorry, there was an error connecting to the AI service.",
          createdAt: Date.now(),
        },
      });
      dispatch({ type: "SET_STATUS", status: "error", error: error instanceof Error ? error.message : "Unknown error" });
    } finally {
      dispatch({ type: "SET_STATUS", status: "idle" });
    }
  };
  
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };
  
  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`;
    }
  };

  return (
    <div className="border-t border-gray-200 bg-white">
      <div className="max-w-2xl mx-auto px-4 py-3">
        <div className="flex items-end gap-2">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => {
              setMessage(e.target.value);
              adjustTextareaHeight();
            }}
            onKeyDown={handleKeyDown}
            placeholder="Type a message..."
            disabled={isDisabled}
            className="flex-1 resize-none rounded-2xl border border-gray-300 px-3 py-2 text-sm focus:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-100 disabled:bg-gray-50 disabled:text-gray-500 transition-all"
            rows={1}
            style={{ minHeight: "36px", maxHeight: "100px" }}
          />
          
          <button
            onClick={handleSubmit}
            disabled={!message.trim() || isDisabled}
            className="w-9 h-9 rounded-full bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center flex-shrink-0"
            style={{
              backgroundColor: !message.trim() || isDisabled ? '#d1d5db' : '#3b82f6',
              minWidth: '36px',
              minHeight: '36px'
            }}
          >
            {isDisabled ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            ) : (
              <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            )}
          </button>
        </div>
        
        {state.error && (
          <div className="mt-3 p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg">
            Error: {state.error}
          </div>
        )}
      </div>
    </div>
  );
}