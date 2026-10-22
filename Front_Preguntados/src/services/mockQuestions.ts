import { ApiQuestion, CategoryKey } from '../types/game';

/**
 * ============================================================================
 * TEMPORARY LOCAL DATA SERVICE (UI DEVELOPMENT ONLY)
 * ============================================================================
 * 
 * TODO: Replace this mock service with actual integration against the FastAPI backend
 * running at http://localhost:8000/questions/<id>
 * 
 * The FastAPI backend endpoint specification:
 * GET http://localhost:8000/questions/{id}
 * Response format:
 * {
 *   "id": number,
 *   "question": string,
 *   "answer": string,
 *   "category": string,
 *   "source": string
 * }
 * ============================================================================
 */

export const CATEGORIES: CategoryKey[] = [
  'Geografía',
  'Historia',
  'Ciencia',
  'Entretenimiento',
  'Arte',
  'Deportes'
];

const MOCK_QUESTIONS: Record<CategoryKey, ApiQuestion[]> = {
  'Geografía': [
    {
      id: 1,
      question: '¿Cuál es la capital de Argentina?',
      answer: 'Buenos Aires',
      category: 'Geografía',
      source: 'Wikipedia',
      options: ['Buenos Aires', 'Córdoba', 'Rosario', 'Mendoza']
    },
    {
      id: 2,
      question: '¿Cuál es el río más largo del mundo?',
      answer: 'Río Amazonas',
      category: 'Geografía',
      source: 'Enciclopedia Geográfica',
      options: ['Río Nilo', 'Río Amazonas', 'Río Mississippi', 'Río Yangtsé']
    },
    {
      id: 3,
      question: '¿En qué país se encuentra la torre de Pisa?',
      answer: 'Italia',
      category: 'Geografía',
      source: 'Guía Mundial',
      options: ['Francia', 'España', 'Italia', 'Grecia']
    }
  ],
  'Historia': [
    {
      id: 4,
      question: '¿En qué año comenzó la Revolución Francesa?',
      answer: '1789',
      category: 'Historia',
      source: 'Historia Universal',
      options: ['1789', '1810', '1492', '1914']
    },
    {
      id: 5,
      question: '¿Quién fue el primer presidente de los Estados Unidos?',
      answer: 'George Washington',
      category: 'Historia',
      source: 'Archivo Histórico',
      options: ['Abraham Lincoln', 'Thomas Jefferson', 'George Washington', 'Benjamin Franklin']
    }
  ],
  'Ciencia': [
    {
      id: 6,
      question: '¿Cuál es el elemento químico cuyo símbolo es Au?',
      answer: 'Oro',
      category: 'Ciencia',
      source: 'Tabla Periódica',
      options: ['Plata', 'Oro', 'Cobre', 'Aluminio']
    },
    {
      id: 7,
      question: '¿Qué planeta es conocido como el planeta rojo?',
      answer: 'Marte',
      category: 'Ciencia',
      source: 'Astronomía Hoy',
      options: ['Venus', 'Marte', 'Júpiter', 'Saturno']
    }
  ],
  'Entretenimiento': [
    {
      id: 8,
      question: '¿Quién dirigió la película "Jurassic Park" (1993)?',
      answer: 'Steven Spielberg',
      category: 'Entretenimiento',
      source: 'IMDb',
      options: ['George Lucas', 'James Cameron', 'Steven Spielberg', 'Quentin Tarantino']
    }
  ],
  'Arte': [
    {
      id: 9,
      question: '¿Quién pintó la obra "La noche estrellada"?',
      answer: 'Vincent van Gogh',
      category: 'Arte',
      source: 'Museo de Arte',
      options: ['Pablo Picasso', 'Claude Monet', 'Vincent van Gogh', 'Salvador Dalí']
    }
  ],
  'Deportes': [
    {
      id: 10,
      question: '¿Cada cuántos años se celebran los Juegos Olímpicos?',
      answer: '4 años',
      category: 'Deportes',
      source: 'Comité Olímpico',
      options: ['2 años', '3 años', '4 años', '5 años']
    }
  ]
};

export async function fetchQuestionByApiOrMock(category: CategoryKey): Promise<ApiQuestion> {
  // If VITE_API_BASE_URL is configured, we could attempt to call FastAPI
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
  
  try {
    // Attempt real API fetch if endpoint supports it or fallback gracefully
    // Note: The prompt states: "El backend real utiliza http://localhost:8000/questions/<id>"
    // For development without live backend, we use temporary mock data.
    const questionsList = MOCK_QUESTIONS[category] || MOCK_QUESTIONS['Geografía'];
    const randomIndex = Math.floor(Math.random() * questionsList.length);
    const q = questionsList[randomIndex];
    
    // Simulate slight network latency
    await new Promise((resolve) => setTimeout(resolve, 400));
    return { ...q, category };
  } catch (error) {
    console.warn('API fetch failed, falling back to local mock question', error);
    const fallbackList = MOCK_QUESTIONS['Geografía'];
    return { ...fallbackList[0], category };
  }
}
