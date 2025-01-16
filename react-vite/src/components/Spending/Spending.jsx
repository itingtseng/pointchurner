import React, { useEffect, useState, useMemo, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import {
  thunkGetUserSpending,
  thunkAddCategoryToSpending,
  thunkEditCategoryNotes,
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
  const [newCategoryNotes, setNewCategoryNotes] = useState(""); // For adding new categories
  const [categories, setCategories] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [categoryToRemove, setCategoryToRemove] = useState(null);
  const [editNotes, setEditNotes] = useState({}); // State for notes per category
  const [editMode, setEditMode] = useState(null); // Tracks the category ID being edited
  const [categoryError, setCategoryError] = useState(""); // Custom error state for dropdown

  useEffect(() => {
    let isMounted = true;
    const fetchData = async () => {
      try {
        await dispatch(thunkGetUserSpending());
        const res = await fetch("/api/spendings/categories/form");
        if (!res.ok) throw new Error("Failed to fetch categories.");
        const data = await res.json();
  
        if (isMounted) {
          const sortedCategories = (data.choices || []).sort((a, b) =>
            a[1].localeCompare(b[1])
          );
          setCategories(sortedCategories);
        }
      } catch (err) {
        if (isMounted) setError("An error occurred while fetching data.");
        console.error("Error fetching spending data:", err);
      }
    };
  
    fetchData();
  
    return () => {
      isMounted = false;
    };
  }, [dispatch]); // Dependencies are correctly limited   
  

  const validateCategory = useCallback(() => {
    if (!newCategoryId) {
      setCategoryError("Please select a category.");
      return false;
    }
    setCategoryError("");
    return true;
  }, [newCategoryId]);  

  const handleAddCategory = useCallback(async (e) => {
    e.preventDefault();
    if (!validateCategory()) return;
  
    try {
      await dispatch(
        thunkAddCategoryToSpending({
          category_id: parseInt(newCategoryId),
          notes: newCategoryNotes.trim(),
        })
      );
      setShowForm(false);
      setNewCategoryId("");
      setNewCategoryNotes("");
      setCategoryError("");
    } catch (err) {
      console.error("Error adding category to spending:", err);
      setError("An error occurred while adding the category.");
    }
  }, [dispatch, newCategoryId, newCategoryNotes, validateCategory]);   

  const handleEditNotes = async (categoryId) => {
    const notes = editNotes[categoryId]?.trim() || "";
    try {
      await dispatch(thunkEditCategoryNotes(categoryId, notes));
      setEditMode(null); // Exit edit mode
      setEditNotes((prev) => ({ ...prev, [categoryId]: "" })); // Reset notes input
      await dispatch(thunkGetUserSpending()); // Fetch the latest state
    } catch (err) {
      console.error("Error editing category notes:", err);
      setError("An error occurred while updating the notes.");
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

  const groupedCategories = useMemo(() => {
    if (!spending?.categories || !Array.isArray(spending.categories)) return {};
    
    const grouped = {};
    spending.categories.forEach((category) => {
      console.log("Processing Category:", category); // Log each category
  
      if (category.parent_categories_id === null) {
        grouped[category.category_id] = {
          name: category.name,
          notes: category.notes,
          children: [],
          id: category.category_id,
        };
      } else {
        if (!grouped[category.parent_categories_id]) {
          grouped[category.parent_categories_id] = {
            name: null,
            notes: null,
            children: [],
            id: category.parent_categories_id,
          };
        }
        console.log("Adding Child to Parent:", {
          parent: grouped[category.parent_categories_id],
          child: category,
        });
        grouped[category.parent_categories_id].children.push({
          name: category.name,
          notes: category.notes,
          id: category.category_id,
        });
      }
    });
    console.log("Final Grouped Categories After Processing:", grouped);
    return grouped;
  }, [spending?.categories]);   
         

  useEffect(() => {
    // Log Redux spending data when it changes
    console.log("Redux Spending Data:", spending);
  }, [spending]);
  
  useEffect(() => {
    // Log groupedCategories after it's processed
    console.log("Grouped Categories AFTER Processing:", groupedCategories);
  }, [groupedCategories]);
  
  useEffect(() => {
    // Log the final state only when spending.categories has valid data
    if (spending?.categories && spending.categories.length > 0) {
      console.log("Final Grouped Categories:", groupedCategories);
    }
  }, [groupedCategories, spending?.categories]);  


  const validCategories = useMemo(() => {
    if (!Array.isArray(categories) || !spending?.categories) return [];
    const existingCategoryIds = new Set(
      spending.categories.map((cat) => cat.category_id)
    );
    return categories.filter(([id]) => {
      const isParentOrChildExcluded = spending.categories.some(
        (cat) => cat.parent_categories_id === id || cat.category_id === id
      );
      return !existingCategoryIds.has(id) && !isParentOrChildExcluded;
    });
  }, [categories, spending?.categories]);

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

  return (
    <div className="spending-container">
      <h1>My Spending</h1>
      <div className="spending-details">
        <h3>Categories</h3>
        {Object.keys(groupedCategories).length > 0 ? (
          <ul className="category-list">
            {Object.values(groupedCategories).map((group, index) => {
              console.log("Rendering Group (Parent):", JSON.stringify(group, null, 2)); // Log each parent group
              return (
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
                      {editMode === group.id ? (
                        <form
                          onSubmit={(e) => {
                            e.preventDefault();
                            handleEditNotes(group.id);
                          }}
                        >
                          <input
                            type="text"
                            value={editNotes[group.id] || ""}
                            onChange={(e) =>
                              setEditNotes((prev) => ({
                                ...prev,
                                [group.id]: e.target.value,
                              }))
                            }
                            placeholder="Edit notes"
                            maxLength={255}
                          />
                          <button type="submit">Save</button>
                          <button
                            type="button"
                            onClick={() => {
                              setEditMode(null);
                              setEditNotes((prev) => ({
                                ...prev,
                                [group.id]: "",
                              }));
                            }}
                          >
                            Cancel
                          </button>
                        </form>
                      ) : (
                        <div>
                          <p>{group.notes ? group.notes : "No notes provided."}</p>
                          <button
                            onClick={() => {
                              setEditMode(group.id);
                              setEditNotes((prev) => ({
                                ...prev,
                                [group.id]: group.notes || "",
                              }));
                            }}
                            className="edit-button"
                          >
                            Edit Notes
                          </button>
                        </div>
                      )}
                    </div>
                  )}
                  {group.children.length > 0 && (
                    <ul>
                      {group.children.map((child, idx) => {
                        console.log(
                          "Rendering Child (Category):",
                          JSON.stringify(child, null, 2)
                        ); // Log each child category
                        return (
                          <li key={idx}>
                            <div>
                              {capitalizeFirstLetter(child.name)}
                              <button
                                onClick={() => confirmRemoveCategory(child.id)}
                                className="remove-button"
                              >
                                Remove
                              </button>
                              {editMode === child.id ? (
                                <form
                                  onSubmit={(e) => {
                                    e.preventDefault();
                                    handleEditNotes(child.id);
                                  }}
                                >
                                  <input
                                    type="text"
                                    value={editNotes[child.id] || ""}
                                    onChange={(e) =>
                                      setEditNotes((prev) => ({
                                        ...prev,
                                        [child.id]: e.target.value,
                                      }))
                                    }
                                    placeholder="Edit notes"
                                    maxLength={255}
                                  />
                                  <button type="submit">Save</button>
                                  <button
                                    type="button"
                                    onClick={() => {
                                      setEditMode(null);
                                      setEditNotes((prev) => ({
                                        ...prev,
                                        [child.id]: "",
                                      }));
                                    }}
                                  >
                                    Cancel
                                  </button>
                                </form>
                              ) : (
                                <div>
                                  <p>{child.notes ? child.notes : "No notes provided."}</p>
                                  <button
                                    onClick={() => {
                                      setEditMode(child.id);
                                      setEditNotes((prev) => ({
                                        ...prev,
                                        [child.id]: child.notes || "",
                                      }));
                                    }}
                                    className="edit-button"
                                  >
                                    Edit Notes
                                  </button>
                                </div>
                              )}
                            </div>
                          </li>
                        );
                      })}
                    </ul>
                  )}
                </li>
              );
            })}
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
            <label>
              Notes:
              <input
                type="text"
                value={newCategoryNotes}
                onChange={(e) => setNewCategoryNotes(e.target.value)}
                placeholder="Add notes"
                maxLength={255}
              />
            </label>
            <button type="submit">Add Category</button>
          </form>
        )}
  
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