
import React, { useState, useRef } from 'react';
import { SendIcon, CameraIcon, XCircleIcon } from './icons';

interface ChatInputProps {
  onSendMessage: (text: string) => void;
  isLoading: boolean;
  image: { data: string; mimeType: string; } | null;
  onSetImage: (image: { data: string; mimeType: string; } | null) => void;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading, image, onSetImage }) => {
  const [text, setText] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        onSetImage({
          data: e.target?.result as string,
          mimeType: file.type,
        });
      };
      reader.readAsDataURL(file);
    }
  };

  const handleCameraClick = () => {
    fileInputRef.current?.click();
  };
  
  const handleRemoveImage = () => {
    onSetImage(null);
    if(fileInputRef.current) {
        fileInputRef.current.value = "";
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if ((text.trim() || image) && !isLoading) {
      onSendMessage(text);
      setText('');
    }
  };

  return (
    <div className="flex flex-col">
      {image && (
        <div className="relative self-start mb-2 ml-14 p-2 bg-gray-200 dark:bg-gray-700 rounded-lg">
          <img src={image.data} alt="Image preview" className="h-24 w-auto rounded-md" />
          <button
            onClick={handleRemoveImage}
            className="absolute -top-2 -right-2 bg-gray-700 dark:bg-gray-200 text-white dark:text-gray-800 rounded-full p-0.5"
            aria-label="Remove image"
          >
            <XCircleIcon className="h-5 w-5" />
          </button>
        </div>
      )}
      <form onSubmit={handleSubmit} className="flex items-center space-x-2 md:space-x-4">
        <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            className="hidden"
            accept="image/*"
            capture="environment"
        />
        <button
            type="button"
            onClick={handleCameraClick}
            disabled={isLoading}
            className="p-3 rounded-full text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
            aria-label="Attach image"
        >
            <CameraIcon className="h-6 w-6" />
        </button>
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={image ? "Add a comment..." : "Ask about your carbon footprint..."}
          disabled={isLoading}
          className="flex-1 p-3 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50"
          autoFocus
        />
        <button
          type="submit"
          disabled={isLoading || (!text.trim() && !image)}
          className="p-3 rounded-full bg-green-500 text-white hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:bg-green-300 dark:disabled:bg-gray-600 disabled:cursor-not-allowed transition-colors"
        >
          <SendIcon className="h-6 w-6" />
        </button>
      </form>
    </div>
  );
};

export default ChatInput;