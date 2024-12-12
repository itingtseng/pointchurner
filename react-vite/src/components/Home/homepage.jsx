import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./homepage.css";

const HomePage = () => {
  const [cards, setCards] = useState([]);

  // Fetch cards from the backend
  useEffect(() => {
    const fetchCards = async () => {
      try {
        const response = await fetch("/api/cards"); // Replace with your actual API endpoint
        if (response.ok) {
          const data = await response.json();
          setCards(data.cards); // Assuming your backend returns an object with `cards` array
        } else {
          console.error("Failed to fetch cards");
        }
      } catch (err) {
        console.error("Error:", err);
      }
    };

    fetchCards();
  }, []);

  return (
    <div className="container">
      <h1>All Cards</h1>
      <div className="grid">
        {cards.map((card) => (
          <Link to={`/cards/${card.id}`} key={card.id} className="card">
            <img
              src={`http://localhost:8000${card.image_url}`} // Include the backend URL
              alt={card.name}
              className="image"
              loading="lazy"
            />
            <p className="cardName">{card.name}</p>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default HomePage;
