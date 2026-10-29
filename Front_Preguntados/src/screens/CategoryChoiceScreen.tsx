import React from 'react';
import { CategoryKey, Player } from '../types/game';
import { CATEGORIES } from '../services/mockQuestions';
import { soundService } from '../services/soundService';
import { Crown, Sparkles } from 'lucide-react';

interface CategoryChoiceScreenProps {
  player: Player;
  onSelectCategory: (category: CategoryKey) => void;
}

const CATEGORY_STYLES: Record<CategoryKey, { bg: string; text: string; border: string }> = {
  'Geografía': { bg: 'bg-blue-600 hover:bg-blue-500', text: 'text-white', border: 'border-blue-400' },
  'Historia': { bg: 'bg-orange-600 hover:bg-orange-500', text: 'text-white', border: 'border-orange-400' },
  'Ciencia': { bg: 'bg-green-600 hover:bg-green-500', text: 'text-white', border: 'border-green-400' },
  'Entretenimiento': { bg: 'bg-pink-600 hover:bg-pink-500', text: 'text-white', border: 'border-pink-400' },
  'Arte': { bg: 'bg-fuchsia-600 hover:bg-fuchsia-500', text: 'text-white', border: 'border-fuchsia-400' },
  'Deportes': { bg: 'bg-yellow-500 hover:bg-yellow-400', text: 'text-indigo-950', border: 'border-yellow-300' },
};

export const CategoryChoiceScreen: React.FC<CategoryChoiceScreenProps> = ({ player, onSelectCategory }) => {
  const allObtained = CATEGORIES.every((cat) => player.crowns[cat]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-gradient-to-br from-indigo-950 via-purple-950 to-slate-950 text-white">
      <div className="w-full max-w-2xl bg-indigo-900/90 border-2 border-yellow-400 rounded-3xl p-6 md:p-8 shadow-2xl text-center">
        <div className="flex justify-center mb-4">
          <div className="w-16 h-16 rounded-full bg-yellow-400 text-indigo-950 flex items-center justify-center shadow-lg animate-bounce">
            <Crown className="w-8 h-8" />
          </div>
        </div>

        <h2 className="text-2xl sm:text-3xl font-black text-yellow-400 mb-2">
          {allObtained ? '¡Todas las insignias obtenidas!' : '¡Oportunidad de Corona!'}
        </h2>
        <p className="text-indigo-200 text-sm sm:text-base mb-6">
          {allObtained
            ? `¡${player.name}, ya has conseguido las 6 insignias! Puedes continuar con la partida.`
            : `¡${player.name}, elegí una categoría pendiente para ganar tu insignia!`}
        </p>

        {allObtained ? (
          <button
            onClick={() => {
              soundService.playSelectCategory();
              onSelectCategory(CATEGORIES[0]);
            }}
            className="px-8 py-4 rounded-2xl bg-gradient-to-r from-yellow-400 via-amber-400 to-yellow-500 text-indigo-950 font-black text-lg uppercase tracking-wider shadow-lg hover:scale-105 active:scale-95 transition-all cursor-pointer"
          >
            Continuar Partida
          </button>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {CATEGORIES.map((cat) => {
              const hasCrown = player.crowns[cat];
              const style = CATEGORY_STYLES[cat];

              if (hasCrown) {
                return (
                  <div
                    key={cat}
                    className="p-4 rounded-2xl font-bold flex items-center justify-between border-2 border-indigo-800 bg-indigo-950/50 opacity-50 cursor-not-allowed text-indigo-400"
                  >
                    <span className="flex items-center gap-3 text-lg">
                      <Sparkles className="w-5 h-5 text-indigo-600" />
                      {cat}
                    </span>
                    <span className="text-xs bg-indigo-900/80 text-yellow-400 px-2.5 py-1 rounded-full flex items-center gap-1 font-semibold border border-indigo-700">
                      <Crown className="w-3.5 h-3.5 text-yellow-400" /> Ya obtenida
                    </span>
                  </div>
                );
              }

              return (
                <button
                  key={cat}
                  onClick={() => {
                    soundService.playSelectCategory();
                    onSelectCategory(cat);
                  }}
                  className={`p-4 rounded-2xl font-bold flex items-center justify-between border-2 shadow-lg transition-all transform hover:scale-105 cursor-pointer ${style.bg} ${style.text} ${style.border}`}
                >
                  <span className="flex items-center gap-3 text-lg">
                    <Sparkles className="w-5 h-5" />
                    {cat}
                  </span>
                  <span className="text-xs bg-white/20 px-2 py-1 rounded-full font-semibold">
                    Desafiar
                  </span>
                </button>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
