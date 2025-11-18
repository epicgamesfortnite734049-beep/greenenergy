import React from 'react';

export interface Badge {
  id: string;
  name: string;
  description: string;
  icon: React.FC<React.SVGProps<SVGSVGElement>>;
  points: number;
}

export interface Rank {
  name: string;
  minPoints: number;
  icon: string;
}

export interface ChartDataPoint {
    source: string;
    value: number;
}

export interface Message {
  id:string;
  text: string;
  sender: 'user' | 'ai';
  imageUrl?: string;
  badge?: Badge;
  chartData?: ChartDataPoint[];
  chartTitle?: string;
  isCarbonReceipt?: boolean;
}

export interface Notification {
  id: string;
  message: string;
  icon: React.ReactNode;
}