import React, { useState, useEffect } from 'react';
import { ApiQuestion, CategoryKey } from '../types/game';
import { Clock, HelpCircle, CheckCircle2, XCircle } from 'lucide-react';

interface QuestionCardProps {
  questionData: ApiQuestion;
  onAnswerResult: (isCorrect: boolean) => void;
}

const CATEGORY_STYLES: Record<CategoryKey, { bg: string; badge: string; border: string }> = {
  'Geografía': { bg: 'from-blue-900/90 to-indigo-950', badge: 'bg-blue-500', border: 'border-blue-500/50' },
  'Historia': { bg: 'from-orange-900/90 to-indigo-950', badge: 'bg-orange-500', border: 'border-orange-500/50' },
  'Ciencia': { bg: 'from-green-900/90 to-indigo-950', badge: 'bg-green-500', border: 'border-green-500/50' },
  'Entretenimiento': { bg: 'from-pink-900/90 to-indigo-950', badge: 'bg-pink-500', border: 'border-pink-500/50' },
  'Arte': { bg: 'from-fuchsia-900/90 to-indigo-950', badge: 'bg-fuchsia-500', border: 'border-fuchsia-500/50' },
  'Deportes': { bg: 'from-yellow-900/90 to-indigo-950', badge: 'bg-yellow-500', border: 'border-yellow-500/50' },
};

export const QuestionCard: React.FC<QuestionCardProps> = ({ questionData, onAnswerResult }) => {
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const [timeLeft, setTimeLeft] = useState<number>(30);
  const [answered, setAnswered] = useState<boolean>(false);

  const style = CATEGORY_STYLES[questionData.category] || CATEGORY_STYLES['Geografía'];

  // Timer countdown
  useEffect(() => {
    if (answered) return;

    if (timeLeft <= 0) {
      handleTimeout();
      return;
    }

    const timer = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft, answered]);

  const handleTimeout = () => {
    if (answered) return;
    setAnswered(true);
    setIsCorrect(false);
    setTimeout(() => {
      onAnswerResult(false);
    }, 2000);
  };

  const handleOptionClick = (option: string) => {
    if (answered) return;
    setAnswered(true);
    setSelectedOption(option);

    const correct = option === questionData.answer;
    setIsCorrect(correct);

    setTimeout(() => {
      onAnswerResult(correct);
    }, 2000);
  };

  return (
    <div className={`w-full max-w-2xl mx-auto rounded-3xl p-6 md:p-8 bg-gradient-to-b ${style.bg} border-2 ${style.border} shadow-[0_15px_40px_rgba(0,0,0,0.6)] text-white relative overflow-hidden`}>
      {/* Top bar with category & timer */}
      <div className="flex items-center justify-between mb-6">
        <span className={`${style.badge} text-white font-extrabold text-xs sm:text-sm px-4 py-1.5 rounded-full uppercase tracking-wider shadow-md`}>
          {questionData.category}
        </span>

        <div className={`flex items-center gap-2 px-4 py-1.5 rounded-full font-bold text-sm ${
          timeLeft <= 10 ? 'bg-red-600/90 animate-pulse text-white' : 'bg-indigo-900/80 text-yellow-300 border border-indigo-700'
        }`}>
          <Clock className="w-4 h-4" />
          <span>{timeLeft}s</span>
        </div>
      </div>

      {/* Question */}
      <div className="mb-8 text-center">
        <h2 className="text-xl sm:text-2xl md:text-3xl font-black leading-snug drop-shadow">
          {questionData.question}
        </h2>
        {questionData.source && (
          <p className="text-xs text-indigo-300 mt-2 italic">Fuente: {questionData.source}</p>
        )}
      </div>

      {/* Options grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
        {questionData.options.map((option, idx) => {
          let btnStyle = 'bg-indigo-900/80 hover:bg-indigo-800 text-white border-indigo-700/60 hover:border-yellow-400';

          if (answered) {
            if (option === questionData.answer) {
              btnStyle = 'bg-green-600 text-white border-green-400 ring-4 ring-green-400/40 animate-pulse';
            } else if (option === selectedOption) {
              btnStyle = 'bg-red-600 text-white border-red-400';
            } else {
              btnStyle = 'bg-indigo-950/50 text-indigo-400 border-indigo-900/30 opacity-50';
            }
          }

          return (
            <button
              key={idx}
              onClick={() => handleOptionClick(option)}
              disabled={answered}
              className={`p-4 rounded-2xl font-bold text-left border-2 transition-all duration-200 shadow-md flex items-center justify-between ${btnStyle} cursor-pointer`}
            >
              <span className="flex items-center gap-3">
                <span className="w-7 h-7 rounded-lg bg-black/20 flex items-center justify-center text-xs font-extrabold">
                  {String.fromCharCode(65 + idx)}
                </span>
                <span className="text-sm sm:text-base">{option}</span>
              </span>

              {answered && option === questionData.answer && (
                <CheckCircle2 className="w-6 h-6 text-white flex-shrink-0" />
              )}
              {answered && option === selectedOption && option !== questionData.answer && (
                <XCircle className="w-6 h-6 text-white flex-shrink-0" />
              )}
            </button>
          );
        })}
      </div>

      {/* Feedback banner */}
      {answered && (
        <div className={`mt-6 p-4 rounded-2xl text-center font-black text-lg flex items-center justify-center gap-3 animate-bounce shadow-xl ${
          isCorrect ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
        }`}>
          {isCorrect ? (
            <>
              <CheckCircle2 className="w-7 h-7" />
              ¡Respuesta Correcta! ¡Ganas punto y turno!
            </>
          ) : (
            <>
              <XCircle className="w-7 h-7" />
              ¡Respuesta Incorrecta! Turno del siguiente jugador.
            </>
          )}
        </div>
      )}
    </div>
  );
};
