import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import {
  thunkGetUserSpending,
  thunkAddCategoryToSpending,
  thunkRemoveCategoryFromSpending,
} from "../../redux/spending";
import "./Spending.css";

const capitalizeFirstLetter = (string) => {
    if (!string) return ""; // Return an empty string if undefined or null
    return string.charAt(0).toUpperCase() + string.slice(1);
  };
  

const Spending = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const spending = useSelector((state) => state.spending.singleSpending);

  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [newCategoryId, setNewCategoryId] = useState("");
  const [categories, setCategories] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [categoryToRemove, setCategoryToRemove] = useState(null);
  const [categoryError, setCategoryError] = useState(""); // Custom error state for dropdown

  useEffect(() => {
    const fetchData = async () => {
      try {
        await dispatch(thunkGetUserSpending());
        const res = await fetch("/api/spendings/categories/form");
        if (!res.ok) throw new Error("Failed to fetch categories.");
        const data = await res.json();
        const sortedCategories = (data.choices || []).sort((a, b) =>
          a[1].localeCompare(b[1])
        );
        setCategories(sortedCategories);
      } catch (err) {
        console.error("Error initializing spending page:", err);
        setError("An error occurred while fetching data.");
      }
    };

    fetchData();
  }, [dispatch]);

  const validateCategory = () => {
    if (!newCategoryId) {
      setCategoryError("Please select a category.");
      return false;
    }
    setCategoryError("");
    return true;
  };

  const handleAddCategory = async (e) => {
    e.preventDefault();
    if (!validateCategory()) return;

    try {
      await dispatch(
        thunkAddCategoryToSpending({ category_id: parseInt(newCategoryId) })
      );
      setShowForm(false);
      setNewCategoryId("");
    } catch (err) {
      console.error("Error adding category to spending:", err);
      setError("An error occurred while adding the category.");
    }
  };

  const confirmRemoveCategory = (categoryId) => {
    setCategoryToRemove(categoryId);
    setShowModal(true);
  };

  const handleRemoveCategory = async () => {
    if (categoryToRemove) {
      try {
        await dispatch(thunkRemoveCategoryFromSpending(categoryToRemove));
        setShowModal(false);
        setCategoryToRemove(null);
      } catch (err) {
        console.error("Error removing category from spending:", err);
        setError("An error occurred while removing the category.");
      }
    }
  };

  const groupCategories = (categories) => {
    const grouped = {};

    categories.forEach((category) => {
      if (category.parent_categories_id === null) {
        grouped[category.category_id] = {
          name: category.name,
          children: [],
          id: category.category_id,
        };
      } else {
        if (!grouped[category.parent_categories_id]) {
          grouped[category.parent_categories_id] = {
            name: null,
            children: [],
            id: category.parent_categories_id,
          };
        }
        grouped[category.parent_categories_id].children.push({
          name: category.name,
          id: category.category_id,
        });
      }
    });

    return grouped;
  };

  const filterValidCategories = () => {
    if (!Array.isArray(categories)) return [];
    if (!spending?.categories) return [];
    const existingCategoryIds = new Set(
      spending.categories.map((cat) => cat.category_id)
    );
    return categories.filter(([id]) => !existingCategoryIds.has(id));
  };

  if (error) {
    return (
      <div className="spending-error">
        <h1>Error</h1>
        <p>{error}</p>
        <button onClick={() => navigate("/")}>Go Back to Home</button>
      </div>
    );
  }

  if (!spending) {
    return <div className="loading">Loading...</div>;
  }

  const groupedCategories = groupCategories(spending.categories);
  const validCategories = filterValidCategories();

  return (
    <div className="spending-container">
      <h1>My Spending</h1>
      <div className="spending-details">
        <h3>Categories</h3>
        {Object.keys(groupedCategories).length > 0 ? (
          <ul className="category-list">
            {Object.values(groupedCategories).map((group, index) => (
              <li key={index}>
                {group.name && (
                  <div>
                    <strong>{capitalizeFirstLetter(group.name)}:</strong>
                    <button
                      onClick={() => confirmRemoveCategory(group.id)}
                      className="remove-button"
                    >
                      Remove
                    </button>
                  </div>
                )}
                {group.children.length > 0 && (
                  <ul>
                    {group.children.map((child, idx) => (
                      <li key={idx}>
                        {capitalizeFirstLetter(child.name)}
                        <button
                          onClick={() => confirmRemoveCategory(child.id)}
                          className="remove-button"
                        >
                          Remove
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
              </li>
            ))}
          </ul>
        ) : (
          <p>No categories available in spending.</p>
        )}

        <button
          className="add-category-button"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? "Cancel" : "Add Category"}
        </button>

        {showForm && (
          <form onSubmit={handleAddCategory} className="add-category-form">
            <label>
              Select Category:
              <select
                value={newCategoryId}
                onChange={(e) => setNewCategoryId(e.target.value)}
                className={categoryError ? "error-input" : ""}
              >
                <option value="">-- Select a category --</option>
                {validCategories.map(([id, name]) => (
                  <option key={id} value={id}>
                    {capitalizeFirstLetter(name)}
                  </option>
                ))}
              </select>
            </label>
            {categoryError && <p className="error-message">{categoryError}</p>}
            <button type="submit">Submit</button>
          </form>
        )}

        {/* Confirmation Modal */}
        {showModal && (
          <div className="confirmation-modal">
            <div className="modal-content">
              <p className="modal-title">
                Are you sure you want to remove this category?
              </p>
              <div className="modal-buttons">
                <button onClick={handleRemoveCategory} className="confirm">
                  Yes
                </button>
                <button onClick={() => setShowModal(false)} className="cancel">
                  No
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Spending;
