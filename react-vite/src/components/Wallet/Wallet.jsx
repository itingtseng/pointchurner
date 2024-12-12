import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { thunkGetUserWallet } from "../../redux/wallet";
import "./Wallet.css";

const Wallet = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  // Redux state and error handling
  const wallet = useSelector((state) => state.wallet.singleWallet);
  const [error, setError] = useState(null);

  // Fetch wallet data on component mount
  useEffect(() => {
    const fetchWallet = async () => {
      try {
        await dispatch(thunkGetUserWallet());
      } catch (err) {
        console.error("Error fetching wallet:", err);
        setError("An error occurred while fetching the wallet.");
      }
    };

    fetchWallet();
  }, [dispatch]);

  // Render error message if there's an issue
  if (error) {
    return (
      <div className="wallet-error">
        <h1>Error</h1>
        <p>{error}</p>
        <button onClick={() => navigate("/")}>Go Back to Home</button>
      </div>
    );
  }

  // Show loading indicator while data is being fetched
  if (!wallet) {
    return <div className="loading">Loading...</div>;
  }

  // Handle the case where the wallet has no cards
  if (!wallet.cards || wallet.cards.length === 0) {
    return (
      <div className="wallet-empty">
        <h1>My Wallet</h1>
        <p>Your wallet is empty. Start adding cards!</p>
        <button onClick={() => navigate("/add-card")}>Add Card</button>
      </div>
    );
  }

  // Render the wallet with its cards
  return (
    <div className="wallet-container">
      <h1>My Wallet</h1>
      <div className="wallet-cards">
        {wallet.cards.map((card) => (
          <div
            key={card.id}
            className="wallet-card"
            onClick={() => navigate(`/cards/${card.id}`)}
          >
            <img
              src={`http://localhost:8000${card.image_url}`}
              alt={card.name}
              className="card-image"
            />
            <h3>{card.name}</h3>
            <p>
              <strong>Nickname:</strong> {card.nickname}
            </p>
            <p>
              <strong>Network:</strong> {card.network}
            </p>
            <p>
              <strong>Issuer:</strong> {card.issuer}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Wallet;
