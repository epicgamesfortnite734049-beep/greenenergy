import React, { useEffect, useState } from 'react';
import { Notification as NotificationType } from '../types';

interface NotificationProps {
  notification: NotificationType;
  onClose: () => void;
}

const Notification: React.FC<NotificationProps> = ({ notification, onClose }) => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    // Component did mount, trigger enter animation
    setVisible(true);

    const timer = setTimeout(() => {
      // Trigger exit animation
      setVisible(false);
    }, 4000); // Display for 4 seconds

    const closeTimer = setTimeout(() => {
        // Unmount component after exit animation
        onClose();
    }, 4500); // Should be longer than the transition duration

    return () => {
      clearTimeout(timer);
      clearTimeout(closeTimer);
    };
  }, [onClose]);

  return (
    <div
      className={`
        pointer-events-auto flex w-full max-w-sm items-center space-x-3 rounded-lg bg-white p-4 shadow-lg ring-1 ring-black ring-opacity-5 
        dark:bg-gray-800 dark:ring-white dark:ring-opacity-10
        transform transition-all duration-500 ease-in-out
        ${visible ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'}
      `}
      role="alert"
    >
      <div className="flex-shrink-0">
        {notification.icon}
      </div>
      <div className="flex-1">
        <p className="text-sm font-medium text-gray-900 dark:text-white">{notification.message}</p>
      </div>
    </div>
  );
};

export default Notification;
