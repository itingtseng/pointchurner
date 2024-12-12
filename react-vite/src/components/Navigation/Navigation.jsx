import { NavLink } from "react-router-dom";
import { useSelector } from "react-redux";
import ProfileButton from "./ProfileButton";
import OpenModalMenuItem from "./OpenModalMenuItem";
import LoginFormModal from "../LoginFormModal";
import SignupFormModal from "../SignupFormModal";
import logo from "../../../src/logo.png";
import "./Navigation.css";

function Navigation() {
  const user = useSelector((store) => {
    console.log("Redux state session.user:", store.session.user); // Debug log
    return store.session.user;
  });
  const walletPath = user?.wallet_id ? `/wallets/${user.wallet_id}` : "/";
  console.log("Navigating to:", walletPath);
  

  return (
    <nav className="navigation">
      <div className="nav-left">
        <NavLink to="/">
          <img src={logo} alt="Logo" className="logo" />
        </NavLink>
      </div>
      <div className="nav-right">
        <ul>
          {user ? (
            <>
              <li>
                <NavLink
                  to={walletPath}
                  className="wallet-link"
                  onClick={() => console.log("Navigating to:", walletPath)}
                >
                  My Wallet
                </NavLink>
              </li>
              <li>
                <ProfileButton />
              </li>
            </>
          ) : (
            <>
              <li>
                <OpenModalMenuItem
                  itemText="Log In"
                  modalComponent={<LoginFormModal />}
                />
              </li>
              <li>
                <OpenModalMenuItem
                  itemText="Sign Up"
                  modalComponent={<SignupFormModal />}
                />
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
}

export default Navigation;
