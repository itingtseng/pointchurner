import { NavLink } from "react-router-dom";
import { useSelector } from "react-redux";
import ProfileButton from "./ProfileButton";
import OpenModalMenuItem from "./OpenModalMenuItem";
import LoginFormModal from "../LoginFormModal";
import SignupFormModal from "../SignupFormModal";
import logo from "../../logo.png";
import "./Navigation.css";

function Navigation() {
  const user = useSelector((store) => store.session.user);

  const walletPath = user?.wallet_id ? `/wallets/${user.wallet_id}` : "/";
  const spendingPath = user?.spending_id ? `/spendings/${user.spending_id}` : "/";

  return (
    <nav className="navigation">
      <div className="nav-left">
        <NavLink to="/">
          <img src={logo} alt="Logo" className="logo" />
        </NavLink>
        <h3>Point Churner</h3>
      </div>
      <div className="nav-right">
        <ul>
          {user ? (
            <>
              <li>
                <NavLink to={walletPath} className="wallet-link">
                  My Wallet
                </NavLink>
              </li>
              <li>
                <NavLink to={spendingPath} className="spending-link">
                  My Spending
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
