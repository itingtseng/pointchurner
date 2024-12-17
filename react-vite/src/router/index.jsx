import { createBrowserRouter } from 'react-router-dom';
import LoginFormPage from '../components/LoginFormPage';
import SignupFormPage from '../components/SignupFormPage';
import Layout from './Layout';
import HomePage from '../components/Home/homepage';
import CardDetail from '../components/Card/CardDetail';
import Wallet from '../components/Wallet/Wallet';
import Spending from '../components/Spending/Spending'; 
import UserProfile from '../components/User/User';

export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <HomePage />,
      },
      {
        path: "login",
        element: <LoginFormPage />,
      },
      {
        path: "signup",
        element: <SignupFormPage />,
      },
      {
        path: "cards/:cardId",
        element: <CardDetail />,
      },
      {
        path: "wallets/:walletId",
        element: <Wallet />,
      },
      {
        path: "/wallet/edit/:cardId",
        element: <Wallet />,
      },
      {
        path: "spendings/:spendingId",
        element: <Spending />,
      },
      {
        path: "/profile",
        element: <UserProfile />,
      },      
    ],
  },
]);