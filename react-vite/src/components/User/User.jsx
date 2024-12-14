import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import EditProfileForm from "./EditProfileForm";

const UserProfile = () => {
  const [user, setUser] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      const response = await fetch("/api/users/session");
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      }
    };
    fetchUser();
  }, []);

  const handleEditToggle = () => {
    setIsEditing((prev) => !prev);
  };

  const handleProfileUpdate = async (updatedData) => {
    const response = await fetch("/api/users/session", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updatedData),
    });
    if (response.ok) {
      const data = await response.json();
      setUser(data.user);
      setIsEditing(false);
    }
  };

  const handleDelete = async () => {
    const confirmed = window.confirm("Are you sure you want to delete your account?");
    if (confirmed) {
      const response = await fetch("/api/users/me", { method: "DELETE" });
      if (response.ok) {
        navigate("/some-path");
      }
    }
  };

  if (!user) return <p>Loading...</p>;

  return (
    <div className="user-profile">
      <h1>{user.username}'s Profile</h1>
      {isEditing ? (
        <EditProfileForm user={user} onSave={handleProfileUpdate} onCancel={handleEditToggle} />
      ) : (
        <div>
          <p>Email: {user.email}</p>
          <p>First Name: {user.firstname}</p>
          <p>Last Name: {user.lastname}</p>
          <button onClick={handleEditToggle}>Edit Profile</button>
          <button onClick={handleDelete} className="delete-btn">Delete Account</button>
        </div>
      )}
    </div>
  );
};

export default UserProfile;
