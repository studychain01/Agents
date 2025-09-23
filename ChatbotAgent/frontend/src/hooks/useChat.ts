/**
 * useChat.ts - Custom Hook for Chat Operations
 * 
 * This hook provides a simple interface for chat functionality while hiding
 * the complexity of state management. It implements optimistic UI patterns
 * and is designed to work with streaming AI responses.
 * 
 * Features:
 * - Optimistic UI updates (messages appear instantly)
 * - Streaming response support (can update messages incrementally)
 * - Error handling with user feedback
 * - Simple API for components
 * 
 * Usage:
 * const { messages, status, sendMessage, clear } = useChat();
 */

import { useChatContext, genId } from "../state/ChatContext";
import { sendChatMessage } from "../services/chatService";

/**
 * Custom hook that provides chat functionality to components
 * Abstracts away the complex state management and provides simple functions
 * 
 * @returns Object with chat state and action functions
 */
export function useChat() {
  // Get state and dispatch from the ChatContext
  const { state, dispatch } = useChatContext();

  /**
   * Send a message to the chat
   * Implements optimistic UI pattern - user message appears immediately
   * Creates a placeholder for assistant response that gets updated when response arrives
   * 
   * @param text - The message text to send
   */
  async function sendMessage(text: string) {
    // Step 1: Immediately add user message (Optimistic UI)
    // This makes the UI feel responsive - no waiting for server
    const userMsg = { 
      id: genId(), 
      role: "user" as const, 
      content: text, 
      createdAt: Date.now() 
    };
    dispatch({ type: "ADD_MESSAGE", msg: userMsg });
    
    // Step 2: Set status to streaming to show loading state
    dispatch({ type: "SET_STATUS", status: "streaming" });

    // Step 3: Create empty assistant message that we'll update with the response
    // This is perfect for streaming responses where content arrives incrementally
    const draftId = genId();
    dispatch({
      type: "ADD_MESSAGE",
      msg: { 
        id: draftId, 
        role: "assistant", 
        content: "", // Empty initially, will be filled with response
        createdAt: Date.now() 
      },
    });

    try {
      // Step 4: Send message to API and wait for response
      const { reply } = await sendChatMessage(text);
      
      // Step 5: Update the empty assistant message with the actual response
      // For streaming responses, you would call PATCH_MESSAGE multiple times
      // as chunks arrive, building up the content incrementally
      dispatch({ type: "PATCH_MESSAGE", id: draftId, patch: { content: reply } });
      
      // Step 6: Reset status to idle (conversation ready for next message)
      dispatch({ type: "SET_STATUS", status: "idle" });
      
    } catch (e) {
      // Error handling: Set error status and show user-friendly error message
      dispatch({ 
        type: "SET_STATUS", 
        status: "error", 
        error: (e as Error).message 
      });
      
      // Replace the empty assistant message with an error indicator
      // This prevents having an empty message bubble in the UI
      dispatch({ 
        type: "PATCH_MESSAGE", 
        id: draftId, 
        patch: { content: "⚠️ Error from server." } 
      });
    }
  }

  /**
   * Clear all messages from the chat
   * Useful for starting a fresh conversation
   */
  function clear() {
    dispatch({ type: "CLEAR_MESSAGES" });
  }

  /**
   * Update AI settings (model, temperature, system prompt)
   * Allows users to customize AI behavior
   * 
   * @param patch - Partial settings object to merge with existing settings
   */
  function updateSettings(patch: Partial<{ model: string; temperature: number; systemPrompt: string }>) {
    dispatch({ type: "SET_SETTINGS", patch });
  }

  // Return the complete chat state plus action functions
  // Components get everything they need in one object
  return { 
    ...state,        // messages, status, error, settings
    sendMessage,     // Function to send new messages
    clear,           // Function to clear conversation
    updateSettings   // Function to update AI settings
  };
}
