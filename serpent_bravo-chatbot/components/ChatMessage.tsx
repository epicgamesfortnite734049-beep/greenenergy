import React from 'react';
import { Message } from '../types';
import { BotIcon } from './icons';
import BadgeDisplay from './BadgeDisplay';
import CarbonChart from './CarbonChart';
import CarbonReceipt from './CarbonReceipt';

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.sender === 'user';

  return (
    <div className={`flex items-end gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className="flex-shrink-0 bg-green-500 p-2 rounded-full self-start">
            <BotIcon className="h-6 w-6 text-white" />
        </div>
      )}
      <div
        className={`rounded-2xl p-3 max-w-lg w-full flex flex-col ${
          isUser
            ? 'bg-blue-500 text-white rounded-br-none'
            : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-bl-none'
        }`}
      >
        {message.imageUrl && (
            <img 
                src={message.imageUrl} 
                alt="User upload" 
                className="rounded-lg mb-2 max-h-64 w-full object-contain" 
            />
        )}
        
        {message.isCarbonReceipt 
            ? <CarbonReceipt text={message.text} />
            : message.text && <p className="text-sm md:text-base whitespace-pre-wrap">{message.text}</p>
        }
        
        {message.chartData && <CarbonChart data={message.chartData} title={message.chartTitle || 'Your CO₂ Footprint Breakdown'} />}
        {message.badge && <BadgeDisplay badge={message.badge} />}
      </div>
    </div>
  );
};

export default ChatMessage;