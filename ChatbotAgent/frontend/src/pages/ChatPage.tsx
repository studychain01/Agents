import { ChatProvider } from "../state/ChatContext";
import ChatWindow from "../components/ChatWindow";
import ChatComposer from "../components/ChatComposer";
import ConversationList from "../components/ConversationList.tsx";

export default function ChatPage() {
  return (
    <ChatProvider>
      <div className="grid grid-cols-[280px_1fr] h-screen">
        <ConversationList />
        <div className="flex flex-col">
          <ChatWindow />
          <ChatComposer />
        </div>
      </div>
    </ChatProvider>
  );
}
