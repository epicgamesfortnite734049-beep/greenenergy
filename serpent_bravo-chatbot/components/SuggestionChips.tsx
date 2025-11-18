import React from 'react';

interface SuggestionChipsProps {
  suggestions: string[];
  onSuggestionClick: (suggestion: string) => void;
}

const SuggestionChips: React.FC<SuggestionChipsProps> = ({ suggestions, onSuggestionClick }) => {
  if (suggestions.length === 0) {
    return null;
  }

  return (
    <div className="flex flex-wrap gap-2 justify-center mb-3 px-2">
      {suggestions.map((suggestion, index) => (
        <button
          key={index}
          onClick={() => onSuggestionClick(suggestion)}
          className="px-4 py-2 text-sm font-medium text-green-700 bg-green-100 border border-green-200 rounded-full hover:bg-green-200 dark:bg-gray-700 dark:text-green-300 dark:border-gray-600 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500 transition-colors"
          aria-label={`Suggestion: ${suggestion}`}
        >
          {suggestion}
        </button>
      ))}
    </div>
  );
};

export default SuggestionChips;
