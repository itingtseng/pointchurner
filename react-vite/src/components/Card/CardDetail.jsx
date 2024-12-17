import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./carddetail.css";

const CardDetail = () => {
  const { cardId } = useParams(); // Get card ID from the URL
  const [card, setCard] = useState(null);
  const navigate = useNavigate(); // Hook for navigation

  useEffect(() => {
    const fetchCardDetails = async () => {
      try {
        const response = await fetch(`/api/cards/${cardId}`); // Fetch card details
        if (response.ok) {
          const data = await response.json();
          setCard(data);
        } else {
          console.error("Failed to fetch card details");
        }
      } catch (err) {
        console.error("Error:", err);
      }
    };

    fetchCardDetails();
  }, [cardId]);

  if (!card) {
    return <div>Loading...</div>;
  }

  return (
    <div className="card-detail">
      <button onClick={() => navigate(-1)} className="back-button">Back</button>
      <h1>{card.name}</h1>
      <img
        src={`http://localhost:8000${card.image_url}`}
        alt={card.name}
        className="card-image"
      />
      <p>
        <strong>Issuer:</strong> {card.issuer}
      </p>
      <p>
        <strong>URL:</strong>{" "}
        <a href={card.url} target="_blank" rel="noopener noreferrer">
          {card.url}
        </a>
      </p>
      <p>
        <strong>Business Card:</strong> {card.is_business ? "Yes" : "No"}
      </p>
      <h2>Reward Points</h2>
      <ul>
        {card.reward_points.map((reward, index) => (
          <li key={index}>
            <strong>Category:</strong> {reward.category_name}
            <br />
            {reward.bonus_point} {reward.multiplier_type}
            <br />
            {reward.notes && (
              <>
                <strong>Notes:</strong> {reward.notes}
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CardDetail;
