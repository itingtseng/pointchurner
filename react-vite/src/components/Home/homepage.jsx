import React, { useEffect } from "react";
import { Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { thunkGetAllCards } from "../../redux/cards";
import { thunkGetAllCategories } from "../../redux/categories";
import { thunkGetUserWallet } from "../../redux/wallet";
import { thunkGetUserSpending } from "../../redux/spending";
import "./homepage.css";

const HomePage = () => {
  const dispatch = useDispatch();

  // Get user, cards, categories, wallet, and spending data from Redux
  const user = useSelector((state) => state.session.user);
  const cards = useSelector((state) => Object.values(state.cards.allCards));
  const categories = useSelector((state) =>
    Object.values(state.categories.allCategories)
  );
  const wallet = useSelector((state) => state.wallet.singleWallet);
  const spending = useSelector((state) => state.spending.singleSpending);

  // Fetch data based on user's login state
  useEffect(() => {
    if (user) {
      dispatch(thunkGetUserWallet());
      dispatch(thunkGetUserSpending());
    } else {
      dispatch(thunkGetAllCards());
      dispatch(thunkGetAllCategories());
    }
  }, [dispatch, user]);

  // Function to deduplicate and process only leaf categories
  const processCategories = (categories) => {
    const leafCategories = new Set();
    categories.forEach((category) => {
      const isChild = categories.some(
        (parent) => parent.name === category.parent_name
      );
      if (!isChild) {
        leafCategories.add(category.name);
      }
    });
    return Array.from(leafCategories);
  };

  // Function to find the best card for each spending category
  const getBestCardForCategory = (category) => {
    if (!wallet || !wallet.cards) return [];
    const relevantCards = wallet.cards.filter(
      (card) =>
        Array.isArray(card.reward_points) &&
        card.reward_points.some((reward) => reward.category === category)
    );

    if (relevantCards.length > 0) {
      return [
        relevantCards.sort(
          (a, b) =>
            Math.max(
              ...b.reward_points
                .filter((reward) => reward.category === category)
                .map((reward) => reward.bonus_point)
            ) -
            Math.max(
              ...a.reward_points
                .filter((reward) => reward.category === category)
                .map((reward) => reward.bonus_point)
            )
        )[0],
      ]; // Return the best card
    }

    return wallet.cards; // Return all cards if no match
  };

  // Conditional rendering for before and after login
  if (!user) {
    return (
      <div className="container">
        <h1>Welcome!</h1>
        <h2>Explore All Cards</h2>
        <div className="grid">
          {cards.length > 0 ? (
            cards.map((card) => (
              <Link to={`/cards/${card.id}`} key={card.id} className="card">
                <img
                  src={`http://localhost:8000${card.image_url}`}
                  alt={card.name}
                  className="image"
                  loading="lazy"
                />
                <p className="cardName">{card.name}</p>
              </Link>
            ))
          ) : (
            <p>No cards available</p>
          )}
        </div>

        <h2>Categories</h2>
        <div className="categories">
          {categories.length > 0 ? (
            categories.map((category) => (
              <div key={category.id} className="category">
                {category.name}
              </div>
            ))
          ) : (
            <p>No categories available</p>
          )}
        </div>
      </div>
    );
  }

  // Process spending categories and find recommendations
  const spendingCategories = spending?.categories || [];
  const leafCategories = processCategories(spendingCategories);

  const spendingRecommendations = leafCategories.map((category) => {
    const recommendedCards = getBestCardForCategory(category);
    return {
      category,
      cards: recommendedCards,
    };
  });

  return (
    <div className="container">
      <h1>Welcome Back!</h1>
      <h2>Recommended Cards for Your Spending</h2>
      <div className="recommendations">
        {spendingRecommendations?.map((rec, index) => (
          <div key={index} className="recommendation">
            <h3>Category: {rec.category}</h3>
            {rec.cards.length > 0 ? (
              <div className="grid">
                {rec.cards.map((card) => (
                  <div key={card.id} className="card">
                    <img
                      src={`http://localhost:8000${card.image_url}`}
                      alt={card.name}
                      className="image"
                    />
                    <p className="cardName">{card.name}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p>No cards available for this category.</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default HomePage;
