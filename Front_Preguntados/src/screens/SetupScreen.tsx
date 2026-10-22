import React, { useState } from 'react';
import { Users, Play, Sparkles } from 'lucide-react';

interface SetupScreenProps {
  onStartGame: (p1Name: string, p2Name: string) => void;
}

export const SetupScreen: React.FC<SetupScreenProps> = ({ onStartGame }) => {
  const [p1Name, setP1Name] = useState<string>('Jugador 1');
  const [p2Name, setP2Name] = useState<string>('Jugador 2');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!p1Name.trim() || !p2Name.trim()) return;
    onStartGame(p1Name.trim(), p2Name.trim());
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-indigo-950 via-purple-950 to-slate-950">
      <div className="w-full max-w-md bg-indigo-900/80 backdrop-blur-md rounded-3xl p-8 border-2 border-yellow-400/50 shadow-[0_20px_50px_rgba(0,0,0,0.7)] text-white relative overflow-hidden">
        {/* Decorative header icon */}
        <div className="absolute -top-10 -right-10 w-32 h-32 bg-yellow-400/10 rounded-full blur-2xl pointer-events-none" />

        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-tr from-yellow-400 to-amber-500 shadow-lg text-indigo-950 mb-4">
            <Sparkles className="w-8 h-8 animate-pulse" />
          </div>
          <h1 className="text-3xl font-black tracking-tight bg-gradient-to-r from-yellow-300 via-yellow-400 to-amber-300 bg-clip-text text-transparent">
            PREGUNTADOS
          </h1>
          <p className="text-indigo-200 text-sm mt-1">Duelo Local - 2 Jugadores</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-yellow-300 mb-2">
              Nombre Jugador 1
            </label>
            <input
              type="text"
              value={p1Name}
              onChange={(e) => setP1Name(e.target.value)}
              maxLength={15}
              required
              className="w-full px-4 py-3 rounded-xl bg-indigo-950/80 border-2 border-indigo-700 focus:border-yellow-400 focus:outline-none text-white font-bold shadow-inner transition-colors"
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-yellow-300 mb-2">
              Nombre Jugador 2
            </label>
            <input
              type="text"
              value={p2Name}
              onChange={(e) => setP2Name(e.target.value)}
              maxLength={15}
              required
              className="w-full px-4 py-3 rounded-xl bg-indigo-950/80 border-2 border-indigo-700 focus:border-yellow-400 focus:outline-none text-white font-bold shadow-inner transition-colors"
            />
          </div>

          <button
            type="submit"
            className="w-full mt-4 py-4 rounded-2xl bg-gradient-to-r from-yellow-400 via-amber-400 to-yellow-500 text-indigo-950 font-black text-lg uppercase tracking-wider shadow-[0_10px_25px_rgba(250,204,21,0.4)] hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center gap-2 cursor-pointer"
          >
            <Play className="w-6 h-6 fill-indigo-950" />
            Iniciar Partida
          </button>
        </form>
      </div>
    </div>
  );
};
