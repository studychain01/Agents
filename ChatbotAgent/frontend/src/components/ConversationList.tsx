import { useChatContext } from "../state/ChatContext";
// ^ Imports the custom React hook that gives you { state, dispatch } from your ChatContext provider.

export default function ConversationList() {
// ^ Declares and exports a React function component named ConversationList.

  const { state, dispatch } = useChatContext();
  // ^ Calls your context hook to access:
  //   - state: the current chat state (messages, status, etc.)
  //   - dispatch: a function to send actions to the reducer

  const handleNewChat = () => {
    dispatch({ type: "CLEAR_MESSAGES" });
  };
  // ^ Event handler for the “New Chat” button.
  //   Dispatches the CLEAR_MESSAGES action (your reducer should wipe state.messages).

  const messageCount = state.messages.length;
  // ^ Derives how many messages exist in the current conversation.

  const hasMessages = messageCount > 0;
  // ^ Boolean flag: true if there’s at least one message.

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <button
          onClick={handleNewChat}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-3 text-sm font-medium transition-colors flex items-center justify-center space-x-2"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          <span>New Chat</span>
        </button>
      </div>

      {/* Conversation List */}
      <div className="flex-1 overflow-y-auto">
        {hasMessages ? (
          <div className="p-3">
            <div className="bg-blue-50 rounded-lg p-3 border border-blue-200">
              <div className="text-sm font-medium text-blue-900 mb-1">
                Current Chat
              </div>
              <div className="text-xs text-blue-600">
                {messageCount} message{messageCount !== 1 ? 's' : ''}
              </div>
            </div>
          </div>
        ) : (
          <div className="p-6 text-center">
            <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <p className="text-sm text-gray-500">
              No conversations yet.<br />
              Start a new chat to begin!
            </p>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200">
        <div className="text-xs text-gray-500 text-center">
          AI Assistant
        </div>
      </div>
    </div>
  );
  // ^ End of the component’s returned JSX.
}
