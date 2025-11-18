import React, { useRef, useEffect } from 'react';
import { Message, Rank } from '../types';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { BotIcon } from './icons';
import SuggestionChips from './SuggestionChips';

interface ChatInterfaceProps {
  messages: Message[];
  onSendMessage: (text: string) => void;
  isLoading: boolean;
  error: string | null;
  suggestions: string[];
  rank: Rank;
  points: number;
  image: { data: string; mimeType: string; } | null;
  onSetImage: (image: { data: string; mimeType: string; } | null) => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ messages, onSendMessage, isLoading, error, suggestions, rank, points, image, onSetImage }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto w-full">
      <header className="bg-white dark:bg-gray-800 p-4 border-b border-gray-200 dark:border-gray-700 shadow-sm sticky top-0 z-10">
        <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-green-500 p-2 rounded-full">
                <BotIcon className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-800 dark:text-white">Serpent_Bravo</h1>
                <p className="text-sm text-green-600 dark:text-green-400 font-medium">Your guide to a greener planet</p>
              </div>
            </div>
            <div className="text-right">
                <div className="text-sm font-bold text-gray-800 dark:text-white flex items-center gap-2 justify-end">
                    <span>{rank.icon} {rank.name}</span>
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-400">{points} points</p>
            </div>
        </div>
      </header>
      
      <main className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}
        {isLoading && (
          <div className="flex justify-start">
             <div className="flex items-center space-x-3">
              <div className="bg-gray-200 dark:bg-gray-700 p-2 rounded-full">
                <BotIcon className="h-8 w-8 text-gray-500" />
              </div>
              <div className="bg-gray-200 dark:bg-gray-700 rounded-2xl p-3 max-w-lg">
                <div className="flex items-center space-x-2">
                    <span className="h-2 w-2 bg-green-500 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                    <span className="h-2 w-2 bg-green-500 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                    <span className="h-2 w-2 bg-green-500 rounded-full animate-bounce"></span>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      <footer className="bg-white dark:bg-gray-800 p-2 md:p-4 border-t border-gray-200 dark:border-gray-700 sticky bottom-0">
        <SuggestionChips suggestions={suggestions} onSuggestionClick={onSendMessage} />
        <ChatInput onSendMessage={onSendMessage} isLoading={isLoading} image={image} onSetImage={onSetImage} />
      </footer>
    </div>
  );
};

export default ChatInterface;