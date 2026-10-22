import React, { useState } from 'react';
import { Player, CategoryKey, GameScreenType } from './types/game';
import { CATEGORIES } from './services/mockQuestions';
import { SetupScreen } from './screens/SetupScreen';
import { GameScreen } from './screens/GameScreen';
import { QuestionScreen } from './screens/QuestionScreen';
import { TransitionScreen } from './screens/TransitionScreen';
import { GameOverScreen } from './screens/GameOverScreen';

export const App: React.FC = () => {
  const [screen, setScreen] = useState<GameScreenType>('SETUP');
  const [players, setPlayers] = useState<Player[]>([]);
  const [currentPlayerIndex, setCurrentPlayerIndex] = useState<number>(0);
  const [currentCategory, setCurrentCategory] = useState<CategoryKey>('Geografía');

  const createInitialCrowns = (): Record<CategoryKey, boolean> => {
    const crowns = {} as Record<CategoryKey, boolean>;
    CATEGORIES.forEach((cat) => {
      crowns[cat] = false;
    });
    return crowns;
  };

  const handleStartGame = (p1Name: string, p2Name: string) => {
    const newPlayers: Player[] = [
      { id: 1, name: p1Name, score: 0, crowns: createInitialCrowns() },
      { id: 2, name: p2Name, score: 0, crowns: createInitialCrowns() }
    ];
    setPlayers(newPlayers);
    setCurrentPlayerIndex(0);
    setScreen('ROULETTE');
  };

  const handleSpinComplete = (category: CategoryKey) => {
    setCurrentCategory(category);
    setScreen('QUESTION');
  };

  const handleAnswerResult = (isCorrect: boolean) => {
    const updatedPlayers = [...players];
    const currentPlayer = { ...updatedPlayers[currentPlayerIndex] };

    if (isCorrect) {
      currentPlayer.score += 1;
      currentPlayer.crowns = {
        ...currentPlayer.crowns,
        [currentCategory]: true,
      };
      updatedPlayers[currentPlayerIndex] = currentPlayer;
      setPlayers(updatedPlayers);

      // Check win condition (all 6 crowns collected)
      const hasWon = Object.values(currentPlayer.crowns).every(Boolean);
      if (hasWon) {
        setScreen('GAME_OVER');
        return;
      }

      // Correct answer: player keeps the turn and spins again
      setScreen('ROULETTE');
    } else {
      // Incorrect answer: switch turn to the other player with transition screen
      const nextIndex = currentPlayerIndex === 0 ? 1 : 0;
      setCurrentPlayerIndex(nextIndex);
      setScreen('TRANSITION');
    }
  };

  const handleTransitionContinue = () => {
    setScreen('ROULETTE');
  };

  const handleRestart = () => {
    setScreen('SETUP');
    setPlayers([]);
    setCurrentPlayerIndex(0);
  };

  return (
    <div className="min-h-screen bg-indigo-950 text-white font-sans selection:bg-yellow-400 selection:text-indigo-950">
      {screen === 'SETUP' && <SetupScreen onStartGame={handleStartGame} />}

      {screen === 'ROULETTE' && players.length > 0 && (
        <GameScreen
          players={players}
          currentPlayerIndex={currentPlayerIndex}
          onSpinComplete={handleSpinComplete}
        />
      )}

      {screen === 'QUESTION' && (
        <QuestionScreen
          category={currentCategory}
          onAnswerResult={handleAnswerResult}
        />
      )}

      {screen === 'TRANSITION' && players.length > 0 && (
        <TransitionScreen
          nextPlayer={players[currentPlayerIndex]}
          onContinue={handleTransitionContinue}
        />
      )}

      {screen === 'GAME_OVER' && players.length > 0 && (
        <GameOverScreen
          players={players}
          onRestart={handleRestart}
        />
      )}
    </div>
  );
};

export default App;
