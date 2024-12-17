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

// Map issuers to their respective networks
const issuerNetworkMap = {
  AMERICAN_EXPRESS: [["AMERICAN_EXPRESS", "American Express"]],
  BANK_OF_AMERICA: [
    ["VISA", "Visa"],
    ["MASTERCARD", "MasterCard"],
  ],
  BARCLAYS: [
    ["VISA", "Visa"],
    ["MASTERCARD", "MasterCard"],
  ],
  BREX: [["MASTERCARD", "MasterCard"]],
  CHASE: [
    ["VISA", "Visa"],
    ["MASTERCARD", "MasterCard"],
  ],
  CAPITAL_ONE: [
    ["VISA", "Visa"],
    ["MASTERCARD", "MasterCard"],
  ],
  CITI: [
    ["VISA", "Visa"],
    ["MASTERCARD", "MasterCard"],
  ],
  DISCOVER: [["DISCOVER", "Discover"]],
  FIRST: [
    ["VISA", "Visa"],
    ["MASTERCARD", "MasterCard"],
  ],
  FNBO: [
    ["VISA", "Visa"],
    ["MASTERCARD", "MasterCard"],
  ],
  PENFED: [
    ["VISA", "Visa"],
    ["MASTERCARD", "MasterCard"],
  ],
  PNC: [["VISA", "Visa"]],
  SYNCHRONY: [
    ["VISA", "Visa"],
    ["MASTERCARD", "MasterCard"],
    ["STORE_ONLY", "Store-only Private Network"],
  ],
  US_BANK: [
    ["VISA", "Visa"],
    ["MASTERCARD", "MasterCard"],
  ],
  WELLS_FARGO: [
    ["VISA", "Visa"],
    ["MASTERCARD", "MasterCard"],
  ],
};

const Wallet = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const wallet = useSelector((state) => state.wallet.singleWallet);
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [formMode, setFormMode] = useState("add");
  const [formCardId, setFormCardId] = useState(null);
  const [formData, setFormData] = useState({
    issuer: "",
    cardType: "",
    selectedCard: null,
    network: "",
    nickname: "",
  });
  const [cards, setCards] = useState([]);
  const [networks, setNetworks] = useState([]);
  const [loadingCards, setLoadingCards] = useState(false);
  const [formErrors, setFormErrors] = useState({});
  const [showCardImages, setShowCardImages] = useState(false);

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

  const fetchCards = async () => {
    if (!formData.issuer || !formData.cardType) return;
    setLoadingCards(true);
    try {
      const response = await fetch(
        `/api/cards?issuer=${formData.issuer}&card_type=${formData.cardType}`
      );
      if (response.ok) {
        const data = await response.json();
        setCards(data.cards);
      } else {
        setCards([]);
      }
    } catch (err) {
      console.error("Error fetching cards:", err);
      setCards([]);
    } finally {
      setLoadingCards(false);
    }
  };

  useEffect(() => {
    fetchCards();
  }, [formData.issuer, formData.cardType]);

  const validateField = (name, value) => {
    switch (name) {
      case "issuer":
        return !value ? "Please select an issuer." : "";
      case "cardType":
        return !value ? "Please select a card type." : "";
      case "selectedCard":
        return !value ? "Please select a card." : "";
      case "network":
        return !value ? "Please select a network." : "";
      case "nickname":
        if (value.length > 50)
          return "Nickname must be less than 50 characters.";
        return "";
      default:
        return "";
    }
  };

  const validateForm = () => {
    const errors = {
      issuer: validateField("issuer", formData.issuer),
      cardType: validateField("cardType", formData.cardType),
      selectedCard: validateField("selectedCard", formData.selectedCard),
      network: validateField("network", formData.network),
    };
    setFormErrors(errors);
    return Object.values(errors).every((error) => !error);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;

    // Reset network options if issuer is changed
    if (name === "issuer") {
      const newNetworks = issuerNetworkMap[value] || [];
      setNetworks(newNetworks); // Update available networks
      setFormData((prev) => ({
        ...prev,
        issuer: value,
        network: "", // Reset network when issuer changes
      }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleDropdownClick = () => {
    if (formData.selectedCard) {
      // Reset the selected card to show all images
      setFormData((prev) => ({
        ...prev,
        selectedCard: null,
      }));
    }
  };

  const handleCardSelection = (card) => {
    setFormData((prev) => ({
      ...prev,
      selectedCard: card,
    }));
    setShowCardImages(false); // Hide card images when a card is selected
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setIsSubmitting(true);
    try {
      if (formMode === "add") {
        const payload = {
          card_id: formData.selectedCard.id,
          network: formData.network,
          nickname: formData.nickname || null,
        };
        await dispatch(thunkAddCardToWallet(payload));
      } else if (formMode === "edit") {
        const payload = {
          nickname: formData.nickname || null,
          network: formData.network,
        };
        await dispatch(thunkUpdateWallet(formCardId, payload));
      }
      setShowForm(false);
      setFormData({
        issuer: "",
        cardType: "",
        selectedCard: null,
        network: "",
        nickname: "",
      });
      setCards([]);
      await dispatch(thunkGetUserWallet());
    } catch (err) {
      console.error("Error handling form submission:", err);
      setError("An error occurred while processing the form.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleAddClick = () => {
    setFormMode("add");
    setFormData({
      issuer: "",
      cardType: "",
      selectedCard: null,
      network: "",
      nickname: "",
    });
    setShowForm(true);
  };

  const handleEditClick = (card) => {
    setFormMode("edit");
    setFormCardId(card.id);
    setFormData({
      selectedCard: card,
      network: card.network,
      nickname: card.nickname,
    });
    setShowForm(true);
  };

  const handleRemoveClick = (cardId) => {
    dispatch(thunkRemoveCardFromWallet(cardId))
      .then(() => dispatch(thunkGetUserWallet()))
      .catch((err) => {
        console.error("Error removing card:", err);
        setError("An error occurred while removing the card.");
      });
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
        <form className="add-card-form" onSubmit={handleFormSubmit}>
          {formMode === "add" && (
            <>
              <label>
                Select Issuer:
                <select
                  name="issuer"
                  value={formData.issuer}
                  onChange={handleInputChange}
                >
                  <option value="">--Select an Issuer--</option>
                  {Object.keys(issuerNetworkMap).map((issuer) => (
                    <option key={issuer} value={issuer}>
                      {issuer.replace(/_/g, " ")}
                    </option>
                  ))}
                </select>
                {formErrors.issuer && (
                  <p className="error-message">{formErrors.issuer}</p>
                )}
              </label>
              <label>
                Network:
                <select
                  name="network"
                  value={formData.network}
                  onChange={handleInputChange}
                  disabled={!networks.length} // Disable if no networks available
                >
                  <option value="">--Select Network--</option>
                  {networks.map(([value, label]) => (
                    <option key={value} value={value}>
                      {label}
                    </option>
                  ))}
                </select>
                {formErrors.network && (
                  <p className="error-message">{formErrors.network}</p>
                )}
              </label>
              <label>
                Card Type:
                <select
                  name="cardType"
                  value={formData.cardType}
                  onChange={handleInputChange}
                >
                  <option value="">--Select Card Type--</option>
                  <option value="business">Business</option>
                  <option value="personal">Personal</option>
                </select>
                {formErrors.cardType && (
                  <p className="error-message">{formErrors.cardType}</p>
                )}
              </label>
              {loadingCards ? (
                <p>Loading cards...</p>
              ) : (
                cards.length > 0 && (
                  <>
                    {/* Dropdown for card selection */}
                    <label>
                      Select Card:
                      <select
                        name="selectedCard"
                        value={formData.selectedCard?.id || ""}
                        onChange={(e) => {
                          const selectedCard = cards.find(
                            (card) => card.id === parseInt(e.target.value)
                          );
                          handleCardSelection(selectedCard);
                        }}
                        onClick={() => handleDropdownClick()} // Reset selected card on dropdown click
                      >
                        <option value="">--Select a Card--</option>
                        {cards.map((card) => (
                          <option key={card.id} value={card.id}>
                            {card.name}
                          </option>
                        ))}
                      </select>
                    </label>

                    {/* Show selected card or all cards if none is selected */}
                    <div className="card-list">
                      {formData.selectedCard ? (
                        <div
                          className="card-item selected"
                          onClick={() => handleCardSelection(null)} // Deselect card to show all cards again
                        >
                          <img
                            src={`http://localhost:8000${formData.selectedCard.image_url}`}
                            alt={formData.selectedCard.name}
                            className="card-image"
                          />
                          <p>{formData.selectedCard.name}</p>
                        </div>
                      ) : (
                        cards.map((card) => (
                          <div
                            key={card.id}
                            className="card-item"
                            onClick={() => handleCardSelection(card)}
                          >
                            <img
                              src={`http://localhost:8000${card.image_url}`}
                              alt={card.name}
                              className="card-image"
                            />
                            <p>{card.name}</p>
                          </div>
                        ))
                      )}
                    </div>

                    {/* Error message for card selection */}
                    {formErrors.selectedCard && (
                      <p className="error-message">{formErrors.selectedCard}</p>
                    )}
                  </>
                )
              )}
            </>
          )}
          <label>
            Nickname:
            <input
              type="text"
              name="nickname"
              value={formData.nickname}
              onChange={handleInputChange}
            />
            {formErrors.nickname && (
              <p className="error-message">{formErrors.nickname}</p>
            )}
          </label>
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting
              ? "Submitting..."
              : formMode === "add"
              ? "Add Card"
              : "Save Changes"}
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
    </div>
  );
};

export default Wallet;
