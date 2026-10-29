import React, { useState } from 'react';
import { Player, CategoryKey, RouletteSector, GameScreenType } from './types/game';
import { CATEGORIES } from './services/mockQuestions';
import { soundService } from './services/soundService';
import { SetupScreen } from './screens/SetupScreen';
import { GameScreen } from './screens/GameScreen';
import { QuestionScreen } from './screens/QuestionScreen';
import { CategoryChoiceScreen } from './screens/CategoryChoiceScreen';
import { TransitionScreen } from './screens/TransitionScreen';
import { GameOverScreen } from './screens/GameOverScreen';
import { Volume2, VolumeX, Music } from 'lucide-react';

export const App: React.FC = () => {
  const [screen, setScreen] = useState<GameScreenType>('SETUP');
  const [players, setPlayers] = useState<Player[]>([]);
  const [currentPlayerIndex, setCurrentPlayerIndex] = useState<number>(0);
  const [currentCategory, setCurrentCategory] = useState<CategoryKey>('Geografía');
  const [isCrownChallenge, setIsCrownChallenge] = useState<boolean>(false);
  const [bgmMuted, setBgmMuted] = useState<boolean>(soundService.isBgmMuted());
  const [sfxMuted, setSfxMuted] = useState<boolean>(soundService.isSfxMuted());

  const handleToggleBgm = () => {
    const muted = soundService.toggleBgm();
    setBgmMuted(muted);
  };

  const handleToggleSfx = () => {
    const muted = soundService.toggleSfx();
    setSfxMuted(muted);
  };

  const createInitialCrowns = (): Record<CategoryKey, boolean> => {
    const crowns = {} as Record<CategoryKey, boolean>;
    CATEGORIES.forEach((cat) => {
      crowns[cat] = false;
    });
    return crowns;
  };

  const handleStartGame = (p1Name: string, p1Avatar: string, p2Name: string, p2Avatar: string) => {
    const newPlayers: Player[] = [
      { id: 1, name: p1Name, avatar: p1Avatar, score: 0, accumulatedCrowns: 0, crowns: createInitialCrowns() },
      { id: 2, name: p2Name, avatar: p2Avatar, score: 0, accumulatedCrowns: 0, crowns: createInitialCrowns() }
    ];
    setPlayers(newPlayers);
    setCurrentPlayerIndex(0);
    setIsCrownChallenge(false);
    setScreen('ROULETTE');
    soundService.startBgm();
  };

  const handleSpinComplete = (sector: RouletteSector) => {
    if (sector === 'Corona') {
      setIsCrownChallenge(true);
      setScreen('CATEGORY_CHOICE');
    } else {
      setIsCrownChallenge(false);
      setCurrentCategory(sector as CategoryKey);
      setScreen('QUESTION');
    }
  };

  const handleCategoryChoice = (category: CategoryKey) => {
    setCurrentCategory(category);
    setIsCrownChallenge(true);
    setScreen('QUESTION');
  };

  const handleAnswerResult = (isCorrect: boolean) => {
    const updatedPlayers = [...players];
    const currentPlayer = { ...updatedPlayers[currentPlayerIndex] };

    if (isCorrect) {
      currentPlayer.score += 1;

      if (isCrownChallenge) {
        currentPlayer.crowns = {
          ...currentPlayer.crowns,
          [currentCategory]: true,
        };
        updatedPlayers[currentPlayerIndex] = currentPlayer;
        setPlayers(updatedPlayers);

        const hasWon = Object.values(currentPlayer.crowns).every(Boolean);
        if (hasWon) {
          soundService.stopBgm();
          setScreen('GAME_OVER');
          return;
        }

        setIsCrownChallenge(false);
        setScreen('ROULETTE');
      } else {
        currentPlayer.accumulatedCrowns += 1;
        updatedPlayers[currentPlayerIndex] = currentPlayer;
        setPlayers(updatedPlayers);

        if (currentPlayer.accumulatedCrowns >= 3) {
          currentPlayer.accumulatedCrowns -= 3;
          updatedPlayers[currentPlayerIndex] = currentPlayer;
          setPlayers(updatedPlayers);
          setIsCrownChallenge(true);
          setScreen('CATEGORY_CHOICE');
        } else {
          setScreen('ROULETTE');
        }
      }
    } else {
      setIsCrownChallenge(false);
      const nextIndex = currentPlayerIndex === 0 ? 1 : 0;
      setCurrentPlayerIndex(nextIndex);
      setScreen('TRANSITION');
    }
  };

  const handleTransitionContinue = () => {
    setScreen('ROULETTE');
  };

  const handleRestart = () => {
    soundService.stopBgm();
    setScreen('SETUP');
    setPlayers([]);
    setCurrentPlayerIndex(0);
    setIsCrownChallenge(false);
  };

  return (
    <div className="min-h-screen bg-indigo-950 text-white font-sans selection:bg-yellow-400 selection:text-indigo-950 relative">
      <div className="absolute top-4 right-4 z-50 flex items-center gap-2">
        <button
          onClick={handleToggleBgm}
          className="p-2.5 rounded-full bg-indigo-900/90 border border-yellow-400/60 text-yellow-300 hover:bg-indigo-800 transition-all shadow-lg flex items-center justify-center cursor-pointer"
          title={bgmMuted ? "Activar música de fondo" : "Silenciar música de fondo"}
        >
          {bgmMuted ? <VolumeX className="w-5 h-5 text-red-400" /> : <Music className="w-5 h-5 text-yellow-300" />}
        </button>
        <button
          onClick={handleToggleSfx}
          className="p-2.5 rounded-full bg-indigo-900/90 border border-yellow-400/60 text-yellow-300 hover:bg-indigo-800 transition-all shadow-lg flex items-center justify-center cursor-pointer"
          title={sfxMuted ? "Activar efectos de sonido" : "Silenciar efectos de sonido"}
        >
          {sfxMuted ? <VolumeX className="w-5 h-5 text-red-400" /> : <Volume2 className="w-5 h-5 text-yellow-300" />}
        </button>
      </div>

      {screen === 'SETUP' && <SetupScreen onStartGame={handleStartGame} />}

      {screen === 'ROULETTE' && players.length > 0 && (
        <GameScreen
          players={players}
          currentPlayerIndex={currentPlayerIndex}
          onSpinComplete={handleSpinComplete}
        />
      )}

      {screen === 'CATEGORY_CHOICE' && players.length > 0 && (
        <CategoryChoiceScreen
          player={players[currentPlayerIndex]}
          onSelectCategory={handleCategoryChoice}
        />
      )}

      {screen === 'QUESTION' && (
        <QuestionScreen
          category={currentCategory}
          isCrownChallenge={isCrownChallenge}
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
