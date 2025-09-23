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
    // ^ Returns JSX to render the sidebar UI.
    <div className="h-full bg-gray-50 border-r border-gray-200 flex flex-col">
      {/* Root container: full height, light gray bg, right border, vertical layout */}
      
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        {/* Top header area with padding and bottom border */}
        <button
          onClick={handleNewChat}
          // ^ Clicking this triggers CLEAR_MESSAGES via the handler above.
          className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 text-sm font-medium transition-colors"
        >
          {/* Full-width primary button with Tailwind styles and hover color */}
          + New Chat
          {/* Button label */}
        </button>
      </div>

      {/* Conversation List */}
      <div className="flex-1 overflow-y-auto">
        {/* Middle area grows to fill space; scrolls if content is tall */}
        {hasMessages ? (
          // ^ Conditional render: if there are messages, show a “Current Chat” card…
          <div className="p-2">
            {/* Small padding around the card */}
            <div className="bg-white rounded-lg p-3 mb-2 border border-gray-200 bg-blue-50 border-blue-200">
              {/* A card with rounded corners and (note: both white and blue-50 are listed;
                  the last one wins, so this ends up blue-50 with a blue border) */}
              <div className="text-sm font-medium text-gray-900 mb-1">
                {/* Title text for the card */}
                Current Chat
              </div>
              <div className="text-xs text-gray-600">
                {/* Subtext showing message count with pluralization */}
                {messageCount} message{messageCount !== 1 ? 's' : ''}
                {/* ^ If count is not 1, append 's' to pluralize. */}
              </div>
            </div>
          </div>
        ) : (
          // …else (no messages) show an empty state.
          <div className="p-4 text-center text-gray-500 text-sm">
            {/* Centered, muted text as an empty-state hint */}
            No conversations yet.<br />
            {/* ^ <br /> inserts a line break. */}
            Start a new chat to begin!
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200">
        {/* Bottom footer with padding and top border */}
        <div className="text-xs text-gray-500 text-center">
          {/* Small, muted, centered label */}
          VenueKonnex Chat
        </div>
      </div>
    </div>
  );
  // ^ End of the component’s returned JSX.
}
