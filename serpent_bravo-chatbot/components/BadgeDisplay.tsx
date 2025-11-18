import React from 'react';
import { Badge } from '../types';

interface BadgeDisplayProps {
  badge: Badge;
}

const BadgeDisplay: React.FC<BadgeDisplayProps> = ({ badge }) => {
  const Icon = badge.icon;
  return (
    <div className="mt-4">
        <div className="bg-green-50 dark:bg-gray-800 border-2 border-dashed border-green-500 rounded-lg p-4 flex items-center space-x-4">
            <div className="flex-shrink-0">
                <Icon className="h-12 w-12 text-green-500" />
            </div>
            <div>
                <h3 className="font-bold text-green-800 dark:text-green-300">Badge Unlocked: {badge.name}</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">{badge.description}</p>
                <p className="text-sm font-semibold text-green-600 dark:text-green-400 mt-1">+{badge.points} points!</p>
            </div>
        </div>
    </div>
  );
};

export default BadgeDisplay;
