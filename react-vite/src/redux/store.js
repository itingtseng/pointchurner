import {
  legacy_createStore as createStore,
  applyMiddleware,
  compose,
  combineReducers,
} from "redux";
import thunk from "redux-thunk";
import sessionReducer from "./session";
import cardsReducer from "./cards";
import categoriesReducer from "./categories";
import spendingReducer from "./spending";
import walletReducer from "./wallet";

// Custom logging middleware
const loggingMiddleware = (store) => (next) => (action) => {
  console.log("Action dispatched:", action); // Logs the dispatched action
  const result = next(action); // Pass the action to the next middleware or reducer
  console.log("New state after action:", store.getState()); // Logs the new state
  return result; // Returns the result of `next(action)`
};

// Combine reducers
const rootReducer = combineReducers({
  session: sessionReducer,
  cards: cardsReducer,
  categories: categoriesReducer,
  spending: spendingReducer,
  wallet: walletReducer,
});

let enhancer;
if (import.meta.env.MODE === "production") {
  // Apply middleware in production (can include logging if desired)
  enhancer = applyMiddleware(thunk);
} else {
  // Apply middleware in development
  const logger = (await import("redux-logger")).default;
  const composeEnhancers =
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
  enhancer = composeEnhancers(applyMiddleware(thunk, loggingMiddleware, logger));
}

// Create and configure the Redux store
const configureStore = (preloadedState) => {
  return createStore(rootReducer, preloadedState, enhancer);
};

export default configureStore;
