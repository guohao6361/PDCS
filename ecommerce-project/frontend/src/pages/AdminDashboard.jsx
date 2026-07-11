import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../components/Toast';
import { getAllUsers, updateUser, updateUserRole, deleteUser } from '../api/user';
import { getProducts, updateProduct, deleteProduct } from '../api/product';
import { getAllOrders, updateOrder, updateOrderStatus, deleteOrder } from '../api/order';
import { getImageUrl } from '../utils/image';
import './AdminDashboard.css';

const orderStatusMap = {
  UNPAID: '未支付', PAID: '已支付', SHIPPED: '已发货',
  IN_TRANSIT: '运输中', DELIVERED: '已送达', COMPLETED: '已完成', CANCELLED: '已取消'
};

const roleLabels = { USER: '用户', MERCHANT: '商家', ADMIN: '管理员' };

export default function AdminDashboard() {
  const { user } = useAuth();
  const { toast, confirm } = useToast();
  const [tab, setTab] = useState('users');
  const [users, setUsers] = useState([]);
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);

  // 编辑用户
  const [editingUser, setEditingUser] = useState(null);
  const [userForm, setUserForm] = useState({ username: '', phone: '', email: '', role: '' });

  // 编辑商品
  const [editingProduct, setEditingProduct] = useState(null);
  const [productForm, setProductForm] = useState({});

  // 编辑订单
  const [editingOrder, setEditingOrder] = useState(null);
  const [orderStatusForm, setOrderStatusForm] = useState('');

  useEffect(() => {
    if (!user || user.role !== 'ADMIN') return;
    loadUsers();
    loadProducts();
    loadOrders();
  }, [user]);

  const loadUsers = async () => { try { setUsers(await getAllUsers()); } catch (err) { console.error(err); } };
  const loadProducts = async () => { try { const d = await getProducts(0, 1000); setProducts(d.content || []); } catch (err) { console.error(err); } };
  const loadOrders = async () => { try { setOrders(await getAllOrders()); } catch (err) { console.error(err); } };

  // 用户管理
  const handleEditUser = (u) => {
    setEditingUser(u);
    setUserForm({ username: u.username || '', phone: u.phone || '', email: u.email || '', role: u.role || 'USER' });
  };

  const handleSaveUser = async () => {
    try {
      await updateUser(editingUser.id, { username: userForm.username, phone: userForm.phone, email: userForm.email });
      await updateUserRole(editingUser.id, userForm.role);
      setEditingUser(null);
      loadUsers();
    } catch (err) { toast(err.message, 'error'); }
  };

  const handleDeleteUser = async (id) => {
    if (!await confirm('确定删除此用户？')) return;
    try { await deleteUser(id); loadUsers(); toast('用户已删除', 'success'); } catch (err) { toast(err.message, 'error'); }
  };

  // 商品管理
  const handleEditProduct = (p) => {
    setEditingProduct(p);
    setProductForm({ name: p.name, price: p.price, stock: p.stock, description: p.description });
  };

  const handleSaveProduct = async () => {
    try {
      await updateProduct(editingProduct.id, { ...productForm, price: Number(productForm.price), stock: Number(productForm.stock) });
      setEditingProduct(null);
      loadProducts();
    } catch (err) { toast(err.message, 'error'); }
  };

  const handleDeleteProduct = async (id) => {
    if (!await confirm('确定删除此商品？')) return;
    try { await deleteProduct(id); loadProducts(); toast('商品已删除', 'success'); } catch (err) { toast(err.message, 'error'); }
  };

  // 订单管理
  const handleSaveOrderStatus = async () => {
    try {
      await updateOrderStatus(editingOrder.id, orderStatusForm);
      setEditingOrder(null);
      loadOrders();
    } catch (err) { toast(err.message, 'error'); }
  };

  const handleDeleteOrder = async (id) => {
    if (!await confirm('确定删除此订单？')) return;
    try { await deleteOrder(id); loadOrders(); toast('订单已删除', 'success'); } catch (err) { toast(err.message, 'error'); }
  };

  if (!user || user.role !== 'ADMIN') return <p className="loading">无权限访问</p>;

  return (
    <div className="dashboard-page admin-dashboard">
      <h1>管理后台</h1>
      <div className="dashboard-tabs">
        <button className={tab === 'users' ? 'active' : ''} onClick={() => setTab('users')}>用户管理</button>
        <button className={tab === 'products' ? 'active' : ''} onClick={() => setTab('products')}>商品管理</button>
        <button className={tab === 'orders' ? 'active' : ''} onClick={() => setTab('orders')}>订单管理</button>
      </div>

      {tab === 'users' && (
        <div className="dashboard-content">
          <table className="admin-table">
            <thead><tr><th>ID</th><th>用户名</th><th>角色</th><th>手机号</th><th>邮箱</th><th>余额</th><th>操作</th></tr></thead>
            <tbody>
              {users.map(u => (
                <tr key={u.id}>
                  <td>{u.id}</td>
                  <td>{u.username}</td>
                  <td><span className="role-tag">{roleLabels[u.role] || u.role}</span></td>
                  <td>{u.phone || '-'}</td>
                  <td>{u.email || '-'}</td>
                  <td>{u.balance !== undefined ? `¥${u.balance}` : '-'}</td>
                  <td>
                    <button onClick={() => handleEditUser(u)}>编辑</button>
                    <button className="btn-danger" onClick={() => handleDeleteUser(u.id)}>删除</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {editingUser && (
            <div className="modal-overlay" onClick={() => setEditingUser(null)}>
              <div className="modal-box" onClick={e => e.stopPropagation()}>
                <h3>编辑用户 #{editingUser.id}</h3>
                <div className="form-group"><label>用户名</label><input value={userForm.username} onChange={e => setUserForm({ ...userForm, username: e.target.value })} /></div>
                <div className="form-group"><label>手机号</label><input value={userForm.phone} onChange={e => setUserForm({ ...userForm, phone: e.target.value })} /></div>
                <div className="form-group"><label>邮箱</label><input value={userForm.email} onChange={e => setUserForm({ ...userForm, email: e.target.value })} /></div>
                <div className="form-group">
                  <label>角色</label>
                  <select value={userForm.role} onChange={e => setUserForm({ ...userForm, role: e.target.value })}>
                    <option value="USER">用户</option>
                    <option value="MERCHANT">商家</option>
                    <option value="ADMIN">管理员</option>
                  </select>
                </div>
                <div className="form-actions">
                  <button onClick={handleSaveUser}>保存</button>
                  <button onClick={() => setEditingUser(null)}>取消</button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {tab === 'products' && (
        <div className="dashboard-content">
          <table className="admin-table">
            <thead><tr><th>ID</th><th>图片</th><th>名称</th><th>价格</th><th>库存</th><th>商家ID</th><th>操作</th></tr></thead>
            <tbody>
              {products.map(p => (
                <tr key={p.id}>
                  <td>{p.id}</td>
                  <td>{p.imageUrl ? <img src={getImageUrl(p.imageUrl)} alt="" className="admin-thumb" /> : '-'}</td>
                  <td>{p.name}</td>
                  <td>¥{p.price}</td>
                  <td>{p.stock}</td>
                  <td>{p.merchantId}</td>
                  <td>
                    <button onClick={() => handleEditProduct(p)}>编辑</button>
                    <button className="btn-danger" onClick={() => handleDeleteProduct(p.id)}>删除</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {editingProduct && (
            <div className="modal-overlay" onClick={() => setEditingProduct(null)}>
              <div className="modal-box" onClick={e => e.stopPropagation()}>
                <h3>编辑商品 #{editingProduct.id}</h3>
                <div className="form-group"><label>名称</label><input value={productForm.name} onChange={e => setProductForm({ ...productForm, name: e.target.value })} /></div>
                <div className="form-group"><label>价格</label><input type="number" step="0.01" value={productForm.price} onChange={e => setProductForm({ ...productForm, price: e.target.value })} /></div>
                <div className="form-group"><label>库存</label><input type="number" value={productForm.stock} onChange={e => setProductForm({ ...productForm, stock: e.target.value })} /></div>
                <div className="form-group"><label>描述</label><textarea value={productForm.description} onChange={e => setProductForm({ ...productForm, description: e.target.value })} /></div>
                <div className="form-actions">
                  <button onClick={handleSaveProduct}>保存</button>
                  <button onClick={() => setEditingProduct(null)}>取消</button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {tab === 'orders' && (
        <div className="dashboard-content">
          <table className="admin-table">
            <thead><tr><th>ID</th><th>用户ID</th><th>商家ID</th><th>金额</th><th>状态</th><th>创建时间</th><th>操作</th></tr></thead>
            <tbody>
              {orders.map(o => (
                <tr key={o.id}>
                  <td>{o.id}</td>
                  <td>{o.userId}</td>
                  <td>{o.merchantId}</td>
                  <td>¥{o.totalPrice}</td>
                  <td><span style={{ color: o.status === 'CANCELLED' ? '#999' : '#1890ff' }}>{orderStatusMap[o.status]}</span></td>
                  <td>{new Date(o.createdAt).toLocaleString()}</td>
                  <td>
                    <button onClick={() => { setEditingOrder(o); setOrderStatusForm(o.status); }}>修改状态</button>
                    <button className="btn-danger" onClick={() => handleDeleteOrder(o.id)}>删除</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {editingOrder && (
            <div className="modal-overlay" onClick={() => setEditingOrder(null)}>
              <div className="modal-box" onClick={e => e.stopPropagation()}>
                <h3>修改订单状态 #{editingOrder.id}</h3>
                <div className="form-group">
                  <label>状态</label>
                  <select value={orderStatusForm} onChange={e => setOrderStatusForm(e.target.value)}>
                    {Object.entries(orderStatusMap).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
                  </select>
                </div>
                <div className="form-actions">
                  <button onClick={handleSaveOrderStatus}>保存</button>
                  <button onClick={() => setEditingOrder(null)}>取消</button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
