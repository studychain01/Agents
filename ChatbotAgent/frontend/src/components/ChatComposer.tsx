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
        <div className="bg-white border-t border-gray-200">
          <div className="max-w-4xl mx-auto px-6 py-4">
            <div className="flex items-end space-x-3">
              <div className="flex-1">
                <div className="relative">
                  <textarea
                    ref={textareaRef}
                    value={message}
                    onChange={(e) => {
                      setMessage(e.target.value);
                      adjustTextareaHeight();
                    }}
                    onKeyDown={handleKeyDown}
                    placeholder={isDisabled ? "AI is thinking..." : "Type your message..."}
                    disabled={isDisabled}
                    className="w-full resize-none rounded-2xl border border-gray-300 px-4 py-3 pr-12 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 disabled:bg-gray-50 disabled:text-gray-500 transition-colors"
                    rows={1}
                    style={{ minHeight: "48px", maxHeight: "120px" }}
                  />
                  <div className="absolute right-3 bottom-3 text-xs text-gray-400">
                    {isDisabled ? "" : "⏎ to send"}
                  </div>
                </div>
              </div>

              <button
                onClick={handleSubmit}
                disabled={!message.trim() || isDisabled}
                className="flex-shrink-0 w-12 h-12 rounded-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
              >
                {isDisabled ? (
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                ) : (
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                )}
              </button>
            </div>
            
            {state.error && (
              <div className="mt-3 p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-center space-x-2">
                  <svg className="w-4 h-4 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                  <span>Error: {state.error}</span>
                </div>
              </div>
            )}
          </div>
        </div>
    );
}