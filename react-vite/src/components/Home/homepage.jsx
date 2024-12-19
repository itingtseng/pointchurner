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

  // Get user, cards, wallet, spending, and categories from Redux store
  const user = useSelector((state) => state.session.user);
  const cards = useSelector((state) => Object.values(state.cards.allCards));
  const categories = useSelector((state) =>
    Object.values(state.categories.allCategories)
  );
  const wallet = useSelector((state) => state.wallet.singleWallet);
  const spending = useSelector((state) => state.spending.singleSpending);

  useEffect(() => {
    if (user) {
      // Fetch wallet and spending data for logged-in users
      dispatch(thunkGetUserWallet());
      dispatch(thunkGetUserSpending());
    } else {
      // Fetch all cards and categories for non-logged-in users
      dispatch(thunkGetAllCards());
      dispatch(thunkGetAllCategories());
    }
  }, [dispatch, user]);

  const capitalizeWords = (string) => {
    return string
      .split(" ")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };

  // Helper function to deduplicate and process only leaf categories
  const processCategories = (categories) => {
    const leafCategories = new Set();
    categories.forEach((category) => {
      const isChild = categories.some(
        (parent) => parent.name === category.parent_name
      );
      if (!isChild) {
        leafCategories.add(capitalizeWords(category.name));
      }
    });
    return Array.from(leafCategories);
  };

  // Get the best card for a given spending category
  const getBestCardForCategory = (category) => {
    if (!wallet || !wallet.cards) return [];

    const relevantCards = wallet.cards.filter(
      (card) =>
        Array.isArray(card.reward_points) &&
        card.reward_points.some((reward) => reward.category_name === category)
    );

    if (relevantCards.length > 0) {
      return [
        relevantCards.sort(
          (a, b) =>
            Math.max(
              ...b.reward_points
                .filter((reward) => reward.category_name === category)
                .map((reward) => reward.bonus_point)
            ) -
            Math.max(
              ...a.reward_points
                .filter((reward) => reward.category_name === category)
                .map((reward) => reward.bonus_point)
            )
        )[0],
      ];
    }

    // If no match, return all cards with a default reward
    return wallet.cards.map((card) => ({
      ...card,
      reward_points: [
        {
          category_name: category,
          bonus_point: 1,
          multiplier_type: "points per dollar",
        },
      ],
    }));
  };

  // Generate bonus details for a given card and category
  const getCardBonusDetails = (card, category) => {
    const reward = card.reward_points?.find(
      (reward) => reward.category_name === category
    );
    return reward
      ? `You'll earn ${reward.bonus_point} ${reward.multiplier_type} for your spending.`
      : null;
  };

  if (!user) {
    // Non-logged-in user view
    return (
      <div className="container">
        <h1>Welcome!</h1>
        <h2>Explore 154 Cards</h2>
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

        <h2>35 Categories</h2>
        <div className="categories">
          {categories.length > 0 ? (
            categories.map((category) => (
              <div key={category.id} className="category">
                {capitalizeWords(category.name)}
              </div>
            ))
          ) : (
            <p>No categories available</p>
          )}
        </div>
      </div>
    );
  }

  // Process spending categories and find recommendations for logged-in users
  const spendingCategories = spending?.categories || [];
  const leafCategories = processCategories(spendingCategories);

  const spendingRecommendations = leafCategories.map((category) => {
    const recommendedCards = getBestCardForCategory(category);
    return {
      category,
      cards: recommendedCards.map((card) => ({
        ...card,
        bonusDetails: getCardBonusDetails(card, category),
      })),
    };
  });

  return (
    <div className="container">
      <h1>Welcome Back!</h1>
      <h2>Recommended Cards for Your Spending</h2>
      <div className="recommendations">
        {spendingRecommendations?.map((rec, index) => (
          <div key={index} className="recommendation">
            <h3>Category: {capitalizeWords(rec.category)}</h3>
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
                    {card.bonusDetails && (
                      <p className="bonusDetails">{card.bonusDetails}</p>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p>
                No specific card available for this category. Check below for
                all cards.
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default HomePage;
