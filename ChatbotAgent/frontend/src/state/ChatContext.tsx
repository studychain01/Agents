/**
 * ChatContext.tsx - Chat State Management
 * 
 * This file provides a complete chat state management solution using React Context + useReducer.
 * Features:
 * - Type-safe message handling with Redux-style actions
 * - Automatic localStorage persistence (survives page refresh)
 * - Support for AI assistants (user/assistant/system/tool roles)
 * - Streaming status management
 * - Configurable AI settings (model, temperature, system prompt)
 * 
 * Usage:
 * 1. Wrap your app with <ChatProvider>
 * 2. Use useChatContext() in components to access state and dispatch
 */

import React, { createContext, useContext, useEffect, useMemo, useReducer } from "react";

/* ========= Types ========= */

/**
 * Message roles for different types of chat participants
 * - user: Human user messages
 * - assistant: AI assistant responses (ChatGPT, Claude, etc.)
 * - system: System messages (instructions, notifications)
 * - tool: Tool/function call results
 */
export type Role = "user" | "assistant" | "system" | "tool";

/**
 * Core message structure for all chat messages
 */
export interface Message {
  id: string;                // Unique identifier for each message
  role: Role;                // Who sent the message (user, assistant, etc.)
  content: string;           // Message text (markdown allowed for assistant/tool)
  createdAt: number;         // Timestamp when message was created (Date.now())
  metadata?: Record<string, unknown>; // Optional extra data (file attachments, etc.)
}

/**
 * Chat status for UI feedback
 * - idle: No active chat operation
 * - streaming: AI is currently generating a response
 * - error: Something went wrong with the last operation
 */
type Status = "idle" | "streaming" | "error";

/**
 * AI configuration settings
 */
export interface ChatSettings {
  model?: string;           // AI model to use (e.g., "gpt-4o-mini", "claude-3-sonnet")
  temperature?: number;     // AI creativity level (0.0 = deterministic, 1.0 = creative)
  systemPrompt?: string;    // Instructions that define AI behavior and personality
}

/**
 * Complete chat state structure
 */
export interface ChatState {
  messages: Message[];      // Array of all chat messages in chronological order
  status: Status;           // Current operation status for UI feedback
  error?: string;           // Error message if something went wrong
  settings: ChatSettings;   // AI configuration settings
}

/* ========= Actions ========= */

/**
 * Redux-style actions for state updates
 * All state changes must go through these actions for predictability
 */
type Action =
  | { type: "ADD_MESSAGE"; msg: Message }                              // Append new message to chat
  | { type: "PATCH_MESSAGE"; id: string; patch: Partial<Message> }     // Update existing message (for streaming)
  | { type: "CLEAR_MESSAGES" }                                         // Remove all messages
  | { type: "SET_STATUS"; status: Status; error?: string }             // Update chat status/error
  | { type: "SET_SETTINGS"; patch: Partial<ChatSettings> };            // Update AI settings

/* ========= Persistence Keys ========= */

/**
 * localStorage key for persisting chat state
 * Versioned (v1) to handle future data structure changes
 */
const LS_KEY = "chat.state.v1";

/* ========= Reducer ========= */

/**
 * Pure reducer function that handles all state updates
 * Follows Redux patterns for predictable state management
 * 
 * @param state - Current chat state
 * @param action - Action describing what change to make
 * @returns New state (never mutates existing state)
 */
function reducer(state: ChatState, action: Action): ChatState {
  switch (action.type) {
    // Add a new message to the end of the conversation
    case "ADD_MESSAGE":
      return {
        ...state,
        messages: [...state.messages, action.msg], // Immutable append
      };

    // Update an existing message (useful for streaming responses)
    case "PATCH_MESSAGE": {
      const messages = state.messages.map((m) =>
        m.id === action.id ? { ...m, ...action.patch } : m // Only update matching message
      );
      return { ...state, messages };
    }

    // Remove all messages (fresh start)
    case "CLEAR_MESSAGES":
      return { ...state, messages: [] };

    // Update chat status and optionally set error message
    case "SET_STATUS":
      return { ...state, status: action.status, error: action.error };

    // Merge new settings with existing ones
    case "SET_SETTINGS":
      return { ...state, settings: { ...state.settings, ...action.patch } };

    // TypeScript exhaustiveness check - should never happen
    default:
      return state;
  }
}

/* ========= Context ========= */

/**
 * React Context for chat state
 * Provides state and dispatch function to child components
 */
const ChatCtx = createContext<{
  state: ChatState;               // Current chat state
  dispatch: React.Dispatch<Action>; // Function to trigger state changes
} | null>(null);

/* ========= Provider ========= */

/**
 * Default chat state when starting fresh
 */
const initialState: ChatState = {
  messages: [],                   // Start with empty conversation
  status: "idle",                 // Not doing anything initially
  error: undefined,               // No errors to start
  settings: {
    model: "gpt-4o-mini",         // Default AI model (pick your favorite)
    temperature: 0.7,             // Balanced creativity (0.0 = deterministic, 1.0 = creative)
    systemPrompt: undefined,      // No default system instructions
  },
};

/**
 * Load chat state from localStorage with error handling
 * Falls back to initialState if anything goes wrong
 * 
 * @returns ChatState from localStorage or default state
 */
function loadState(): ChatState {
  try {
    const raw = localStorage.getItem(LS_KEY);
    if (!raw) return initialState; // No saved data, use defaults
    
    const parsed = JSON.parse(raw) as ChatState;
    
    // Defensive programming: ensure data structure is valid
    // This prevents crashes when localStorage has old/corrupted data
    return {
      ...initialState,            // Start with safe defaults
      ...parsed,                  // Override with saved data
      messages: Array.isArray(parsed.messages) ? parsed.messages : [], // Ensure messages is array
      settings: { ...initialState.settings, ...(parsed.settings ?? {}) }, // Merge settings safely
    };
  } catch {
    // JSON.parse failed or other error - use safe defaults
    return initialState;
  }
}

/**
 * ChatProvider component that wraps your app to provide chat state
 * 
 * Usage:
 * <ChatProvider>
 *   <YourApp />
 * </ChatProvider>
 */
export function ChatProvider({ children }: { children: React.ReactNode }) {
  // Initialize state with useReducer, loading from localStorage on first render
  const [state, dispatch] = useReducer(reducer, undefined, loadState);

  // Auto-save state to localStorage whenever it changes
  // This ensures chat history persists across browser sessions
  useEffect(() => {
    try {
      localStorage.setItem(LS_KEY, JSON.stringify(state));
    } catch {
      // localStorage.setItem can fail due to:
      // - Storage quota exceeded
      // - Private browsing mode
      // - Browser security settings
      // Silently ignore these errors to prevent app crashes
    }
  }, [state]);

  // Memoize context value to prevent unnecessary re-renders
  // Only creates new object when state actually changes
  const value = useMemo(() => ({ state, dispatch }), [state]);
  
  return <ChatCtx.Provider value={value}>{children}</ChatCtx.Provider>;
}

/* ========= Hook ========= */

/**
 * Custom hook to access chat state and dispatch
 * Must be used within a <ChatProvider> or will throw an error
 * 
 * @returns Object with current state and dispatch function
 * @throws Error if used outside ChatProvider
 * 
 * Example:
 * const { state, dispatch } = useChatContext();
 * dispatch({ type: "ADD_MESSAGE", msg: newMessage });
 */
export function useChatContext() {
  const ctx = useContext(ChatCtx);
  if (!ctx) {
    throw new Error("useChatContext must be used within <ChatProvider>");
  }
  return ctx;
}

/* ========= Helpers ========= */

/**
 * Generate a unique ID for messages
 * Uses crypto.randomUUID() if available (modern browsers)
 * Falls back to Math.random() for compatibility
 * 
 * @returns Unique string ID
 */
export function genId() {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID(); // Cryptographically secure, proper UUID format
  }
  // Fallback: not cryptographically secure but good enough for UI purposes
  return Math.random().toString(36).slice(2);
}
