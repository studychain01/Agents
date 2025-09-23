import { useState, useRef, KeyboardEvent} from "react";
import { useChatContext, genId } from "../state/ChatContext";

export default function ChatComposer() {
    const { state, dispatch } = useChatContext();
    const [message, setMessage] = useState("");
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const isDisabled = state.status === "streaming";

    const handleSubmit = () => {
        const trimmedMessage = message.trim();
        if(!trimmedMessage || isDisabled) return;

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

        dispatch({type: "SET_STATUS", status: "streaming"});

        setTimeout(() => {
            dispatch({
                type: "ADD_MESSAGE",
                msg: {
                    id: genId(),
                    role: "assistant",
                    content: `I received your message: "${trimmedMessage}"\n\nThis is a demo response. In a real implementation, this would connect to an AI service to generate meaningful responses.`,
                    createdAt: Date.now(),
                  },
            });
            dispatch({type: "SET_STATUS", status: "idle"});
        }, 1500);
    };
    
    const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if(e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };
    
    const adjustTextareaHeight = () => {
      const textarea = textareaRef.current;
      if(textarea) {
        textarea.style.height = "auto";
        textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`;
      }
    };

    return (
        <div className="border-t border-gray-200 bg-white p-4">
          <div className="flex items-center space-x-3">
            <div className="flex-1">
              <textarea
                ref={textareaRef}
                value={message}
                onChange={(e) => {
                  setMessage(e.target.value);
                  adjustTextareaHeight();
                }}
                onKeyDown={handleKeyDown}
                placeholder={isDisabled ? "Thinking..." : "Type a message..."}
                disabled={isDisabled}
                className="w-full resize-none rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-50 disabled:text-gray-500"
                rows={1}
                style={{ minHeight: "40px", maxHeight: "120px" }}
              />
              <div className="mt-1 text-xs text-gray-500">
                Press Enter to send, Shift+Enter for new line
              </div>
            </div>

            <button
              onClick={handleSubmit}
              disabled={!message.trim() || isDisabled}
              className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-300 disabled:cursor-not-allowed"
              style={{ minHeight: "40px" }}
            >
              {isDisabled ? (
                <div className="flex items-center space-x-1">
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                </div>
             ) : (
                "Send"
             )}
            </button>
        </div>
      
        {state.error && (
          <div className="mt-2 text-sm text-red-600 bg-red-50 border border-red-200 rounded px-3 py-2">
            Error: {state.error}
          </div>
        )}
      </div>
    );
}