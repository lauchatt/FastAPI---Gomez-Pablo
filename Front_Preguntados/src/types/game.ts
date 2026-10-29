export type CategoryKey = 'Geografía' | 'Historia' | 'Ciencia' | 'Entretenimiento' | 'Arte' | 'Deportes';
export type RouletteSector = CategoryKey | 'Corona';

export interface ApiQuestion {
  id: number;
  question: string;
  answer: string;
  category: CategoryKey;
  source: string;
  options: string[];
}

export interface Player {
  id: number;
  name: string;
  avatar: string;
  score: number;
  accumulatedCrowns: number;
  crowns: Record<CategoryKey, boolean>;
}

export type GameScreenType = 'SETUP' | 'ROULETTE' | 'QUESTION' | 'CATEGORY_CHOICE' | 'TRANSITION' | 'GAME_OVER';

export interface CategoryConfig {
  name: CategoryKey;
  color: string;
  bgClass: string;
  borderClass: string;
  textClass: string;
  icon: string;
}
