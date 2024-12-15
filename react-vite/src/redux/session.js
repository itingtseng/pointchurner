// Action Types
const SET_USER = "session/setUser";
const REMOVE_USER = "session/removeUser";

// Action creator for setting the user
const setUser = (user) => {
  console.log("Setting user with wallet_id and spending_id:", user.wallet_id, user.spending_id); // Debug user payload
  return {
    type: SET_USER,
    payload: {
      ...user,
      wallet_id: user.wallet_id || null,
      spending_id: user.spending_id || null, // Ensure spending_id is handled
    },
  };
};

// Action creator for removing the user
const removeUser = () => ({
  type: REMOVE_USER,
});

// Centralized error handling
const handleError = async (response) => {
  if (response.status < 500) {
    const errorMessages = await response.json();
    return errorMessages;
  }
  return { server: "Something went wrong. Please try again later." };
};

// Thunk for authenticating the session user
export const thunkAuthenticate = () => async (dispatch) => {
  try {
    const response = await fetch("/api/auth/");
    if (response.ok) {
      const data = await response.json();
      console.log("Fetched session user:", data); // Debug log
      dispatch(setUser(data));
    } else {
      console.error("Failed to authenticate session user.");
    }
  } catch (error) {
    console.error("Error authenticating session user:", error);
  }
};

// Thunk for logging in a user
export const thunkLogin = (credentials) => async (dispatch) => {
  try {
    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials),
    });

    if (response.ok) {
      const data = await response.json();
      dispatch(setUser(data));
    } else {
      return handleError(response);
    }
  } catch (error) {
    console.error("Error logging in user:", error);
  }
};

// Thunk for signing up a new user
export const thunkSignup = (user) => async (dispatch) => {
  try {
    const response = await fetch("/api/auth/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(user),
    });

    if (response.ok) {
      const data = await response.json();
      dispatch(setUser(data));
    } else {
      return handleError(response);
    }
  } catch (error) {
    console.error("Error signing up user:", error);
  }
};

// Thunk for logging out the user
export const thunkLogout = (navigate) => async (dispatch) => {
  try {
    const response = await fetch("/api/auth/logout", { method: "POST" });
    if (response.ok) {
      dispatch(removeUser());
      navigate("/"); // Redirect to the homepage
    } else {
      console.error("Failed to log out user:", await response.text());
    }
  } catch (error) {
    console.error("Error logging out user:", error);
  }
};

// Thunk to fetch the session user
export const fetchSessionUser = () => async (dispatch) => {
  try {
    const response = await fetch("/api/users/session");
    if (response.ok) {
      const data = await response.json();
      dispatch(setUser(data));
    } else if (response.status === 401) {
      // Clear session and redirect
      dispatch(removeUser());
      window.location.href = "/login"; // Redirect to login
    } else {
      console.error("Failed to fetch session user:", await response.text());
    }
  } catch (error) {
    console.error("Error fetching session user:", error);
  }
};


// Initial state
const initialState = { user: null };

// Session reducer to manage the user state
function sessionReducer(state = initialState, action) {
  switch (action.type) {
    case SET_USER:
      return { ...state, user: action.payload }; // Update user state with payload
    case REMOVE_USER:
      return { ...state, user: null }; // Clear user state on logout
    default:
      return state;
  }
}

export default sessionReducer;
