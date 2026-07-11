import { useAuth } from '../context/AuthContext';
import './Profile.css';

export default function Profile() {
  const { user } = useAuth();

  if (!user) return <p className="loading">请先登录</p>;

  return (
    <div className="profile-page">
      <h1>我的信息</h1>
      <div className="profile-card">
        <div className="profile-avatar">{user.username?.charAt(0)?.toUpperCase()}</div>
        <div className="profile-info">
          <div className="profile-field">
            <span className="field-label">用户名</span>
            <span className="field-value">{user.username}</span>
          </div>
          <div className="profile-field">
            <span className="field-label">用户ID</span>
            <span className="field-value">{user.id}</span>
          </div>
          <div className="profile-field">
            <span className="field-label">账户余额</span>
            <span className="field-value balance">¥{user.balance}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
