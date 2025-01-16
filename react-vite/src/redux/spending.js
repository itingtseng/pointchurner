// Action Types
const LOAD_USER_SPENDING = "spendings/load_user_spending";
const ADD_CATEGORY_TO_SPENDING = "spendings/add_category_to_spending";
const EDIT_CATEGORY_NOTES = "spending/editCategoryNotes";
const REMOVE_CATEGORY_FROM_SPENDING = "spendings/remove_category_from_spending";

// Action Creators
export const loadUserSpending = (spending) => ({
  type: LOAD_USER_SPENDING,
  spending,
});

export const addCategoryToSpending = (category) => ({
  type: ADD_CATEGORY_TO_SPENDING,
  category,
});

export const editCategoryNotes = (category) => ({
  type: EDIT_CATEGORY_NOTES,
  category,
});

export const removeCategoryFromSpending = (categoryId) => ({
  type: REMOVE_CATEGORY_FROM_SPENDING,
  categoryId,
});

// Thunks
export const thunkGetUserSpending = () => async (dispatch) => {
  try {
    const res = await fetch("/api/spendings/session");
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    dispatch(loadUserSpending(data));
  } catch (error) {
    console.error("Error fetching user's spending:", error);
    throw error;
  }
};

export const thunkAddCategoryToSpending =
  (categoryData) => async (dispatch) => {
    try {
      const res = await fetch("/api/spendings/categories", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(categoryData),
      });
      if (res.ok) {
        const data = await res.json();
        dispatch(addCategoryToSpending(data.category));
        // Refresh the spending profile after adding a category
        const updatedSpendingRes = await fetch("/api/spendings/session");
        if (updatedSpendingRes.ok) {
          const updatedSpending = await updatedSpendingRes.json();
          dispatch(loadUserSpending(updatedSpending));
        }
      } else {
        const error = await res.json();
        throw new Error(error.message || "Failed to add category to spending");
      }
    } catch (error) {
      console.error("Error adding category to spending:", error);
      throw error;
    }
  };

export const thunkEditCategoryNotes =
  (categoryId, notes) => async (dispatch) => {
    try {
      const res = await fetch(`/api/spendings/categories/${categoryId}/notes`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ notes }),
      });

      if (!res.ok) {
        const error = await res.json();
        throw new Error(
          error.message || "Failed to update notes for the category."
        );
      }

      const data = await res.json();
      dispatch(editCategoryNotes(data.category)); // Dispatch action to update Redux state
    } catch (error) {
      console.error("Error updating notes for the category:", error);
      throw error;
    }
  };

export const thunkRemoveCategoryFromSpending =
  (categoryId) => async (dispatch) => {
    try {
      const res = await fetch(`/api/spendings/categories/${categoryId}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error(await res.text());
      dispatch(removeCategoryFromSpending(categoryId));
    } catch (error) {
      console.error("Error removing category from spending:", error);
      throw error;
    }
  };

// Reducer
const initialState = { singleSpending: null };

function spendingReducer(state = initialState, action) {
  switch (action.type) {
    case LOAD_USER_SPENDING:
      return { ...state, singleSpending: action.spending };
    case ADD_CATEGORY_TO_SPENDING:
      if (!state.singleSpending) return state;
      return {
        ...state,
        singleSpending: {
          ...state.singleSpending,
          categories: [...state.singleSpending.categories, action.category],
        },
      };
    case REMOVE_CATEGORY_FROM_SPENDING:
      if (!state.singleSpending) return state;
      return {
        ...state,
        singleSpending: {
          ...state.singleSpending,
          categories: state.singleSpending.categories.filter(
            (category) => category.category_id !== action.categoryId
          ),
        },
      };
    case EDIT_CATEGORY_NOTES:
      return {
        ...state,
        singleSpending: {
          ...state.singleSpending,
          categories: state.singleSpending.categories.map((category) => {
            if (category.category_id === action.category.category_id) {
              return {
                ...category,
                notes: action.category.notes,
              };
            }
            return category;
          }),
        },
      };

    default:
      return state;
  }
}

export default spendingReducer;
