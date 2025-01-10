import { useState } from "react";
import { thunkLogin } from "../../redux/session";
import { useDispatch } from "react-redux";
import { useModal } from "../../context/Modal";
import "../../context/Modal.css";
import { useNavigate } from "react-router-dom";

function LoginFormModal() {
  const dispatch = useDispatch();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});
  const { closeModal } = useModal();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const newErrors = {};
    if (!email.trim()) newErrors.email = "Email is required.";
    if (!password.trim()) newErrors.password = "Password is required.";

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    const serverResponse = await dispatch(
      thunkLogin({
        email,
        password,
      })
    );

    if (serverResponse) {
      setErrors(serverResponse);
    } else {
      closeModal();
    }
  };

  const demoUserLogin = async (e) => {
      e.preventDefault();
  
      setErrors({});
  
      const serverResponse = await dispatch(
        thunkLogin({
          email: "demo@aa.io",
          password: "password",
        })
      );
  
      if (serverResponse) {
        setErrors({
          general: "Login failed. Please check your credentials and try again.",
        });
      } else {
        closeModal();
        navigate("/");
      }
    };

  return (
    <>
      <h1>Log In</h1>
      <form onSubmit={handleSubmit} noValidate>
        <label>
          Email
          <input
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>
        {errors.email && <p className="error-message">{errors.email}</p>}
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        {errors.password && <p className="error-message">{errors.password}</p>}
        <button type="submit">Log In</button>
        <button type="button" onClick={demoUserLogin}>
            Demo Login
          </button>
      </form>
    </>
  );
}

export default LoginFormModal;
