import React from 'react';
import { Player, RouletteSector } from '../types/game';
import { PlayerHUD } from '../components/PlayerHUD';
import { Roulette } from '../components/Roulette';
import { ErrorBanner } from '../components/ErrorBanner';

interface GameScreenProps {
  players: Player[];
  currentPlayerIndex: number;
  onSpinComplete: (sector: RouletteSector) => void;
}

export const GameScreen: React.FC<GameScreenProps> = ({
  players,
  currentPlayerIndex,
  onSpinComplete,
}) => {
  const currentPlayer = players[currentPlayerIndex];

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-indigo-950 via-purple-950 to-slate-950 text-white">
      <ErrorBanner />

      {/* Header HUD */}
      <PlayerHUD players={players} currentPlayerIndex={currentPlayerIndex} />

      {/* Main Roulette Area */}
      <div className="flex-1 flex flex-col items-center justify-center p-4">
        <div className="text-center mb-4">
          <h2 className="text-2xl font-black text-yellow-400 tracking-wide">
            ¡Turno de {currentPlayer.name}!
          </h2>
          <p className="text-indigo-200 text-sm mt-1">Gira la ruleta para elegir una categoría o corona</p>
        </div>

        <Roulette onSpinComplete={onSpinComplete} />
      </div>
    </div>
  );
};
