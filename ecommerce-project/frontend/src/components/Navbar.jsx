import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <Link to="/" className="logo">🛒 电商商城</Link>
      <div className="nav-links">
        <Link to="/">首页</Link>
        {user && <Link to="/cart">购物车</Link>}
        {user && <Link to="/orders">我的订单</Link>}
        {user && <Link to="/profile">我的信息</Link>}
      </div>
      <div className="nav-user">
        {user ? (
          <>
            <span className="username">{user.username} (¥{user.balance})</span>
            <button onClick={handleLogout} className="btn-logout">退出</button>
          </>
        ) : (
          <Link to="/login" className="btn-login">登录</Link>
        )}
      </div>
    </nav>
  );
}
