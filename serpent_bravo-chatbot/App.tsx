

import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { Message, Badge, Rank, ChartDataPoint, Notification as NotificationType } from './types';
import ChatInterface from './components/ChatInterface';
import Notification from './components/Notification';
import { sendMessageToAI } from './services/geminiService';
import { BADGES, RANKS } from './data/gamification';

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'initial-message',
      text: "Hello! I'm Serpent_Bravo, your friendly guide to a greener planet. 🌍 I can help you understand your carbon footprint, share fun facts about our environment, or give you simple tips to make a positive impact. What's on your mind today?",
      sender: 'ai',
    },
  ]);
  const [suggestions, setSuggestions] = useState<string[]>([
    'Calculate my carbon footprint',
    'How can I reduce plastic use?',
    "What's the footprint of an item?",
  ]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [image, setImage] = useState<{ data: string; mimeType: string; } | null>(null);

  // Gamification state
  const [points, setPoints] = useState<number>(0);
  const [unlockedBadges, setUnlockedBadges] = useState<string[]>([]);

  // Notification state
  const [notifications, setNotifications] = useState<NotificationType[]>([]);

  const currentRank = useMemo(() => {
    return [...RANKS].reverse().find(rank => points >= rank.minPoints) || RANKS[0];
  }, [points]);

  // --- Notification Logic ---
  const addNotification = useCallback((message: string, icon: React.ReactNode) => {
    const id = Date.now().toString() + Math.random();
    setNotifications(prev => [...prev, { id, message, icon }]);
  }, []);

  const removeNotification = useCallback((id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  }, []);
  
  // Effect for rank up notifications
  const prevRank = useRef<Rank>(currentRank);
  useEffect(() => {
    if (currentRank.name !== prevRank.current.name) {
      addNotification(`Rank Up: You are now an ${currentRank.name}!`, <span>{currentRank.icon}</span>);
    }
    prevRank.current = currentRank;
  }, [currentRank, addNotification]);

  // Effect for badge unlock notifications
  const prevUnlockedBadgesCount = useRef(unlockedBadges.length);
  useEffect(() => {
    if (unlockedBadges.length > prevUnlockedBadgesCount.current) {
      const newBadgeId = unlockedBadges[unlockedBadges.length - 1];
      const newBadge = BADGES[newBadgeId];
      if (newBadge) {
        addNotification(`Badge Unlocked: ${newBadge.name}!`, <newBadge.icon className="h-6 w-6 text-yellow-500" />);
      }
    }
    prevUnlockedBadgesCount.current = unlockedBadges.length;
  }, [unlockedBadges, addNotification]);
  // --- End Notification Logic ---

  const processAiResponse = useCallback((responseText: string): { cleanedText: string; awardedBadge?: Badge; chartData?: ChartDataPoint[]; chartTitle?: string; isCarbonReceipt?: boolean } => {
    let text = responseText;
    let awardedBadge: Badge | undefined = undefined;
    let chartData: ChartDataPoint[] | undefined = undefined;
    let chartTitle: string | undefined = undefined;
    let isCarbonReceipt: boolean | undefined = undefined;

    // Carbon Receipt Check (must be first, as it's a primary display type)
    const receiptRegex = /\[CARBON_RECEIPT\]\r?\n?([\s\S]*)/;
    const receiptMatch = text.match(receiptRegex);
    if (receiptMatch) {
      return { cleanedText: receiptMatch[1].trim(), isCarbonReceipt: true };
    }

    const badgeRegex = /\[BADGE_AWARDED:(\w+)\]/;
    const badgeMatch = text.match(badgeRegex);
    if (badgeMatch) {
      const badgeId = badgeMatch[1];
      text = text.replace(badgeRegex, '').trim();
      const badge = BADGES[badgeId];
      if (badge && !unlockedBadges.includes(badgeId)) {
        setUnlockedBadges(prev => [...prev, badgeId]);
        setPoints(prev => prev + badge.points);
        awardedBadge = badge;
      }
    }

    const chartTitleRegex = /\[CHART_TITLE:(.*?)\]/;
    const chartTitleMatch = text.match(chartTitleRegex);
    if (chartTitleMatch) {
        text = text.replace(chartTitleRegex, '').trim();
        chartTitle = chartTitleMatch[1];
    }

    const pieChartRegex = /\[PIE_CHART_DATA:({.*})\]/;
    const pieChartMatch = text.match(pieChartRegex);
    if (pieChartMatch) {
        text = text.replace(pieChartRegex, '').trim();
        try {
            const data = JSON.parse(pieChartMatch[1]);
            const formattedData: ChartDataPoint[] = Object.entries(data)
                .filter(([, value]) => typeof value === 'number' && value > 0)
                .map(([key, value]) => {
                    const source = key.replace(/([A-Z])/g, ' $1').replace(/^./, (str) => str.toUpperCase());
                    return { source, value: value as number };
                });
            
            if (formattedData.length > 0) {
              chartData = formattedData;
            }
        } catch (e) {
            console.error("Failed to parse chart data from AI response:", e);
        }
    }
    
    return { cleanedText: text, awardedBadge, chartData, chartTitle, isCarbonReceipt };
  }, [unlockedBadges]);

  const handleSendMessage = useCallback(async (text: string) => {
    if (!text.trim() && !image) return;
    
    if (text === "What's the footprint of an item?" && !image) {
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        sender: 'ai',
        text: "Great! Please use the camera icon 📸 to snap a picture of the item you're curious about."
      }]);
      return;
    }

    setSuggestions([]);

    const userMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: 'user',
      imageUrl: image?.data,
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setIsLoading(true);
    setError(null);
    const imageToSend = image; // Capture image state for this send operation
    setImage(null); // Clear image from input immediately for a better UX

    try {
      const aiResponseText = await sendMessageToAI(text, imageToSend);
      
      const { cleanedText, awardedBadge, chartData, chartTitle, isCarbonReceipt } = processAiResponse(aiResponseText);
      
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: cleanedText,
        sender: 'ai',
        badge: awardedBadge,
        chartData: chartData,
        chartTitle: chartTitle,
        isCarbonReceipt: isCarbonReceipt,
      };
      setMessages((prevMessages) => [...prevMessages, aiMessage]);

    } catch (err) {
      const errorMessage = 'Oops! Something went wrong. Please try again. 🤖';
      setError(errorMessage);
      const errorAiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: errorMessage,
        sender: 'ai',
      };
      setMessages((prevMessages) => [...prevMessages, errorAiMessage]);
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, [processAiResponse, image]);

  return (
    <div className="relative flex flex-col h-screen bg-gray-100 dark:bg-gray-900 font-sans">
      <div className="absolute top-2 left-1/2 -translate-x-1/2 text-xs text-gray-400 dark:text-gray-500 z-20">
        Created by Team GreenVision (Arsh Kumar Gupta & Adarsh)
      </div>
      <div aria-live="assertive" className="fixed inset-0 flex items-start justify-end p-4 space-y-3 pointer-events-none z-50">
        <div className="w-full max-w-xs space-y-3">
          {notifications.map((notification) => (
            <Notification
              key={notification.id}
              notification={notification}
              onClose={() => removeNotification(notification.id)}
            />
          ))}
        </div>
      </div>
      <ChatInterface
        messages={messages}
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
        error={error}
        suggestions={suggestions}
        rank={currentRank}
        points={points}
        image={image}
        onSetImage={setImage}
      />
    </div>
  );
};

export default App;