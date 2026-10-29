import React, { useState } from 'react';
import { Play, Sparkles } from 'lucide-react';

interface SetupScreenProps {
  onStartGame: (p1Name: string, p1Avatar: string, p2Name: string, p2Avatar: string) => void;
}

const AVATARS = ['🦁', '🚀', '🐼', '🤖', '🦄', '🦊', '🐱', '⭐'];

export const SetupScreen: React.FC<SetupScreenProps> = ({ onStartGame }) => {
  const [p1Name, setP1Name] = useState<string>('Jugador 1');
  const [p1Avatar, setP1Avatar] = useState<string>('🦁');
  const [p2Name, setP2Name] = useState<string>('Jugador 2');
  const [p2Avatar, setP2Avatar] = useState<string>('🚀');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!p1Name.trim() || !p2Name.trim()) return;
    onStartGame(p1Name.trim(), p1Avatar, p2Name.trim(), p2Avatar);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-indigo-950 via-purple-950 to-slate-950">
      <div className="w-full max-w-lg bg-indigo-900/80 backdrop-blur-md rounded-3xl p-6 sm:p-8 border-2 border-yellow-400/50 shadow-[0_20px_50px_rgba(0,0,0,0.7)] text-white relative overflow-hidden">
        <div className="absolute -top-10 -right-10 w-32 h-32 bg-yellow-400/10 rounded-full blur-2xl pointer-events-none" />

        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-tr from-yellow-400 to-amber-500 shadow-lg text-indigo-950 mb-3">
            <Sparkles className="w-7 h-7 animate-pulse" />
          </div>
          <h1 className="text-3xl font-black tracking-tight bg-gradient-to-r from-yellow-300 via-yellow-400 to-amber-300 bg-clip-text text-transparent">
            PREGUNTADOS
          </h1>
          <p className="text-indigo-200 text-sm mt-1">Duelo Local - Personaliza tus jugadores</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Player 1 Setup */}
          <div className="bg-indigo-950/60 p-4 rounded-2xl border border-indigo-800/80">
            <label className="block text-xs font-bold uppercase tracking-wider text-yellow-300 mb-2">
              Jugador 1
            </label>
            <div className="flex gap-3 items-center">
              <input
                type="text"
                value={p1Name}
                onChange={(e) => setP1Name(e.target.value)}
                maxLength={15}
                required
                placeholder="Nombre P1"
                className="flex-1 px-4 py-2.5 rounded-xl bg-indigo-900/80 border-2 border-indigo-700 focus:border-yellow-400 focus:outline-none text-white font-bold shadow-inner"
              />
            </div>
            <div className="mt-3">
              <span className="text-[11px] font-semibold text-indigo-300 uppercase block mb-1.5">Elige tu avatar:</span>
              <div className="flex gap-2 flex-wrap">
                {AVATARS.map((av) => (
                  <button
                    type="button"
                    key={`p1-${av}`}
                    onClick={() => setP1Avatar(av)}
                    className={`w-10 h-10 rounded-xl text-xl flex items-center justify-center transition-all cursor-pointer ${
                      p1Avatar === av
                        ? 'bg-yellow-400 text-indigo-950 scale-110 shadow-lg ring-2 ring-white'
                        : 'bg-indigo-900/60 hover:bg-indigo-800 text-white'
                    }`}
                  >
                    {av}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Player 2 Setup */}
          <div className="bg-indigo-950/60 p-4 rounded-2xl border border-indigo-800/80">
            <label className="block text-xs font-bold uppercase tracking-wider text-yellow-300 mb-2">
              Jugador 2
            </label>
            <div className="flex gap-3 items-center">
              <input
                type="text"
                value={p2Name}
                onChange={(e) => setP2Name(e.target.value)}
                maxLength={15}
                required
                placeholder="Nombre P2"
                className="flex-1 px-4 py-2.5 rounded-xl bg-indigo-900/80 border-2 border-indigo-700 focus:border-yellow-400 focus:outline-none text-white font-bold shadow-inner"
              />
            </div>
            <div className="mt-3">
              <span className="text-[11px] font-semibold text-indigo-300 uppercase block mb-1.5">Elige tu avatar:</span>
              <div className="flex gap-2 flex-wrap">
                {AVATARS.map((av) => (
                  <button
                    type="button"
                    key={`p2-${av}`}
                    onClick={() => setP2Avatar(av)}
                    className={`w-10 h-10 rounded-xl text-xl flex items-center justify-center transition-all cursor-pointer ${
                      p2Avatar === av
                        ? 'bg-yellow-400 text-indigo-950 scale-110 shadow-lg ring-2 ring-white'
                        : 'bg-indigo-900/60 hover:bg-indigo-800 text-white'
                    }`}
                  >
                    {av}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <button
            type="submit"
            className="w-full py-4 rounded-2xl bg-gradient-to-r from-yellow-400 via-amber-400 to-yellow-500 text-indigo-950 font-black text-lg uppercase tracking-wider shadow-[0_10px_25px_rgba(250,204,21,0.4)] hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center gap-2 cursor-pointer"
          >
            <Play className="w-6 h-6 fill-indigo-950" />
            Iniciar Partida
          </button>
        </form>
      </div>
    </div>
  );
};
