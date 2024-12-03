const LOAD_ALL_WALLETS = 'wallets/load_all_wallets';
const LOAD_WALLET_BY_ID = 'wallets/load_wallet_by_id';
const CREATE_WALLET = 'wallets/create_wallet';
const UPDATE_WALLET = 'wallets/update_wallet';
const DELETE_WALLET = 'wallets/delete_wallet';

// Action Creators
export const loadAllWallets = wallets => ({ type: LOAD_ALL_WALLETS, wallets });
export const loadWalletById = wallet => ({ type: LOAD_WALLET_BY_ID, wallet });
export const createWallet = wallet => ({ type: CREATE_WALLET, wallet });
export const updateWallet = wallet => ({ type: UPDATE_WALLET, wallet });
export const deleteWallet = walletId => ({ type: DELETE_WALLET, walletId });

// Thunks
export const thunkGetAllWallets = () => async dispatch => {
    const res = await fetch('/api/wallets');
    if (res.ok) {
        const data = await res.json();
        dispatch(loadAllWallets(data.wallets));
    }
};

export const thunkGetWalletById = walletId => async dispatch => {
    const res = await fetch(`/api/wallets/${walletId}`);
    if (res.ok) {
        const data = await res.json();
        dispatch(loadWalletById(data));
    }
};

export const thunkCreateWallet = wallet => async dispatch => {
    const res = await fetch('/api/wallets', {
        method: 'POST',
        body: wallet
    });
    if (res.ok) {
        const data = await res.json();
        dispatch(createWallet(data));
    }
};

export const thunkUpdateWallet = wallet => async dispatch => {
    const res = await fetch(`/api/wallets/${wallet.id}`, {
        method: 'PUT',
        body: wallet
    });
    if (res.ok) {
        const data = await res.json();
        dispatch(updateWallet(data));
    }
};

export const thunkDeleteWallet = walletId => async dispatch => {
    const res = await fetch(`/api/wallets/${walletId}`, { method: 'DELETE' });
    if (res.ok) {
        dispatch(deleteWallet(walletId));
    }
};

// Reducer
const initialState = { allWallets: {}, singleWallet: null };

export default function walletsReducer(state = initialState, action) {
    switch (action.type) {
        case LOAD_ALL_WALLETS:
            const allWallets = {};
            action.wallets.forEach(wallet => { allWallets[wallet.id] = wallet });
            return { ...state, allWallets };
        case LOAD_WALLET_BY_ID:
            return { ...state, singleWallet: action.wallet };
        case CREATE_WALLET:
            return { ...state, allWallets: { ...state.allWallets, [action.wallet.id]: action.wallet } };
        case UPDATE_WALLET:
            return { ...state, allWallets: { ...state.allWallets, [action.wallet.id]: action.wallet } };
        case DELETE_WALLET:
            const newState = { ...state };
            delete newState.allWallets[action.walletId];
            return newState;
        default:
            return state;
    }
}
