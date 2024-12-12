// Action Types
const LOAD_ALL_CARDS = 'cards/load_all_cards';
const LOAD_CARD_BY_ID = 'cards/load_card_by_id';
const CREATE_CARD = 'cards/create_card';
const UPDATE_CARD = 'cards/update_card';

// Action Creators
export const loadAllCards = (cards) => ({ type: LOAD_ALL_CARDS, cards });
export const loadCardById = (card) => ({ type: LOAD_CARD_BY_ID, card });
export const createCard = (card) => ({ type: CREATE_CARD, card });
export const updateCard = (card) => ({ type: UPDATE_CARD, card });

// Thunks
export const thunkGetAllCards = () => async (dispatch) => {
  const res = await fetch('/api/cards');
  if (res.ok) {
    const data = await res.json();
    dispatch(loadAllCards(data.cards));
  } else {
    console.error('Failed to fetch all cards');
  }
};

export const thunkGetCardById = (cardId) => async (dispatch) => {
  const res = await fetch(`/api/cards/${cardId}`);
  if (res.ok) {
    const data = await res.json();
    dispatch(loadCardById(data));
  } else {
    console.error(`Failed to fetch card with ID: ${cardId}`);
  }
};

export const thunkCreateCard = (cardData) => async (dispatch) => {
  const res = await fetch('/api/cards', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(cardData),
  });
  if (res.ok) {
    const data = await res.json();
    dispatch(createCard(data));
  } else {
    console.error('Failed to create card');
  }
};

export const thunkUpdateCard = (cardId, cardData) => async (dispatch) => {
  const res = await fetch(`/api/cards/${cardId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(cardData),
  });
  if (res.ok) {
    const data = await res.json();
    dispatch(updateCard(data));
  } else {
    console.error(`Failed to update card with ID: ${cardId}`);
  }
};

// Reducer
const initialState = { allCards: {}, singleCard: null };

export default function cardsReducer(state = initialState, action) {
  switch (action.type) {
    case LOAD_ALL_CARDS: {
      const allCards = {};
      action.cards.forEach((card) => {
        allCards[card.id] = card;
      });
      return { ...state, allCards };
    }
    case LOAD_CARD_BY_ID: {
      return { ...state, singleCard: action.card };
    }
    case CREATE_CARD: {
      return {
        ...state,
        allCards: { ...state.allCards, [action.card.id]: action.card },
      };
    }
    case UPDATE_CARD: {
      return {
        ...state,
        allCards: { ...state.allCards, [action.card.id]: action.card },
      };
    }
    default:
      return state;
  }
}
