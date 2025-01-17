import React, { useEffect } from "react";
import { Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { thunkGetAllCards } from "../../redux/cards";
import { thunkGetAllCategories } from "../../redux/categories";
import { thunkGetUserWallet } from "../../redux/wallet";
import { thunkGetUserSpending } from "../../redux/spending";
import "./homepage.css";
import BASE_URL from "../../config";

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
      dispatch(thunkGetUserWallet());
      dispatch(thunkGetUserSpending());
    } else {
      dispatch(thunkGetAllCards());
      dispatch(thunkGetAllCategories());
    }
  }, [dispatch, user]);
  
  useEffect(() => {
    console.log("Spending Categories:", spending?.categories || []);
    console.log("Wallet Cards:", wallet?.cards || []);
  }, [spending, wallet]);
  

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
      console.log("Processing Category:", category);
      const isChild = categories.some(
        (parent) => parent.name === category.parent_name
      );
      if (!isChild) {
        leafCategories.add(capitalizeWords(category.name));
      }
    });
    console.log("Leaf Categories:", Array.from(leafCategories));
    return Array.from(leafCategories);
  };
  

  // Get the best card for a given spending category
  const getBestCardForCategory = (category) => {
    if (!wallet || !wallet.cards) return [];

    console.log(`Processing category: ${category}`);
    console.log("Wallet Cards:", wallet.cards);
    wallet.cards.forEach((card) => {
      console.log(`Card: ${card.name}`, card); // Log full card data
    });
    
  
    const normalizedCategory = category.toLowerCase().trim();
  
    const relevantCards = wallet.cards.filter(
      (card) =>
        Array.isArray(card.reward_points) &&
        card.reward_points.some(
          (reward) => reward.category_name.toLowerCase().trim() === normalizedCategory
        )
    );
  
    if (relevantCards.length > 0) {
      return [
        relevantCards.sort(
          (a, b) =>
            Math.max(
              ...b.reward_points
                .filter(
                  (reward) =>
                    reward.category_name.toLowerCase().trim() === normalizedCategory
                )
                .map((reward) => reward.bonus_point)
            ) -
            Math.max(
              ...a.reward_points
                .filter(
                  (reward) =>
                    reward.category_name.toLowerCase().trim() === normalizedCategory
                )
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
  
  const getCardBonusDetails = (card, category) => {
    const normalizedCategory = category.toLowerCase().trim();
    const reward = card.reward_points?.find(
      (reward) =>
        reward.category_name.toLowerCase().trim() === normalizedCategory
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
        <h2>Explore 156 Cards</h2>
        <p>Maximize Rewards On Every Purchase</p>
        <div className="grid-log-out">
          {cards.length > 0 ? (
            cards.map((card) => (
              <Link to={`/cards/${card.id}`} key={card.id} className="card-log-out">
                <img
                  src={`${BASE_URL}${card.image_url}`}
                  alt={card.name}
                  className="image"
                  loading="lazy"
                />
                {/* <p className="cardName">{card.name}</p> */}
              </Link>
            ))
          ) : (
            <p>No cards available</p>
          )}
        </div>

        <h2>37 Categories</h2>
        <p>Align Spending with Your Goals</p>
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
    console.log("Processing Category:", category);
    const recommendedCards = getBestCardForCategory(category);
    console.log("Recommended Cards for Category:", category, recommendedCards);
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
              <div className="grid-log-in">
                {rec.cards.map((card) => (
                  <div key={card.id} className="card-log-in">
                    <img
                      src={`${BASE_URL}${card.image_url}`}
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
