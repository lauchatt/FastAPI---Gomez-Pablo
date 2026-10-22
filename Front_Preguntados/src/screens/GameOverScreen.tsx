import React from 'react';
import { Player } from '../types/game';
import { Trophy, RotateCcw, Award } from 'lucide-react';

interface GameOverScreenProps {
  players: Player[];
  onRestart: () => void;
}

export const GameOverScreen: React.FC<GameOverScreenProps> = ({ players, onRestart }) => {
  // Determine winner (highest score or most crowns)
  const sortedPlayers = [...players].sort((a, b) => {
    const crownsA = Object.values(a.crowns).filter(Boolean).length;
    const crownsB = Object.values(b.crowns).filter(Boolean).length;
    if (crownsA !== crownsB) return crownsB - crownsA;
    return b.score - a.score;
  });

  const winner = sortedPlayers[0];

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-indigo-950 via-purple-950 to-slate-950 text-white">
      <div className="w-full max-w-lg bg-indigo-900/90 backdrop-blur-md rounded-3xl p-8 border-2 border-yellow-400 shadow-[0_20px_50px_rgba(0,0,0,0.8)] text-center relative overflow-hidden">
        <div className="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-tr from-yellow-300 via-yellow-400 to-amber-500 shadow-xl flex items-center justify-center text-indigo-950 animate-bounce">
          <Trophy className="w-12 h-12" />
        </div>

        <h2 className="text-xl font-bold text-yellow-300 tracking-wide uppercase mb-1">¡Fin del Duelo!</h2>
        <h1 className="text-4xl font-black text-white tracking-tight mb-6">
          ¡Ganador: {winner.name}!
        </h1>

        <div className="bg-indigo-950/70 rounded-2xl p-4 mb-8 border border-indigo-800/60 space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-indigo-300 flex items-center justify-center gap-1">
            <Award className="w-4 h-4 text-yellow-400" /> Marcador Final
          </h3>
          <div className="space-y-2">
            {sortedPlayers.map((p, idx) => {
              const crownsCount = Object.values(p.crowns).filter(Boolean).length;
              return (
                <div key={p.id} className="flex items-center justify-between bg-indigo-900/50 px-4 py-3 rounded-xl border border-indigo-800/40">
                  <span className="font-extrabold flex items-center gap-2">
                    <span className="text-yellow-400">#{idx + 1}</span> {p.name}
                  </span>
                  <div className="flex items-center gap-4 text-sm font-bold">
                    <span>{p.score} pts</span>
                    <span className="text-yellow-400">{crownsCount} 👑</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <button
          onClick={onRestart}
          className="w-full py-4 rounded-2xl bg-gradient-to-r from-yellow-400 via-amber-400 to-yellow-500 text-indigo-950 font-black text-lg uppercase tracking-wider shadow-[0_10px_25px_rgba(250,204,21,0.4)] hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center gap-2 cursor-pointer"
        >
          <RotateCcw className="w-6 h-6" />
          Jugar de Nuevo
        </button>
      </div>
    </div>
  );
};
