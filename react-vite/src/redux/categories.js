// Action Types
const LOAD_ALL_CATEGORIES = 'categories/load_all_categories';
const LOAD_CATEGORY_BY_ID = 'categories/load_category_by_id';

// Action Creators
export const loadAllCategories = (categories) => ({ type: LOAD_ALL_CATEGORIES, categories });
export const loadCategoryById = (category) => ({ type: LOAD_CATEGORY_BY_ID, category });

// Thunks
export const thunkGetAllCategories = () => async (dispatch) => {
  const res = await fetch('/api/categories');
  if (res.ok) {
    const data = await res.json();
    dispatch(loadAllCategories(data.categories));
  } else {
    console.error('Failed to fetch all categories');
  }
};

export const thunkGetCategoryById = (categoryId) => async (dispatch) => {
  const res = await fetch(`/api/categories/${categoryId}`);
  if (res.ok) {
    const data = await res.json();
    dispatch(loadCategoryById(data));
  } else {
    console.error(`Failed to fetch category with ID: ${categoryId}`);
  }
};

// Reducer
const initialState = { allCategories: {}, singleCategory: null };

export default function categoriesReducer(state = initialState, action) {
  switch (action.type) {
    case LOAD_ALL_CATEGORIES: {
      const allCategories = {};
      action.categories.forEach((category) => {
        allCategories[category.id] = category;
      });
      return { ...state, allCategories };
    }
    case LOAD_CATEGORY_BY_ID: {
      return { ...state, singleCategory: action.category };
    }
    default:
      return state;
  }
}
