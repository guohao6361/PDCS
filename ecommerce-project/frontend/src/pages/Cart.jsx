import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCart, removeFromCart, clearCart } from '../api/cart';
import { getProduct } from '../api/product';
import { createOrder } from '../api/order';
import { useAuth } from '../context/AuthContext';
import './Cart.css';

export default function Cart() {
  const { user, updateUser } = useAuth();
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [selected, setSelected] = useState(new Set());
  const [loading, setLoading] = useState(true);

  const loadCart = async () => {
    if (!user) return;
    try {
      const data = await getCart(user.id);
      const cartItems = data.items || [];
      const enriched = await Promise.all(
        cartItems.map(async (ci) => {
          try {
            const product = await getProduct(ci.productId);
            return { ...ci, product };
          } catch {
            return { ...ci, product: { id: ci.productId, name: '商品已下架', price: 0 } };
          }
        })
      );
      setItems(enriched);
      setSelected(new Set());
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => {
    loadCart();
  }, [user]);

  const toggleSelect = (productId) => {
    const next = new Set(selected);
    if (next.has(productId)) next.delete(productId);
    else next.add(productId);
    setSelected(next);
  };

  const toggleAll = () => {
    if (selected.size === items.length) setSelected(new Set());
    else setSelected(new Set(items.map(i => i.productId)));
  };

  const handleRemove = async (productId) => {
    try {
      await removeFromCart(user.id, productId);
      await loadCart();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleCheckout = async () => {
    if (selected.size === 0) return alert('请先选择商品');
    try {
      const order = await createOrder(user.id);
      updateUser({ ...user, balance: user.balance - order.totalPrice });
      navigate(`/payment/${order.id}`);
    } catch (err) {
      alert(err.message);
    }
  };

  const handleClear = async () => {
    try {
      await clearCart(user.id);
      setItems([]);
      setSelected(new Set());
    } catch (err) {
      alert(err.message);
    }
  };

  if (!user) return <p className="loading">请先登录</p>;
  if (loading) return <p className="loading">加载中...</p>;

  const selectedItems = items.filter(i => selected.has(i.productId));
  const total = selectedItems.reduce((sum, i) => sum + (i.product?.price || 0) * i.quantity, 0);
  const allSelected = items.length > 0 && selected.size === items.length;

  return (
    <div className="cart-page">
      <h1>购物车</h1>
      {items.length === 0 ? (
        <p className="empty-cart">购物车是空的</p>
      ) : (
        <>
          <div className="cart-select-all">
            <label className="checkbox-label">
              <input type="checkbox" checked={allSelected} onChange={toggleAll} />
              <span>全选</span>
            </label>
          </div>
          <div className="cart-list">
            {items.map((item, idx) => (
              <div key={idx} className="cart-item">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={selected.has(item.productId)}
                    onChange={() => toggleSelect(item.productId)}
                  />
                </label>
                <div className="cart-item-info">
                  <h3>{item.product?.name || `商品#${item.productId}`}</h3>
                  <p className="cart-item-price">¥{item.product?.price || 0} x {item.quantity}</p>
                </div>
                <p className="cart-item-subtotal">¥{(item.product?.price || 0) * item.quantity}</p>
                <button onClick={() => handleRemove(item.productId)} className="btn-remove">删除</button>
              </div>
            ))}
          </div>
          <div className="cart-summary">
            <p className="cart-total">
              已选 <strong>{selected.size}</strong> 件，总计：<strong>¥{total}</strong>
            </p>
            <div className="cart-actions">
              <button onClick={handleClear} className="btn-clear">清空购物车</button>
              <button onClick={handleCheckout} className="btn-checkout" disabled={selected.size === 0}>
                去结算
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
