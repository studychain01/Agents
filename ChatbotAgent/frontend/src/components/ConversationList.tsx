import { useChatContext } from "../state/ChatContext";

export function ConversationList() {
  const { state, dispatch } = useChatContext();

  const handleNewChat = () => {
    dispatch({ type: "CLEAR_MESSAGES" });
  };

  const messageCount = state.messages.length;
  const hasMessages = messageCount > 0;

  return (
    <div className="h-full flex flex-col bg-gray-900 text-white">
      {/* Header */}
      <div className="p-4 border-b border-gray-700">
        <button
          onClick={handleNewChat}
          className="w-full bg-gray-800 hover:bg-gray-700 text-white rounded-lg px-4 py-3 text-base font-medium transition-colors flex items-center justify-center space-x-2"
        >
          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          <span>New chat</span>
        </button>
      </div>

      {/* Conversation List */}
      <div className="flex-1 overflow-y-auto">
        <div className="p-6 text-center">
          <div className="w-12 h-12 bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <p className="text-base text-gray-400">
            No conversations yet.<br />
            Start a new chat to begin!
          </p>
        </div>
      </div>

      {/* Current Conversation Info - Right above footer line */}
      {hasMessages && (
        <div className="px-4 pb-0 text-center">
          <div className="text-sm text-gray-300">
            Current conversation
          </div>
          <div className="text-xs text-gray-500">
            {messageCount} message{messageCount !== 1 ? 's' : ''}
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="p-4 border-t border-gray-700">
        <div className="text-xs text-gray-500 text-center">
          AI Assistant
        </div>
      </div>
    </div>
  );
}