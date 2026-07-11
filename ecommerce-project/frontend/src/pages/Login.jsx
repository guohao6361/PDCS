import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, register } from '../api/user';
import { useAuth } from '../context/AuthContext';
import './Login.css';

export default function Login() {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login: authLogin } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      if (isRegister) {
        await register(username, password);
        alert('注册成功，请登录');
        setIsRegister(false);
      } else {
        const data = await login(username, password);
        authLogin(data.token, { id: data.userId, username: data.username, balance: data.balance });
        navigate('/');
      }
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="login-page">
      <div className="login-box">
        <h2>{isRegister ? '注册' : '登录'}</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="用户名"
            value={username}
            onChange={e => setUsername(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="密码"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
          {error && <p className="error">{error}</p>}
          <button type="submit" className="btn-submit">{isRegister ? '注册' : '登录'}</button>
        </form>
        <p className="toggle">
          {isRegister ? '已有账号？' : '没有账号？'}
          <button type="button" onClick={() => setIsRegister(!isRegister)}>
            {isRegister ? '去登录' : '去注册'}
          </button>
        </p>
      </div>
    </div>
  );
}
