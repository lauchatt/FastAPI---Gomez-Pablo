import React from 'react';
import { Player } from '../types/game';
import { Smartphone, ArrowRight } from 'lucide-react';

interface TransitionScreenProps {
  nextPlayer: Player;
  onContinue: () => void;
}

export const TransitionScreen: React.FC<TransitionScreenProps> = ({ nextPlayer, onContinue }) => {
  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-indigo-950 via-purple-950 to-slate-950 text-white">
      <div className="w-full max-w-md bg-indigo-900/90 backdrop-blur-md rounded-3xl p-8 border-2 border-yellow-400/50 shadow-[0_20px_50px_rgba(0,0,0,0.7)] text-center relative overflow-hidden">
        <div className="w-20 h-20 mx-auto mb-6 rounded-3xl bg-gradient-to-tr from-yellow-400 to-amber-500 shadow-lg flex items-center justify-center text-indigo-950 animate-bounce">
          <Smartphone className="w-10 h-10" />
        </div>

        <h2 className="text-xl text-indigo-200 font-semibold mb-2">Pásale el dispositivo a</h2>
        <h1 className="text-3xl font-black text-yellow-400 tracking-wide mb-8">
          {nextPlayer.name}
        </h1>

        <button
          onClick={onContinue}
          className="w-full py-4 rounded-2xl bg-gradient-to-r from-yellow-400 via-amber-400 to-yellow-500 text-indigo-950 font-black text-lg uppercase tracking-wider shadow-[0_10px_25px_rgba(250,204,21,0.4)] hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center gap-2 cursor-pointer"
        >
          <span>¡Estoy Listo!</span>
          <ArrowRight className="w-6 h-6" />
        </button>
      </div>
    </div>
  );
};
