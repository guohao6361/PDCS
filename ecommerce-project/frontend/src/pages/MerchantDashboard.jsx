import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../components/Toast';
import { getMerchantProducts, createProduct, updateProduct, deleteProduct, uploadProductImage } from '../api/product';
import { getMerchantOrders, updateOrderStatus } from '../api/order';
import { getProfile, updateProfile, uploadAvatar, changePassword, deleteSelf } from '../api/user';
import { getImageUrl } from '../utils/image';
import './MerchantDashboard.css';

const orderStatusMap = {
  UNPAID: '未支付', PAID: '已支付', SHIPPED: '已发货',
  IN_TRANSIT: '运输中', DELIVERED: '已送达', COMPLETED: '已完成', CANCELLED: '已取消'
};

const orderStatusColors = {
  UNPAID: '#faad14', PAID: '#1890ff', SHIPPED: '#722ed1',
  IN_TRANSIT: '#13c2c2', DELIVERED: '#52c41a', COMPLETED: '#389e0d', CANCELLED: '#999'
};

export default function MerchantDashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const { toast, confirm } = useToast();
  const [tab, setTab] = useState('products');
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [profile, setProfile] = useState(null);

  // 商品表单
  const [showProductForm, setShowProductForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [productForm, setProductForm] = useState({ name: '', price: '', stock: '', description: '', imageUrl: '' });

  // 密码
  const [pwdForm, setPwdForm] = useState({ oldPassword: '', newPassword: '' });
  // 资料
  const [editForm, setEditForm] = useState({ username: '', phone: '', email: '' });

  useEffect(() => {
    if (!user) return;
    loadProducts();
    loadOrders();
    loadProfile();
  }, [user]);

  const loadProducts = async () => {
    try { setProducts(await getMerchantProducts(user.id)); } catch (err) { console.error(err); }
  };

  const loadOrders = async () => {
    try { setOrders(await getMerchantOrders(user.id)); } catch (err) { console.error(err); }
  };

  const loadProfile = async () => {
    try {
      const p = await getProfile(user.id);
      setProfile(p);
      setEditForm({ username: p.username || '', phone: p.phone || '', email: p.email || '' });
    } catch (err) { console.error(err); }
  };

  // 商品管理
  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try {
      const res = await uploadProductImage(file);
      setProductForm({ ...productForm, imageUrl: res.imageUrl });
    } catch (err) { toast(err.message, 'error'); }
  };

  const handleSaveProduct = async () => {
    if (!productForm.name || !productForm.price) return toast('请填写商品名称和价格', 'error');
    try {
      const data = { ...productForm, price: Number(productForm.price), stock: Number(productForm.stock) || 0, merchantId: user.id };
      if (editingProduct) {
        await updateProduct(editingProduct.id, data);
      } else {
        await createProduct(data);
      }
      setShowProductForm(false);
      setEditingProduct(null);
      setProductForm({ name: '', price: '', stock: '', description: '', imageUrl: '' });
      loadProducts();
    } catch (err) { toast(err.message, 'error'); }
  };

  const handleEditProduct = (p) => {
    setProductForm({ name: p.name, price: p.price, stock: p.stock, description: p.description || '', imageUrl: p.imageUrl || '' });
    setEditingProduct(p);
    setShowProductForm(true);
  };

  const handleDeleteProduct = async (id) => {
    if (!await confirm('确定删除此商品？')) return;
    try { await deleteProduct(id); loadProducts(); toast('商品已删除', 'success'); } catch (err) { toast(err.message, 'error'); }
  };

  // 订单管理
  const handleShipOrder = async (orderId) => {
    try { await updateOrderStatus(orderId, 'SHIPPED'); toast('已发货', 'success'); loadOrders(); } catch (err) { toast(err.message, 'error'); }
  };

  const handleTransitOrder = async (orderId) => {
    try { await updateOrderStatus(orderId, 'IN_TRANSIT'); toast('已更新为运输中', 'success'); loadOrders(); } catch (err) { toast(err.message, 'error'); }
  };

  const handleDeliverOrder = async (orderId) => {
    try { await updateOrderStatus(orderId, 'DELIVERED'); toast('已确认送达', 'success'); loadOrders(); } catch (err) { toast(err.message, 'error'); }
  };

  // 个人信息
  const handleUpdateProfile = async () => {
    try { await updateProfile(user.id, editForm); toast('修改成功', 'success'); loadProfile(); } catch (err) { toast(err.message, 'error'); }
  };

  const handleAvatarUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try { const res = await uploadAvatar(user.id, file); setProfile({ ...profile, avatar: res.avatarUrl }); toast('头像上传成功', 'success'); } catch (err) { toast(err.message, 'error'); }
  };

  const handleChangePassword = async () => {
    if (!pwdForm.oldPassword || !pwdForm.newPassword) return toast('请填写完整', 'error');
    try { await changePassword(user.id, pwdForm); toast('登录密码修改成功，请重新登录', 'success'); logout(); navigate('/login'); } catch (err) { toast(err.message, 'error'); }
  };

  const handleDeleteSelf = async () => {
    if (!await confirm('确定注销账户？此操作不可恢复！')) return;
    try { await deleteSelf(user.id); logout(); navigate('/login'); } catch (err) { toast(err.message, 'error'); }
  };

  if (!user || user.role !== 'MERCHANT') return <p className="loading">无权限访问</p>;

  return (
    <div className="dashboard-page merchant-dashboard">
      <h1>商家后台</h1>
      <div className="dashboard-tabs">
        <button className={tab === 'products' ? 'active' : ''} onClick={() => setTab('products')}>商品管理</button>
        <button className={tab === 'orders' ? 'active' : ''} onClick={() => setTab('orders')}>订单管理</button>
        <button className={tab === 'profile' ? 'active' : ''} onClick={() => setTab('profile')}>个人信息</button>
      </div>

      {tab === 'products' && (
        <div className="dashboard-content">
          <button className="btn-primary" onClick={() => { setShowProductForm(true); setEditingProduct(null); setProductForm({ name: '', price: '', stock: '', description: '', imageUrl: '' }); }}>+ 发布商品</button>
          {showProductForm && (
            <div className="product-form">
              <h3>{editingProduct ? '编辑商品' : '发布新商品'}</h3>
              <input placeholder="商品名称 *" value={productForm.name} onChange={e => setProductForm({ ...productForm, name: e.target.value })} />
              <input placeholder="价格 *" type="number" step="0.01" value={productForm.price} onChange={e => setProductForm({ ...productForm, price: e.target.value })} />
              <input placeholder="库存" type="number" value={productForm.stock} onChange={e => setProductForm({ ...productForm, stock: e.target.value })} />
              <textarea placeholder="商品描述" value={productForm.description} onChange={e => setProductForm({ ...productForm, description: e.target.value })} />
              <div className="image-upload">
                <label className="btn-upload">
                  上传商品图片
                  <input type="file" accept="image/*" onChange={handleImageUpload} hidden />
                </label>
                {(productForm.imageData || productForm.imageUrl) && <img src={productForm.imageData || getImageUrl(productForm.imageUrl)} alt="预览" className="preview-img" />}
              </div>
              <div className="form-actions">
                <button onClick={handleSaveProduct}>{editingProduct ? '保存修改' : '发布'}</button>
                <button onClick={() => setShowProductForm(false)}>取消</button>
              </div>
            </div>
          )}
          <div className="product-list-dashboard">
            {products.map(p => (
              <div key={p.id} className="product-row">
                {(p.imageData || p.imageUrl) && <img src={p.imageData || getImageUrl(p.imageUrl)} alt="" className="product-thumb" />}
                <div className="product-row-info">
                  <strong>{p.name}</strong>
                  <span>¥{p.price} | 库存: {p.stock}</span>
                </div>
                <div className="product-row-actions">
                  <button onClick={() => handleEditProduct(p)}>编辑</button>
                  <button className="btn-danger" onClick={() => handleDeleteProduct(p.id)}>删除</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {tab === 'orders' && (
        <div className="dashboard-content">
          <div className="order-list-dashboard">
            {orders.length === 0 ? <p>暂无订单</p> : orders.map(o => (
              <div key={o.id} className="order-row">
                <div className="order-row-header">
                  <span>#{o.id}</span>
                  <span style={{ color: orderStatusColors[o.status] }}>{orderStatusMap[o.status]}</span>
                  <span>¥{o.totalPrice}</span>
                  <span>{new Date(o.createdAt).toLocaleString()}</span>
                </div>
                <div className="order-row-items">
                  {o.items?.map((item, idx) => (
                    <span key={idx}>{item.productName} x{item.quantity}</span>
                  ))}
                </div>
                <div className="order-row-actions">
                  {o.status === 'PAID' && <button onClick={() => handleShipOrder(o.id)}>发货</button>}
                  {o.status === 'SHIPPED' && <button onClick={() => handleTransitOrder(o.id)}>更新为运输中</button>}
                  {o.status === 'IN_TRANSIT' && <button onClick={() => handleDeliverOrder(o.id)}>确认送达</button>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {tab === 'profile' && profile && (
        <div className="dashboard-content">
          <div className="profile-edit-section">
            <div className="avatar-area">
              {profile.avatar ? <img src={getImageUrl(profile.avatar)} alt="" className="avatar-img" /> : <div className="avatar-placeholder">{profile.username?.charAt(0)}</div>}
              <label className="btn-upload">
                更换头像
                <input type="file" accept="image/*" onChange={handleAvatarUpload} hidden />
              </label>
            </div>
            <div className="form-group"><label>用户名</label><input value={editForm.username} onChange={e => setEditForm({ ...editForm, username: e.target.value })} /></div>
            <div className="form-group"><label>手机号</label><input value={editForm.phone} onChange={e => setEditForm({ ...editForm, phone: e.target.value })} /></div>
            <div className="form-group"><label>邮箱</label><input value={editForm.email} onChange={e => setEditForm({ ...editForm, email: e.target.value })} /></div>
            <button className="btn-save" onClick={handleUpdateProfile}>保存修改</button>
          </div>
          <div className="password-section">
            <h3>修改密码</h3>
            <div className="form-group"><label>旧密码</label><input type="password" value={pwdForm.oldPassword} onChange={e => setPwdForm({ ...pwdForm, oldPassword: e.target.value })} /></div>
            <div className="form-group"><label>新密码</label><input type="password" value={pwdForm.newPassword} onChange={e => setPwdForm({ ...pwdForm, newPassword: e.target.value })} /></div>
            <button className="btn-save" onClick={handleChangePassword}>修改密码</button>
          </div>
          <div className="balance-info-dashboard">
            <span>账户余额</span>
            <strong>¥{profile.balance ?? user.balance}</strong>
          </div>
          <div className="profile-danger">
            <button className="btn-delete-account" onClick={handleDeleteSelf}>注销账户</button>
          </div>
        </div>
      )}
    </div>
  );
}
