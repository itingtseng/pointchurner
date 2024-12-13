import React, { useEffect } from "react";
import { Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { thunkGetAllCards } from "../../redux/cards"; // Adjust the path if needed
import { thunkGetAllCategories } from "../../redux/categories"; // Adjust the path if needed
import "./homepage.css";

const HomePage = () => {
  const dispatch = useDispatch();

  // Fetch cards and categories from Redux
  useEffect(() => {
    dispatch(thunkGetAllCards());
    dispatch(thunkGetAllCategories());
  }, [dispatch]);

  // Get cards and categories from Redux store
  const cards = useSelector((state) => Object.values(state.cards.allCards));
  const categories = useSelector((state) => Object.values(state.categories.allCategories));

  return (
    <div className="container">
      <h1>All Cards</h1>
      <div className="grid">
        {cards.length > 0 ? (
          cards.map((card) => (
            <Link to={`/cards/${card.id}`} key={card.id} className="card">
              <img
                src={`http://localhost:8000${card.image_url}`} // Include the backend URL
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
};

export default HomePage;
