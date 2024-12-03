const LOAD_ALL_CATEGORIES = 'categories/load_all_categories';
const LOAD_CATEGORY_BY_ID = 'categories/load_category_by_id';
const CREATE_CATEGORY = 'categories/create_category';
const UPDATE_CATEGORY = 'categories/update_category';
const DELETE_CATEGORY = 'categories/delete_category';

// Action Creators
export const loadAllCategories = categories => ({ type: LOAD_ALL_CATEGORIES, categories });
export const loadCategoryById = category => ({ type: LOAD_CATEGORY_BY_ID, category });
export const createCategory = category => ({ type: CREATE_CATEGORY, category });
export const updateCategory = category => ({ type: UPDATE_CATEGORY, category });
export const deleteCategory = categoryId => ({ type: DELETE_CATEGORY, categoryId });

// Thunks
export const thunkGetAllCategories = () => async dispatch => {
    const res = await fetch('/api/categories');
    if (res.ok) {
        const data = await res.json();
        dispatch(loadAllCategories(data.categories));
    }
};

export const thunkGetCategoryById = categoryId => async dispatch => {
    const res = await fetch(`/api/categories/${categoryId}`);
    if (res.ok) {
        const data = await res.json();
        dispatch(loadCategoryById(data));
    }
};

export const thunkCreateCategory = category => async dispatch => {
    const res = await fetch('/api/categories', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(category)
    });
    if (res.ok) {
        const data = await res.json();
        dispatch(createCategory(data));
    }
};

export const thunkUpdateCategory = category => async dispatch => {
    const res = await fetch(`/api/categories/${category.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(category)
    });
    if (res.ok) {
        const data = await res.json();
        dispatch(updateCategory(data));
    }
};

export const thunkDeleteCategory = categoryId => async dispatch => {
    const res = await fetch(`/api/categories/${categoryId}`, { method: 'DELETE' });
    if (res.ok) {
        dispatch(deleteCategory(categoryId));
    }
};

// Reducer
const initialState = { allCategories: {}, singleCategory: null };

export default function categoriesReducer(state = initialState, action) {
    switch (action.type) {
        case LOAD_ALL_CATEGORIES:
            const allCategories = {};
            action.categories.forEach(category => { allCategories[category.id] = category });
            return { ...state, allCategories };
        case LOAD_CATEGORY_BY_ID:
            return { ...state, singleCategory: action.category };
        case CREATE_CATEGORY:
            return { ...state, allCategories: { ...state.allCategories, [action.category.id]: action.category } };
        case UPDATE_CATEGORY:
            return { ...state, allCategories: { ...state.allCategories, [action.category.id]: action.category } };
        case DELETE_CATEGORY:
            const newState = { ...state };
            delete newState.allCategories[action.categoryId];
            return newState;
        default:
            return state;
    }
}
