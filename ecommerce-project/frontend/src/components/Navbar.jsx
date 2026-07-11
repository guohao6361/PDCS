import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getImageUrl } from '../utils/image';
import './Navbar.css';

const roleLabels = { USER: '用户', MERCHANT: '商家', ADMIN: '管理员' };

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
        {user && user.role === 'USER' && <Link to="/cart">购物车</Link>}
        {user && user.role === 'USER' && <Link to="/orders">我的订单</Link>}
        {user && <Link to="/profile">我的信息</Link>}
        {user?.role === 'MERCHANT' && <Link to="/merchant">商家后台</Link>}
        {user?.role === 'ADMIN' && <Link to="/admin">管理后台</Link>}
      </div>
      <div className="nav-user">
        {user ? (
          <>
            <span className="username">
              {user.avatar && <img src={getImageUrl(user.avatar)} alt="" className="nav-avatar" />}
              {user.username}
              <span className="role-tag">{roleLabels[user.role] || '用户'}</span>
              {user.balance !== undefined && <span className="balance"> (¥{user.balance})</span>}
            </span>
            <button onClick={handleLogout} className="btn-logout">退出</button>
          </>
        ) : (
          <Link to="/login" className="btn-login">登录</Link>
        )}
      </div>
    </nav>
  );
}
