export type CategoryKey = 'Geografía' | 'Historia' | 'Ciencia' | 'Entretenimiento' | 'Arte' | 'Deportes';

export interface ApiQuestion {
  id: number;
  question: string;
  answer: string;
  category: CategoryKey;
  source: string;
  options: string[]; // 4 options for the UI
}

export interface Player {
  id: number;
  name: string;
  score: number;
  crowns: Record<CategoryKey, boolean>;
}

export type GameScreenType = 'SETUP' | 'ROULETTE' | 'QUESTION' | 'TRANSITION' | 'GAME_OVER';

export interface CategoryConfig {
  name: CategoryKey;
  color: string;
  bgClass: string;
  borderClass: string;
  textClass: string;
  icon: string;
}
