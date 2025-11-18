import { Badge, Rank } from '../types';
import { BadgeIcon } from '../components/icons';

// Define all available badges
export const BADGES: { [key: string]: Badge } = {
  TRANSPORT_TRACKER: {
    id: 'TRANSPORT_TRACKER',
    name: 'Transport Tracker',
    description: 'You calculated your transportation footprint. A journey of a thousand miles begins with a single step!',
    icon: BadgeIcon,
    points: 50,
  },
  HOME_HERO: {
    id: 'HOME_HERO',
    name: 'Home Hero',
    description: "You've calculated your home energy footprint! Knowledge is power - literally.",
    icon: BadgeIcon,
    points: 50,
  },
  ECO_EATER: {
    id: 'ECO_EATER',
    name: 'Eco Eater',
    description: "You've analyzed your diet's footprint. You are what you eat, and you're eating greener!",
    icon: BadgeIcon,
    points: 50,
  },
};

// Define all available ranks
export const RANKS: Rank[] = [
  { name: 'Eco Novice', minPoints: 0, icon: '🌱' },
  { name: 'Green Learner', minPoints: 100, icon: '🌳' },
  { name: 'Planet Protector', minPoints: 300, icon: '🌍' },
];
