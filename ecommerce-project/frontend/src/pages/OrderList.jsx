import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getUserOrders } from '../api/order';
import { cancelOrder } from '../api/payment';
import { useAuth } from '../context/AuthContext';
import './OrderList.css';

const statusMap = {
  CREATED: '待支付',
  PAID: '已支付',
  CANCELLED: '已取消'
};

export default function OrderList() {
  const { user, updateUser } = useAuth();
  const navigate = useNavigate();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState(null);

  useEffect(() => {
    const load = async () => {
      if (!user) return;
      try {
        const data = await getUserOrders(user.id);
        setOrders(data);
      } catch (err) {
        console.error(err);
      }
      setLoading(false);
    };
    load();
  }, [user]);

  const toggleDetail = (orderId) => {
    setExpandedId(expandedId === orderId ? null : orderId);
  };

  const handlePay = (e, orderId) => {
    e.stopPropagation();
    navigate(`/payment/${orderId}`);
  };

  const handleCancel = async (e, orderId) => {
    e.stopPropagation();
    if (!window.confirm('确定取消此订单？')) return;
    try {
      await cancelOrder(orderId);
      setOrders(orders.map(o => o.id === orderId ? { ...o, status: 'CANCELLED' } : o));
    } catch (err) {
      alert(err.message);
    }
  };

  if (!user) return <p className="loading">请先登录</p>;
  if (loading) return <p className="loading">加载中...</p>;

  return (
    <div className="orders-page">
      <h1>我的订单</h1>
      {orders.length === 0 ? (
        <p className="empty-orders">暂无订单</p>
      ) : (
        <div className="orders-list">
          {orders.map(order => (
            <div key={order.id} className="order-card">
              <div className="order-header" onClick={() => toggleDetail(order.id)}>
                <span className="order-id">订单 #{order.id}</span>
                <span className={`order-status status-${order.status.toLowerCase()}`}>{statusMap[order.status] || order.status}</span>
                <span className="order-amount">¥{order.totalPrice}</span>
                <span className="order-date">{new Date(order.createdAt).toLocaleString()}</span>
                <span className={`order-arrow ${expandedId === order.id ? 'expanded' : ''}`}>&#9660;</span>
              </div>
              {expandedId === order.id && (
                <div className="order-detail">
                  <h4>商品明细</h4>
                  <table className="order-items-table">
                    <thead>
                      <tr>
                        <th>商品名称</th>
                        <th>单价</th>
                        <th>数量</th>
                        <th>小计</th>
                      </tr>
                    </thead>
                    <tbody>
                      {order.items && order.items.map((item, idx) => (
                        <tr key={idx}>
                          <td className="item-name">{item.productName}</td>
                          <td className="item-price">¥{item.price}</td>
                          <td className="item-qty">x{item.quantity}</td>
                          <td className="item-subtotal">¥{item.price * item.quantity}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  <div className="order-detail-footer">
                    <span>订单总额</span>
                    <span className="detail-total">¥{order.totalPrice}</span>
                  </div>
                  <div className="order-actions">
                    {order.status === 'CREATED' && (
                      <>
                        <button className="btn-cancel-order" onClick={(e) => handleCancel(e, order.id)}>取消订单</button>
                        <button className="btn-pay-order" onClick={(e) => handlePay(e, order.id)}>去支付</button>
                      </>
                    )}
                    {order.status !== 'CREATED' && (
                      <button className="btn-view-order" onClick={(e) => handlePay(e, order.id)}>查看详情</button>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
