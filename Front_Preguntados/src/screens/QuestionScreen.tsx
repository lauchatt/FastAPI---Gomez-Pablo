import React, { useEffect, useState } from 'react';
import { ApiQuestion, CategoryKey } from '../types/game';
import { fetchQuestionByApiOrMock } from '../services/mockQuestions';
import { QuestionCard } from '../components/QuestionCard';
import { ErrorBanner } from '../components/ErrorBanner';
import { Loader2, Crown } from 'lucide-react';

interface QuestionScreenProps {
  category: CategoryKey;
  isCrownChallenge?: boolean;
  onAnswerResult: (isCorrect: boolean) => void;
}

export const QuestionScreen: React.FC<QuestionScreenProps> = ({ category, isCrownChallenge, onAnswerResult }) => {
  const [question, setQuestion] = useState<ApiQuestion | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);

    fetchQuestionByApiOrMock(category)
      .then((data) => {
        if (isMounted) {
          setQuestion(data);
          setLoading(false);
        }
      })
      .catch((err) => {
        console.error('Failed to fetch question', err);
        setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [category]);

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-indigo-950 via-purple-950 to-slate-950 text-white">
      <ErrorBanner />

      {isCrownChallenge && (
        <div className="bg-yellow-500 text-indigo-950 font-extrabold text-center py-2 px-4 shadow-md flex items-center justify-center gap-2 text-sm sm:text-base">
          <Crown className="w-5 h-5" />
          <span>¡PREGUNTA POR CORONA / INSIGNIA DE {category.toUpperCase()}!</span>
        </div>
      )}

      <div className="flex-1 flex items-center justify-center p-4">
        {loading || !question ? (
          <div className="flex flex-col items-center justify-center gap-3">
            <Loader2 className="w-12 h-12 text-yellow-400 animate-spin" />
            <p className="text-indigo-200 font-bold">Cargando pregunta de {category}...</p>
          </div>
        ) : (
          <QuestionCard questionData={question} onAnswerResult={onAnswerResult} />
        )}
      </div>
    </div>
  );
};
