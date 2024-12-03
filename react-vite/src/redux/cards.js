const LOAD_ALL_CARDS = 'cards/load_all_cards';
const LOAD_CARD_BY_ID = 'cards/load_card_by_id';
const CREATE_CARD = 'cards/create_card';
const UPDATE_CARD = 'cards/update_card';
const DELETE_CARD = 'cards/delete_card';

// Action Creators
export const loadAllCards = cards => ({ type: LOAD_ALL_CARDS, cards });
export const loadCardById = card => ({ type: LOAD_CARD_BY_ID, card });
export const createCard = card => ({ type: CREATE_CARD, card });
export const updateCard = card => ({ type: UPDATE_CARD, card });
export const deleteCard = cardId => ({ type: DELETE_CARD, cardId });

// Thunks
export const thunkGetAllCards = () => async dispatch => {
    const res = await fetch('/api/cards');
    if (res.ok) {
        const data = await res.json();
        dispatch(loadAllCards(data.cards));
    }
};

export const thunkGetCardById = cardId => async dispatch => {
    const res = await fetch(`/api/cards/${cardId}`);
    if (res.ok) {
        const data = await res.json();
        dispatch(loadCardById(data));
    }
};

export const thunkCreateCard = card => async dispatch => {
    const res = await fetch('/api/cards', {
        method: 'POST',
        body: card
    });
    if (res.ok) {
        const data = await res.json();
        dispatch(createCard(data));
    }
};

export const thunkUpdateCard = card => async dispatch => {
    const res = await fetch(`/api/cards/${card.id}`, {
        method: 'PUT',
        body: card
    });
    if (res.ok) {
        const data = await res.json();
        dispatch(updateCard(data));
    }
};

export const thunkDeleteCard = cardId => async dispatch => {
    const res = await fetch(`/api/cards/${cardId}`, { method: 'DELETE' });
    if (res.ok) {
        dispatch(deleteCard(cardId));
    }
};

// Reducer
const initialState = { allCards: {}, singleCard: null };

export default function cardsReducer(state = initialState, action) {
    switch (action.type) {
        case LOAD_ALL_CARDS:
            const allCards = {};
            action.cards.forEach(card => { allCards[card.id] = card });
            return { ...state, allCards };
        case LOAD_CARD_BY_ID:
            return { ...state, singleCard: action.card };
        case CREATE_CARD:
            return { ...state, allCards: { ...state.allCards, [action.card.id]: action.card } };
        case UPDATE_CARD:
            return { ...state, allCards: { ...state.allCards, [action.card.id]: action.card } };
        case DELETE_CARD:
            const newState = { ...state };
            delete newState.allCards[action.cardId];
            return newState;
        default:
            return state;
    }
}
