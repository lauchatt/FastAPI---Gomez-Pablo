import { ApiQuestion, CategoryKey, RouletteSector } from '../types/game';

export const CATEGORIES: CategoryKey[] = [
  'Geografía',
  'Historia',
  'Ciencia',
  'Entretenimiento',
  'Arte',
  'Deportes'
];

export const ROULETTE_SECTORS: RouletteSector[] = [
  'Geografía',
  'Historia',
  'Ciencia',
  'Corona',
  'Entretenimiento',
  'Arte',
  'Deportes'
];

const CATEGORY_SLUG_MAP: Record<CategoryKey, string> = {
  'Geografía': 'geografia',
  'Historia': 'historia',
  'Ciencia': 'ciencia',
  'Entretenimiento': 'entretenimiento',
  'Arte': 'arte',
  'Deportes': 'deporte',
};

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

// Translation cache and used question tracking to ensure non-repetition
const translationCache = new Map<string, string>();
const usedQuestionIds: Record<CategoryKey, Set<number>> = {
  'Geografía': new Set(),
  'Historia': new Set(),
  'Ciencia': new Set(),
  'Entretenimiento': new Set(),
  'Arte': new Set(),
  'Deportes': new Set(),
};

async function translateText(text: string): Promise<string> {
  if (!text || typeof text !== 'string') return text;
  if (translationCache.has(text)) {
    return translationCache.get(text)!;
  }

  try {
    const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(text)}&langpair=en|es`;
    const res = await fetch(url);
    if (res.ok) {
      const data = await res.json();
      if (data && data.responseData && data.responseData.translatedText) {
        const translated = data.responseData.translatedText;
        if (!translated.includes('MYMEMORY WARNING') && !translated.includes('QUOTA EXCEEDED')) {
          translationCache.set(text, translated);
          return translated;
        }
      }
    }
  } catch (error) {
    console.warn('[Translation] Failed to translate via MyMemory API, keeping original:', error);
  }

  translationCache.set(text, text);
  return text;
}

export async function fetchQuestionByApiOrMock(category: CategoryKey): Promise<ApiQuestion> {
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || '';
  const slug = CATEGORY_SLUG_MAP[category] || 'geografia';

  const endpoints = [
    `${apiBaseUrl}/questions/category/${slug}`,
    `${apiBaseUrl}/questions`
  ];

  for (const url of endpoints) {
    try {
      console.log(`[API] Fetching from ${url}`);
      const response = await fetch(url);
      console.log(`[API] Response status: ${response.status}`);
      if (response.ok) {
        const data = await response.json();
        console.log(`[API] Response data:`, data);

        let items = [];
        if (Array.isArray(data)) {
          items = data;
        } else if (data && Array.isArray(data.questions)) {
          items = data.questions;
        } else if (data && Array.isArray(data.items)) {
          items = data.items;
        } else if (data && typeof data === 'object' && (data.id || data.question)) {
          items = [data];
        }

        if (url.endsWith('/questions')) {
          items = items.filter((q: any) => 
            q.category?.toLowerCase() === category.toLowerCase() ||
            q.category?.toLowerCase() === slug.toLowerCase()
          );
        }

        if (items.length > 0) {
          // Filter out questions already used in this session to prevent immediate repetition
          let availableItems = items.filter((q: any) => !usedQuestionIds[category].has(q.id));
          if (availableItems.length === 0) {
            usedQuestionIds[category].clear();
            availableItems = items;
          }

          const randomIndex = Math.floor(Math.random() * availableItems.length);
          const q = availableItems[randomIndex];
          
          if (q.id) {
            usedQuestionIds[category].add(q.id);
          }

          console.log(`[API] Selected question item:`, q);

          const rawQuestion = q.question || q.pregunta || q.text || 'Pregunta sin texto';
          const rawAnswer = q.answer || q.respuesta || q.correct_answer || q.correcta || '';

          let optionsList: string[] = [];
          if (Array.isArray(q.options)) {
            optionsList = q.options;
          } else if (Array.isArray(q.opciones)) {
            optionsList = q.opciones;
          } else {
            optionsList = [
              q.option_1, q.option_2, q.option_3, q.option_4,
              q.opcion_1, q.opcion_2, q.opcion_3, q.opcion_4,
              q.opcion1, q.opcion2, q.opcion3, q.opcion4
            ].filter(Boolean);
          }

          if (rawAnswer && !optionsList.includes(rawAnswer)) {
            optionsList.push(rawAnswer);
          }

          const uniqueOptions = Array.from(new Set(optionsList));

          const finalOptions = uniqueOptions.length >= 2 
            ? uniqueOptions 
            : [rawAnswer || 'Respuesta', 'Opción A', 'Opción B', 'Opción C'];

          // Translate question, answer and options to Spanish
          const translatedQuestion = await translateText(rawQuestion);
          const translatedAnswer = await translateText(rawAnswer);
          const translatedOptions = await Promise.all(finalOptions.map(opt => translateText(opt)));

          if (translatedAnswer && !translatedOptions.includes(translatedAnswer)) {
            translatedOptions[0] = translatedAnswer;
          }

          return {
            id: q.id || Math.random(),
            question: translatedQuestion,
            answer: translatedAnswer || translatedOptions[0],
            category: category,
            source: q.source || 'FastAPI Backend DB',
            options: Array.from(new Set(translatedOptions))
          };
        }
      }
    } catch (error) {
      console.warn(`[API] Error fetching from ${url}:`, error);
    }
  }

  console.warn('[API] All API endpoints failed or returned empty. Falling back to local mock question.');
  // Fallback to local mock data
  const questionsList = MOCK_QUESTIONS[category] || MOCK_QUESTIONS['Geografía'];
  const randomIndex = Math.floor(Math.random() * questionsList.length);
  const q = questionsList[randomIndex];
  await new Promise((resolve) => setTimeout(resolve, 300));
  return { ...q, category };
}
