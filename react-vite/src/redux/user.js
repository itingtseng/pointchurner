import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import csrfFetch from "../csrf"; // Adjust path if needed

// Thunks for fetching, updating, and deleting users
export const fetchSessionUser = createAsyncThunk(
  "user/fetchSessionUser",
  async () => {
    const response = await csrfFetch("/api/users/session");
    if (!response.ok) throw new Error("Failed to fetch session user");
    return await response.json();
  }
);

export const updateUser = createAsyncThunk(
  "user/updateUser",
  async (updatedData) => {
    const response = await csrfFetch("/api/users/session", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updatedData),
    });
    if (!response.ok) throw new Error("Failed to update user");
    return await response.json();
  }
);

export const deleteUser = createAsyncThunk(
  "user/deleteUser",
  async () => {
    const response = await csrfFetch("/api/users/me", { method: "DELETE" });
    if (!response.ok) throw new Error("Failed to delete user");
    return response.json();
  }
);

// Slice
const userSlice = createSlice({
  name: "user",
  initialState: { user: null, status: "idle", error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchSessionUser.fulfilled, (state, action) => {
        state.user = action.payload;
      })
      .addCase(updateUser.fulfilled, (state, action) => {
        state.user = action.payload.user;
      })
      .addCase(deleteUser.fulfilled, (state) => {
        state.user = null;
      })
      .addMatcher(
        (action) => action.type.endsWith("/rejected"),
        (state, action) => {
          state.error = action.error.message;
        }
      );
  },
});

export default userSlice.reducer;
