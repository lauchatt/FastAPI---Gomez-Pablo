import React, { useState } from 'react';
import { RouletteSector } from '../types/game';
import { ROULETTE_SECTORS } from '../services/mockQuestions';
import { soundService } from '../services/soundService';
import { Compass, Sparkles, Crown } from 'lucide-react';

interface RouletteProps {
  onSpinComplete: (sector: RouletteSector) => void;
  disabled?: boolean;
}

const SECTOR_COLORS: Record<RouletteSector, { fill: string; text: string }> = {
  'Geografía': { fill: '#3b82f6', text: '#ffffff' },
  'Historia': { fill: '#f97316', text: '#ffffff' },
  'Ciencia': { fill: '#22c55e', text: '#ffffff' },
  'Corona': { fill: '#a855f7', text: '#ffffff' },
  'Entretenimiento': { fill: '#ec4899', text: '#ffffff' },
  'Arte': { fill: '#d946ef', text: '#ffffff' },
  'Deportes': { fill: '#eab308', text: '#ffffff' },
};

export const Roulette: React.FC<RouletteProps> = ({ onSpinComplete, disabled }) => {
  const [spinning, setSpinning] = useState<boolean>(false);
  const [rotation, setRotation] = useState<number>(0);
  const [selectedSector, setSelectedSector] = useState<RouletteSector | null>(null);

  const spinRoulette = () => {
    if (spinning || disabled) return;

    soundService.startRouletteSpinSound();
    setSpinning(true);
    setSelectedSector(null);

    const randomSectorIndex = Math.floor(Math.random() * ROULETTE_SECTORS.length);
    const targetSector = ROULETTE_SECTORS[randomSectorIndex];
    
    const totalSectors = ROULETTE_SECTORS.length;
    const sliceAngle = 360 / totalSectors;
    const extraSpins = 360 * 6;
    const targetDegree = extraSpins + (360 - (randomSectorIndex * sliceAngle + sliceAngle / 2));

    setRotation((prev) => prev + targetDegree);

    setTimeout(() => {
      setSpinning(false);
      setSelectedSector(targetSector);
      onSpinComplete(targetSector);
    }, 4000);
  };

  return (
    <div className="flex flex-col items-center justify-center my-6">
      <div className="relative z-20 -mb-4 w-0 h-0 border-l-[16px] border-l-transparent border-r-[16px] border-r-transparent border-t-[28px] border-t-yellow-400 drop-shadow-[0_4px_4px_rgba(0,0,0,0.4)] animate-bounce" />

      <div className="relative w-72 h-72 sm:w-80 sm:h-80 rounded-full p-2 bg-gradient-to-tr from-yellow-500 via-amber-400 to-yellow-300 shadow-[0_10px_30px_rgba(0,0,0,0.5)] border-4 border-yellow-200">
        <div
          className="w-full h-full rounded-full relative overflow-hidden shadow-inner transition-transform ease-out"
          style={{
            transform: `rotate(${rotation}deg)`,
            transitionDuration: spinning ? '4s' : '0s',
          }}
        >
          <svg className="w-full h-full" viewBox="0 0 200 200">
            {ROULETTE_SECTORS.map((sector, index) => {
              const totalSectors = ROULETTE_SECTORS.length;
              const angle = (360 / totalSectors) * index;
              const nextAngle = (360 / totalSectors) * (index + 1);
              
              const x1 = 100 + 100 * Math.cos((Math.PI * (angle - 90)) / 180);
              const y1 = 100 + 100 * Math.sin((Math.PI * (angle - 90)) / 180);
              const x2 = 100 + 100 * Math.cos((Math.PI * (nextAngle - 90)) / 180);
              const y2 = 100 + 100 * Math.sin((Math.PI * (nextAngle - 90)) / 180);
              
              const pathData = `M 100 100 L ${x1} ${y1} A 100 100 0 0 1 ${x2} ${y2} Z`;

              const midAngle = angle + (360 / totalSectors) / 2;
              const textRadius = 62;
              const textX = 100 + textRadius * Math.cos((Math.PI * (midAngle - 90)) / 180);
              const textY = 100 + textRadius * Math.sin((Math.PI * (midAngle - 90)) / 180);

              return (
                <g key={sector}>
                  <path d={pathData} fill={SECTOR_COLORS[sector].fill} stroke="#ffffff" strokeWidth="2" />
                  {sector === 'Corona' && (
                    <g transform={`translate(${textX}, ${textY}) rotate(${midAngle})`}>
                      <circle r="18" fill="rgba(251, 191, 36, 0.4)" className="animate-pulse" />
                      <circle r="14" fill="#d97706" stroke="#fde047" strokeWidth="2.5" className="drop-shadow-[0_2px_6px_rgba(0,0,0,0.8)]" />
                      <text
                        x="0"
                        y="1"
                        fill="#ffffff"
                        fontSize="16"
                        fontWeight="black"
                        textAnchor="middle"
                        dominantBaseline="central"
                        className="drop-shadow-[0_2px_4px_rgba(0,0,0,0.9)] select-none pointer-events-none"
                      >
                        👑
                      </text>
                    </g>
                  )}
                </g>
              );
            })}
          </svg>
        </div>

        <button
          onClick={spinRoulette}
          disabled={spinning || disabled}
          className="absolute inset-0 m-auto w-20 h-20 rounded-full bg-gradient-to-b from-yellow-300 via-yellow-500 to-amber-600 border-4 border-white text-white font-extrabold text-sm shadow-[0_6px_15px_rgba(0,0,0,0.4)] flex flex-col items-center justify-center transform active:scale-95 transition-transform hover:scale-105 disabled:opacity-80 cursor-pointer z-10"
        >
          <Compass className={`w-6 h-6 text-white drop-shadow mb-0.5 ${spinning ? 'animate-spin' : ''}`} />
          <span className="drop-shadow text-[11px] tracking-wider uppercase">
            {spinning ? 'GIRANDO' : 'GIRAR'}
          </span>
        </button>
      </div>

      {selectedSector && !spinning && (
        <div className="mt-4 animate-fade-in flex items-center gap-2 bg-indigo-900/90 border border-yellow-400 px-4 py-2 rounded-full shadow-lg text-yellow-300 font-bold text-sm">
          {selectedSector === 'Corona' ? <Crown className="w-4 h-4 text-yellow-400 animate-bounce" /> : <Sparkles className="w-4 h-4 text-yellow-400 animate-pulse" />}
          <span>Resultado ruleta: <strong className="text-white">{selectedSector}</strong></span>
        </div>
      )}
    </div>
  );
};
