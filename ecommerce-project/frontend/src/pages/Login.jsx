import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, register } from '../api/user';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../components/Toast';
import './Login.css';

export default function Login() {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('USER');
  const [payPassword, setPayPassword] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const { login: authLogin } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      if (isRegister) {
        if (role === 'USER' && (!/^\d{6}$/.test(payPassword))) {
          setError('支付密码必须为6位数字');
          return;
        }
        await register({ username, password, role, payPassword: role === 'USER' ? payPassword : undefined, phone, email });
        toast('注册成功，请登录', 'success');
        setIsRegister(false);
        setPayPassword('');
        setPhone('');
        setEmail('');
      } else {
        const data = await login(username, password);
        authLogin(data.token, {
          id: data.userId,
          username: data.username,
          balance: data.balance,
          role: data.role || 'USER'
        });
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
            placeholder="登录密码（6-20位）"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
            minLength={6}
            maxLength={20}
          />
          {isRegister && (
            <>
              <select value={role} onChange={e => setRole(e.target.value)}>
                <option value="USER">普通用户</option>
                <option value="MERCHANT">商家</option>
              </select>
              <input
                type="text"
                placeholder="手机号"
                value={phone}
                onChange={e => setPhone(e.target.value)}
              />
              <input
                type="email"
                placeholder="邮箱"
                value={email}
                onChange={e => setEmail(e.target.value)}
              />
              {role === 'USER' && (
                <input
                  type="text"
                  placeholder="支付密码（6位数字）"
                  value={payPassword}
                  onChange={e => setPayPassword(e.target.value)}
                  maxLength={6}
                  required
                />
              )}
            </>
          )}
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
