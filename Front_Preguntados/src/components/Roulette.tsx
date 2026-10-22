import React, { useState } from 'react';
import { CategoryKey } from '../types/game';
import { CATEGORIES } from '../services/mockQuestions';
import { Compass, Sparkles } from 'lucide-react';

interface RouletteProps {
  onSpinComplete: (category: CategoryKey) => void;
  disabled?: boolean;
}

const CATEGORY_COLORS: Record<CategoryKey, { fill: string; text: string }> = {
  'Geografía': { fill: '#3b82f6', text: '#ffffff' },
  'Historia': { fill: '#f97316', text: '#ffffff' },
  'Ciencia': { fill: '#22c55e', text: '#ffffff' },
  'Entretenimiento': { fill: '#ec4899', text: '#ffffff' },
  'Arte': { fill: '#d946ef', text: '#ffffff' },
  'Deportes': { fill: '#eab308', text: '#ffffff' },
};

export const Roulette: React.FC<RouletteProps> = ({ onSpinComplete, disabled }) => {
  const [spinning, setSpinning] = useState<boolean>(false);
  const [rotation, setRotation] = useState<number>(0);
  const [selectedCategory, setSelectedCategory] = useState<CategoryKey | null>(null);

  const spinRoulette = () => {
    if (spinning || disabled) return;

    setSpinning(true);
    setSelectedCategory(null);

    // Random extra spins (between 5 and 8 full rotations) plus a random target category index
    const randomCategoryIndex = Math.floor(Math.random() * CATEGORIES.length);
    const targetCategory = CATEGORIES[randomCategoryIndex];
    
    // Each slice is 360 / 6 = 60 degrees
    const sliceAngle = 360 / CATEGORIES.length;
    // Calculate degree to center the selected category at the top pointer (0 deg)
    // Index 0 is centered around 30 deg, etc.
    const extraSpins = 360 * 6;
    const targetDegree = extraSpins + (360 - (randomCategoryIndex * sliceAngle + sliceAngle / 2));

    setRotation((prev) => prev + targetDegree);

    setTimeout(() => {
      setSpinning(false);
      setSelectedCategory(targetCategory);
      onSpinComplete(targetCategory);
    }, 4000); // matches CSS transition duration (4s)
  };

  return (
    <div className="flex flex-col items-center justify-center my-6">
      {/* Pointer at the top */}
      <div className="relative z-20 -mb-4 w-0 h-0 border-l-[16px] border-l-transparent border-r-[16px] border-r-transparent border-t-[28px] border-t-yellow-400 drop-shadow-[0_4px_4px_rgba(0,0,0,0.4)] animate-bounce" />

      {/* Roulette Wheel Container */}
      <div className="relative w-72 h-72 sm:w-80 sm:h-80 rounded-full p-2 bg-gradient-to-tr from-yellow-500 via-amber-400 to-yellow-300 shadow-[0_10px_30px_rgba(0,0,0,0.5)] border-4 border-yellow-200">
        <div
          className="w-full h-full rounded-full relative overflow-hidden shadow-inner transition-transform ease-out"
          style={{
            transform: `rotate(${rotation}deg)`,
            transitionDuration: spinning ? '4s' : '0s',
          }}
        >
          <svg className="w-full h-full" viewBox="0 0 200 200">
            {CATEGORIES.map((cat, index) => {
              const angle = (360 / CATEGORIES.length) * index;
              const nextAngle = (360 / CATEGORIES.length) * (index + 1);
              
              // SVG path for a pie slice
              const x1 = 100 + 100 * Math.cos((Math.PI * (angle - 90)) / 180);
              const y1 = 100 + 100 * Math.sin((Math.PI * (angle - 90)) / 180);
              const x2 = 100 + 100 * Math.cos((Math.PI * (nextAngle - 90)) / 180);
              const y2 = 100 + 100 * Math.sin((Math.PI * (nextAngle - 90)) / 180);
              
              const pathData = `M 100 100 L ${x1} ${y1} A 100 100 0 0 1 ${x2} ${y2} Z`;

              // Text coordinates (midpoint of angle)
              const midAngle = angle + 30;
              const textRadius = 62;
              const textX = 100 + textRadius * Math.cos((Math.PI * (midAngle - 90)) / 180);
              const textY = 100 + textRadius * Math.sin((Math.PI * (midAngle - 90)) / 180);

              return (
                <g key={cat}>
                  <path d={pathData} fill={CATEGORY_COLORS[cat].fill} stroke="#ffffff" strokeWidth="2" />
                  <text
                    x={textX}
                    y={textY}
                    fill={CATEGORY_COLORS[cat].text}
                    fontSize="11"
                    fontWeight="bold"
                    textAnchor="middle"
                    dominantBaseline="central"
                    transform={`rotate(${midAngle}, ${textX}, ${textY})`}
                    className="drop-shadow-[0_1px_2px_rgba(0,0,0,0.8)] select-none pointer-events-none"
                  >
                    {cat.toUpperCase()}
                  </text>
                </g>
              );
            })}
          </svg>
        </div>

        {/* Center spin button */}
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

      {selectedCategory && !spinning && (
        <div className="mt-4 animate-fade-in flex items-center gap-2 bg-indigo-900/90 border border-yellow-400 px-4 py-2 rounded-full shadow-lg text-yellow-300 font-bold text-sm">
          <Sparkles className="w-4 h-4 text-yellow-400 animate-pulse" />
          <span>Categoría seleccionada: <strong className="text-white">{selectedCategory}</strong></span>
        </div>
      )}
    </div>
  );
};
