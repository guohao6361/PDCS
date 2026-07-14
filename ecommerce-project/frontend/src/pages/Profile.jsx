import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../components/Toast';
import {
  getProfile, updateProfile, uploadAvatar, changePassword, changePayPassword,
  getAddresses, createAddress, updateAddress, deleteAddress, setDefaultAddress,
  deleteSelf
} from '../api/user';
import { getImageUrl } from '../utils/image';
import './Profile.css';

export default function Profile() {
  const { user, updateUser, logout, refreshUser } = useAuth();
  const navigate = useNavigate();
  const { toast, confirm } = useToast();
  const [profile, setProfile] = useState(null);
  const [addresses, setAddresses] = useState([]);
  const [activeTab, setActiveTab] = useState('info');

  // 资料编辑
  const [editForm, setEditForm] = useState({ username: '', phone: '', email: '' });
  // 密码
  const [pwdForm, setPwdForm] = useState({ oldPassword: '', newPassword: '' });
  const [payPwdForm, setPayPwdForm] = useState({ oldPayPassword: '', newPayPassword: '' });
  // 新地址
  const [addrForm, setAddrForm] = useState({ receiverName: '', phone: '', province: '', city: '', district: '', detailAddress: '', isDefault: false });
  const [editingAddrId, setEditingAddrId] = useState(null);

  useEffect(() => {
    if (!user) return;
    const load = async () => {
      try {
        const [p, a] = await Promise.all([getProfile(user.id), getAddresses(user.id)]);
        setProfile(p);
        setAddresses(a || []);
        setEditForm({ username: p.username || '', phone: p.phone || '', email: p.email || '' });
      } catch (err) {
        console.error(err);
      }
    };
    load();
  }, [user]);

  if (!user) return <p className="loading">请先登录</p>;
  if (!profile) return <p className="loading">加载中...</p>;

  // 资料修改
  const handleUpdateProfile = async () => {
    try {
      const updated = await updateProfile(user.id, editForm);
      setProfile(updated);
      updateUser({ ...user, ...updated });
      toast('资料修改成功', 'success');
    } catch (err) {
      toast(err.message, 'error');
    }
  };

  // 头像上传
  const handleAvatarUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    if (file.size > 2 * 1024 * 1024) return toast('图片大小不能超过2MB', 'error');
    try {
      const res = await uploadAvatar(user.id, file);
      setProfile({ ...profile, avatar: res.avatarUrl });
      updateUser({ ...user, avatar: res.avatarUrl });
      toast('头像上传成功', 'success');
    } catch (err) {
      toast(err.message, 'error');
    }
  };

  // 修改登录密码
  const handleChangePassword = async () => {
    if (!pwdForm.oldPassword || !pwdForm.newPassword) return toast('请填写完整', 'error');
    if (pwdForm.newPassword.length < 6 || pwdForm.newPassword.length > 20) return toast('密码长度6-20位', 'error');
    try {
      await changePassword(user.id, pwdForm);
      toast('登录密码修改成功，请重新登录', 'success');
      logout();
      navigate('/login');
    } catch (err) {
      toast(err.message, 'error');
    }
  };

  // 修改支付密码
  const handleChangePayPassword = async () => {
    if (!payPwdForm.oldPayPassword || !payPwdForm.newPayPassword) return toast('请填写完整', 'error');
    if (!/^\d{6}$/.test(payPwdForm.newPayPassword)) return toast('支付密码必须为6位数字', 'error');
    try {
      await changePayPassword(user.id, payPwdForm);
      toast('支付密码修改成功', 'success');
      setPayPwdForm({ oldPayPassword: '', newPayPassword: '' });
    } catch (err) {
      toast(err.message, 'error');
    }
  };

  // 地址管理
  const loadAddresses = async () => {
    try {
      const a = await getAddresses(user.id);
      setAddresses(a || []);
    } catch (err) {
      console.error('加载地址失败:', err);
    }
  };

  const handleSaveAddress = async () => {
    if (!addrForm.receiverName || !addrForm.phone || !addrForm.detailAddress) {
      return toast('请填写完整地址信息', 'error');
    }
    try {
      if (editingAddrId) {
        await updateAddress(user.id, editingAddrId, addrForm);
        toast('地址修改成功', 'success');
      } else {
        if (addresses.length >= 10) return toast('最多保存10个地址', 'error');
        await createAddress(user.id, addrForm);
        toast('地址添加成功', 'success');
      }
      setEditingAddrId(null);
      setAddrForm({ receiverName: '', phone: '', province: '', city: '', district: '', detailAddress: '', isDefault: false });
      // 重新加载地址列表，确保默认地址状态正确
      await loadAddresses();
    } catch (err) {
      toast(err.message, 'error');
    }
  };

  const handleEditAddress = (addr) => {
    setAddrForm({ receiverName: addr.receiverName, phone: addr.phone, province: addr.province, city: addr.city, district: addr.district, detailAddress: addr.detailAddress, isDefault: addr.isDefault });
    setEditingAddrId(addr.id);
  };

  const handleDeleteAddress = async (addrId) => {
    if (!await confirm('确定删除此地址？')) return;
    try {
      await deleteAddress(user.id, addrId);
      toast('地址删除成功', 'success');
      // 重新加载地址列表
      await loadAddresses();
    } catch (err) {
      toast(err.message, 'error');
    }
  };

  const handleSetDefault = async (addrId) => {
    try {
      await setDefaultAddress(user.id, addrId);
      toast('默认地址设置成功', 'success');
      // 重新加载地址列表，确保默认地址状态正确
      await loadAddresses();
    } catch (err) {
      toast(err.message, 'error');
    }
  };

  // 注销账户
  const handleDeleteSelf = async () => {
    if (!await confirm('确定注销账户？此操作不可恢复！')) return;
    try {
      await deleteSelf(user.id);
      logout();
      navigate('/login');
    } catch (err) {
      toast(err.message, 'error');
    }
  };

  return (
    <div className="profile-page">
      <h1>我的信息</h1>
      <div className="profile-tabs">
        <button className={activeTab === 'info' ? 'active' : ''} onClick={() => setActiveTab('info')}>个人资料</button>
        <button className={activeTab === 'password' ? 'active' : ''} onClick={() => setActiveTab('password')}>密码管理</button>
        {user.role === 'USER' && <button className={activeTab === 'address' ? 'active' : ''} onClick={() => setActiveTab('address')}>收货地址</button>}
      </div>

      {activeTab === 'info' && (
        <div className="profile-section">
          <div className="profile-avatar-area">
            {profile.avatar ? (
              <img src={getImageUrl(profile.avatar)} alt="头像" className="profile-avatar-img" />
            ) : (
              <div className="profile-avatar">{profile.username?.charAt(0)?.toUpperCase()}</div>
            )}
            <label className="btn-upload-avatar">
              上传头像
              <input type="file" accept="image/*" onChange={handleAvatarUpload} hidden />
            </label>
          </div>
          <div className="profile-form">
            <div className="form-group">
              <label>用户名</label>
              <input value={editForm.username} onChange={e => setEditForm({ ...editForm, username: e.target.value })} />
            </div>
            <div className="form-group">
              <label>手机号</label>
              <input value={editForm.phone} onChange={e => setEditForm({ ...editForm, phone: e.target.value })} />
            </div>
            <div className="form-group">
              <label>邮箱</label>
              <input type="email" value={editForm.email} onChange={e => setEditForm({ ...editForm, email: e.target.value })} />
            </div>
            <div className="form-group">
              <label>角色</label>
              <span className="readonly">{profile.role || user.role}</span>
            </div>
            <div className="form-group">
              <label>余额</label>
              <span className="readonly">¥{profile.balance ?? user.balance}</span>
            </div>
            <button className="btn-save" onClick={handleUpdateProfile}>保存修改</button>
          </div>
          <div className="profile-danger">
            <button className="btn-delete-account" onClick={handleDeleteSelf}>注销账户</button>
          </div>
        </div>
      )}

      {activeTab === 'password' && (
        <div className="profile-section">
          <div className="password-section">
            <h3>修改登录密码</h3>
            <div className="form-group">
              <label>旧密码</label>
              <input type="password" value={pwdForm.oldPassword} onChange={e => setPwdForm({ ...pwdForm, oldPassword: e.target.value })} />
            </div>
            <div className="form-group">
              <label>新密码（6-20位）</label>
              <input type="password" value={pwdForm.newPassword} onChange={e => setPwdForm({ ...pwdForm, newPassword: e.target.value })} />
            </div>
            <button className="btn-save" onClick={handleChangePassword}>修改登录密码</button>
          </div>
          {user.role === 'USER' && (
            <div className="password-section">
              <h3>修改支付密码</h3>
              <div className="form-group">
                <label>旧支付密码</label>
                <input type="password" value={payPwdForm.oldPayPassword} onChange={e => setPayPwdForm({ ...payPwdForm, oldPayPassword: e.target.value })} />
              </div>
              <div className="form-group">
                <label>新支付密码（6位数字）</label>
                <input type="text" maxLength={6} value={payPwdForm.newPayPassword} onChange={e => setPayPwdForm({ ...payPwdForm, newPayPassword: e.target.value })} />
              </div>
              <button className="btn-save" onClick={handleChangePayPassword}>修改支付密码</button>
            </div>
          )}
        </div>
      )}

      {activeTab === 'address' && (
        <div className="profile-section">
          <h3>收货地址 ({addresses.length}/10)</h3>
          <div className="address-list-profile">
            {addresses.map(addr => (
              <div key={addr.id} className="address-card">
                <div className="address-card-info">
                  <strong>{addr.receiverName}</strong> {addr.phone}
                  <br />
                  {addr.province}{addr.city}{addr.district} {addr.detailAddress}
                  {addr.isDefault && <span className="default-tag">默认</span>}
                </div>
                <div className="address-card-actions">
                  {!addr.isDefault && <button onClick={() => handleSetDefault(addr.id)}>设为默认</button>}
                  <button onClick={() => handleEditAddress(addr)}>编辑</button>
                  <button className="btn-danger" onClick={() => handleDeleteAddress(addr.id)}>删除</button>
                </div>
              </div>
            ))}
          </div>
          {addresses.length < 10 && (
            <div className="address-form">
              <h4>{editingAddrId ? '编辑地址' : '新增地址'}</h4>
              <input placeholder="收件人姓名 *" value={addrForm.receiverName} onChange={e => setAddrForm({ ...addrForm, receiverName: e.target.value })} />
              <input placeholder="手机号 *" value={addrForm.phone} onChange={e => setAddrForm({ ...addrForm, phone: e.target.value })} />
              <input placeholder="省" value={addrForm.province} onChange={e => setAddrForm({ ...addrForm, province: e.target.value })} />
              <input placeholder="市" value={addrForm.city} onChange={e => setAddrForm({ ...addrForm, city: e.target.value })} />
              <input placeholder="区" value={addrForm.district} onChange={e => setAddrForm({ ...addrForm, district: e.target.value })} />
              <input placeholder="详细地址 *" value={addrForm.detailAddress} onChange={e => setAddrForm({ ...addrForm, detailAddress: e.target.value })} />
              <label className="checkbox-label">
                <input type="checkbox" checked={addrForm.isDefault} onChange={e => setAddrForm({ ...addrForm, isDefault: e.target.checked })} />
                设为默认地址
              </label>
              <div className="address-form-actions">
                <button onClick={handleSaveAddress}>{editingAddrId ? '保存修改' : '添加地址'}</button>
                {editingAddrId && <button onClick={() => { setEditingAddrId(null); setAddrForm({ receiverName: '', phone: '', province: '', city: '', district: '', detailAddress: '', isDefault: false }); }}>取消</button>}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
