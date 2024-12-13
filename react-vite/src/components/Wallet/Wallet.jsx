import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import {
  thunkGetUserWallet,
  thunkAddCardToWallet,
  thunkUpdateWallet,
  thunkRemoveCardFromWallet,
} from "../../redux/wallet";
import "./Wallet.css";

const Wallet = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const wallet = useSelector((state) => state.wallet.singleWallet);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formMode, setFormMode] = useState("add");
  const [formCardId, setFormCardId] = useState(null);
  const [formData, setFormData] = useState({
    card_id: "",
    network: "",
    nickname: "",
  });
  const [nicknameError, setNicknameError] = useState("");
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [cardToRemove, setCardToRemove] = useState(null);

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

  const validateNickname = () => {
    if (!formData.nickname.trim()) {
      setNicknameError("Nickname cannot be empty");
      return false;
    }
    if (formData.nickname.length > 50) {
      setNicknameError("Nickname must be less than 50 characters");
      return false;
    }
    setNicknameError("");
    return true;
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    if (!validateNickname()) return;

    try {
      if (formMode === "add") {
        await dispatch(thunkAddCardToWallet(formData));
      } else if (formMode === "edit") {
        await dispatch(
          thunkUpdateWallet(formCardId, {
            nickname: formData.nickname,
            network: formData.network,
          })
        );
      }
      setFormData({ card_id: "", network: "", nickname: "" });
      setShowForm(false);
      setFormCardId(null);
      await dispatch(thunkGetUserWallet());
    } catch (err) {
      console.error("Error handling form submission:", err);
      setError("An error occurred while processing the form.");
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
    if (name === "nickname") validateNickname();
  };

  const handleAddClick = () => {
    setFormMode("add");
    setFormData({ card_id: "", network: "", nickname: "" });
    setShowForm(true);
  };

  const handleEditClick = (card) => {
    setFormMode("edit");
    setFormCardId(card.id);
    setFormData({ network: card.network, nickname: card.nickname });
    setShowForm(true);
  };

  const handleRemoveClick = (cardId) => {
    setCardToRemove(cardId);
    setShowConfirmModal(true);
  };

  const confirmRemoveCard = async () => {
    try {
      await dispatch(thunkRemoveCardFromWallet(cardToRemove));
      setCardToRemove(null);
      setShowConfirmModal(false);
      await dispatch(thunkGetUserWallet());
    } catch (err) {
      console.error("Error removing card:", err);
      setError("An error occurred while removing the card.");
    }
  };

  if (error) {
    return (
      <div className="wallet-error">
        <h1>Error</h1>
        <p>{error}</p>
        <button onClick={() => navigate("/")}>Go Back to Home</button>
      </div>
    );
  }

  if (!wallet) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="wallet-container">
      <h1>My Wallet</h1>
      <button className="add-card-button" onClick={handleAddClick}>
        Add Card
      </button>

      {showForm && (
        <form className="add-card-form" onSubmit={handleFormSubmit} noValidate>
          {formMode === "add" && (
            <label>
              Card ID:
              <input
                type="text"
                name="card_id"
                value={formData.card_id}
                onChange={handleInputChange}
              />
            </label>
          )}
          <label>
            Network:
            <select
              name="network"
              value={formData.network}
              onChange={handleInputChange}
            >
              <option value="">Select a network</option>
              <option value="VISA">Visa</option>
              <option value="MASTERCARD">MasterCard</option>
              <option value="AMERICAN_EXPRESS">American Express</option>
              <option value="DISCOVER">Discover</option>
              <option value="OTHER">Other</option>
            </select>
          </label>
          <label>
            Nickname:
            <input
              type="text"
              name="nickname"
              value={formData.nickname}
              onChange={handleInputChange}
              className={nicknameError ? "error-input" : ""}
            />
          </label>
          {nicknameError && <p className="error-message">{nicknameError}</p>}
          <button type="submit">
            {formMode === "add" ? "Add Card" : "Save Changes"}
          </button>
          <button
            type="button"
            className="cancel-button"
            onClick={() => setShowForm(false)}
          >
            Cancel
          </button>
        </form>
      )}

      <div className="wallet-cards">
        {wallet.cards && wallet.cards.length > 0 ? (
          wallet.cards.map((card) => (
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
              <button
                className="edit-button"
                onClick={(e) => {
                  e.stopPropagation();
                  handleEditClick(card);
                }}
              >
                Edit
              </button>
              <button
                className="remove-button"
                onClick={(e) => {
                  e.stopPropagation();
                  handleRemoveClick(card.id);
                }}
              >
                Remove
              </button>
            </div>
          ))
        ) : (
          <p>Your wallet is empty. Start adding cards!</p>
        )}
      </div>

      {showConfirmModal && (
        <div className="confirmation-modal">
          <div className="modal-content">
            <p className="modal-title">
              Are you sure you want to remove this card?
            </p>
            <div className="modal-buttons">
              <button className="confirm" onClick={confirmRemoveCard}>
                Yes
              </button>
              <button
                className="cancel"
                onClick={() => setShowConfirmModal(false)}
              >
                No
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Wallet;
