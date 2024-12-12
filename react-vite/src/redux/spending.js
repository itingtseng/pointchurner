// Action Types
const LOAD_ALL_SPENDINGS = 'spendings/load_all_spendings';
const LOAD_SPENDING_BY_ID = 'spendings/load_spending_by_id';
const CREATE_SPENDING = 'spendings/create_spending';
const UPDATE_SPENDING = 'spendings/update_spending';
const DELETE_SPENDING = 'spendings/delete_spending';

// Action Creators
export const loadAllSpendings = (spendings) => ({ type: LOAD_ALL_SPENDINGS, spendings });
export const loadSpendingById = (spending) => ({ type: LOAD_SPENDING_BY_ID, spending });
export const createSpending = (spending) => ({ type: CREATE_SPENDING, spending });
export const updateSpending = (spending) => ({ type: UPDATE_SPENDING, spending });
export const deleteSpending = (spendingId) => ({ type: DELETE_SPENDING, spendingId });

// Thunks
export const thunkGetAllSpendings = () => async (dispatch) => {
  const res = await fetch('/api/spendings');
  if (res.ok) {
    const data = await res.json();
    dispatch(loadAllSpendings(data.spendings));
  } else {
    console.error('Failed to fetch all spendings');
  }
};

export const thunkGetSpendingById = (spendingId) => async (dispatch) => {
  const res = await fetch(`/api/spendings/${spendingId}`);
  if (res.ok) {
    const data = await res.json();
    dispatch(loadSpendingById(data));
  } else {
    console.error(`Failed to fetch spending with ID: ${spendingId}`);
  }
};

export const thunkCreateSpending = (spending) => async (dispatch) => {
  const res = await fetch('/api/spendings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(spending),
  });
  if (res.ok) {
    const data = await res.json();
    dispatch(createSpending(data));
  } else {
    console.error('Failed to create spending');
  }
};

export const thunkUpdateSpending = (spending) => async (dispatch) => {
  const res = await fetch(`/api/spendings/${spending.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(spending),
  });
  if (res.ok) {
    const data = await res.json();
    dispatch(updateSpending(data));
  } else {
    console.error(`Failed to update spending with ID: ${spending.id}`);
  }
};

export const thunkDeleteSpending = (spendingId) => async (dispatch) => {
  const res = await fetch(`/api/spendings/${spendingId}`, {
    method: 'DELETE',
  });
  if (res.ok) {
    dispatch(deleteSpending(spendingId));
  } else {
    console.error(`Failed to delete spending with ID: ${spendingId}`);
  }
};

// Reducer
const initialState = { allSpendings: {}, singleSpending: null };

function spendingReducer(state = initialState, action) {
  switch (action.type) {
    case LOAD_ALL_SPENDINGS: {
      const allSpendings = {};
      action.spendings.forEach((spending) => {
        allSpendings[spending.id] = spending;
      });
      return { ...state, allSpendings };
    }
    case LOAD_SPENDING_BY_ID: {
      return { ...state, singleSpending: action.spending };
    }
    case CREATE_SPENDING: {
      return {
        ...state,
        allSpendings: {
          ...state.allSpendings,
          [action.spending.id]: action.spending,
        },
      };
    }
    case UPDATE_SPENDING: {
      return {
        ...state,
        allSpendings: {
          ...state.allSpendings,
          [action.spending.id]: action.spending,
        },
      };
    }
    case DELETE_SPENDING: {
      const newState = { ...state };
      delete newState.allSpendings[action.spendingId];
      return newState;
    }
    default:
      return state;
  }
}

export default spendingReducer