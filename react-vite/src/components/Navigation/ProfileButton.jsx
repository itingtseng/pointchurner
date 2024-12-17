import { useState, useEffect, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { FaUserCircle } from "react-icons/fa";
import { thunkLogout } from "../../redux/session";
import { useNavigate, Link } from "react-router-dom";

function ProfileButton() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [showMenu, setShowMenu] = useState(false);
  const user = useSelector((store) => store.session.user);
  const ulRef = useRef();

  const toggleMenu = (e) => {
    e.stopPropagation(); // Prevent bubbling to document
    setShowMenu(!showMenu);
  };

  useEffect(() => {
    if (!showMenu) return;

    const closeMenu = (e) => {
      if (ulRef.current && !ulRef.current.contains(e.target)) {
        setShowMenu(false);
      }
    };

    document.addEventListener("click", closeMenu);

    return () => document.removeEventListener("click", closeMenu);
  }, [showMenu]);

  const closeMenu = () => setShowMenu(false);

  const logout = (e) => {
    e.preventDefault();
    dispatch(thunkLogout(navigate)); // Pass navigate to thunkLogout
    closeMenu();
  };

  return (
    <>
      {user && (
        <>
          <button onClick={toggleMenu} className="profile-icon-button">
            <FaUserCircle className="profile-icon" />
          </button>
          {showMenu && (
            <ul className="profile-dropdown" ref={ulRef}>
              <li>
                <Link to="/profile" onClick={closeMenu}>
                  {user.username}
                </Link>
              </li>
              <li>
                <Link to="/profile" onClick={closeMenu}>
                  {user.email}
                </Link>
              </li>
              <li>
                <button onClick={logout}>Log Out</button>
              </li>
            </ul>
          )}
        </>
      )}
    </>
  );
}

export default ProfileButton;
