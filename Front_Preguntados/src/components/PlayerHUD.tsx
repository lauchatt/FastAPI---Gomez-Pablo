import React from 'react';
import { Player, CategoryKey } from '../types/game';
import { Trophy, Crown, Star } from 'lucide-react';

interface PlayerHUDProps {
  players: Player[];
  currentPlayerIndex: number;
}

const CATEGORY_COLORS: Record<CategoryKey, string> = {
  'Geografía': 'bg-blue-500',
  'Historia': 'bg-orange-500',
  'Ciencia': 'bg-green-500',
  'Entretenimiento': 'bg-pink-500',
  'Arte': 'bg-fuchsia-500',
  'Deportes': 'bg-yellow-500',
};

export const PlayerHUD: React.FC<PlayerHUDProps> = ({ players, currentPlayerIndex }) => {
  return (
    <div className="w-full max-w-4xl mx-auto px-4 py-3 grid grid-cols-1 md:grid-cols-2 gap-4">
      {players.map((player, idx) => {
        const isCurrent = idx === currentPlayerIndex;
        return (
          <div
            key={player.id}
            className={`relative rounded-2xl p-4 transition-all duration-300 border-2 shadow-lg flex flex-col justify-between ${
              isCurrent
                ? 'bg-gradient-to-r from-indigo-900/90 to-purple-900/90 border-yellow-400 shadow-yellow-500/20 ring-4 ring-yellow-400/30 scale-[1.02]'
                : 'bg-indigo-950/60 border-indigo-800/60 opacity-80'
            }`}
          >
            {isCurrent && (
              <div className="absolute -top-3 left-6 bg-yellow-400 text-indigo-950 text-xs font-extrabold px-3 py-1 rounded-full uppercase tracking-wider shadow-md animate-bounce">
                ¡Tu Turno!
              </div>
            )}

            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-3">
                <div className={`w-12 h-12 rounded-2xl flex items-center justify-center text-2xl shadow-inner border-2 ${
                  isCurrent ? 'bg-yellow-400/20 border-yellow-400 animate-pulse' : 'bg-indigo-900 border-indigo-700'
                }`}>
                  {player.avatar || '👑'}
                </div>
                <div>
                  <h3 className="font-extrabold text-lg text-white tracking-wide">{player.name}</h3>
                  <div className="flex items-center gap-3 text-xs text-indigo-300 mt-0.5">
                    <span className="flex items-center gap-1">
                      <Trophy className="w-3.5 h-3.5 text-yellow-400" /> Puntos: <strong className="text-white">{player.score}</strong>
                    </span>
                    <span className="flex items-center gap-1">
                      <Star className="w-3.5 h-3.5 text-amber-400" /> preguntas: <strong className="text-yellow-300">{player.accumulatedCrowns}/3</strong>
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Insignias collection */}
            <div className="mt-2 pt-2 border-t border-indigo-800/40">
              <div className="flex items-center gap-1.5 flex-wrap">
                {(Object.keys(CATEGORY_COLORS) as CategoryKey[]).map((cat) => {
                  const hasCrown = player.crowns[cat];
                  return (
                    <div
                      key={cat}
                      title={`${cat}: ${hasCrown ? 'Obtenida' : 'Pendiente'}`}
                      className={`w-7 h-7 rounded-full flex items-center justify-center transition-all ${
                        hasCrown
                          ? `${CATEGORY_COLORS[cat]} text-white shadow-md scale-105 ring-2 ring-white/60`
                          : 'bg-indigo-900/40 border border-indigo-700/50 text-indigo-600 grayscale opacity-40'
                      }`}
                    >
                      <Crown className={`w-4 h-4 ${hasCrown ? 'text-white drop-shadow' : 'text-indigo-400'}`} />
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
