import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { getUserOrders, cancelOrder, updateOrderStatus } from '../api/order';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../components/Toast';
import './OrderList.css';

const statusMap = {
  UNPAID: '未支付',
  PAID: '已支付',
  SHIPPED: '已发货',
  IN_TRANSIT: '运输中',
  DELIVERED: '已送达',
  COMPLETED: '已完成',
  CANCELLED: '已取消'
};

const statusColors = {
  UNPAID: '#faad14',
  PAID: '#1890ff',
  SHIPPED: '#722ed1',
  IN_TRANSIT: '#13c2c2',
  DELIVERED: '#52c41a',
  COMPLETED: '#389e0d',
  CANCELLED: '#999'
};

const PAYMENT_TIMEOUT = 15 * 60 * 1000; // 15 minutes

function CountdownTimer({ createdAt, onExpire }) {
  const [timeLeft, setTimeLeft] = useState('');
  const intervalRef = useRef(null);

  useEffect(() => {
    const update = () => {
      const elapsed = Date.now() - new Date(createdAt).getTime();
      const remaining = PAYMENT_TIMEOUT - elapsed;
      if (remaining <= 0) {
        setTimeLeft('已超时');
        clearInterval(intervalRef.current);
        if (onExpire) onExpire();
        return;
      }
      const mins = Math.floor(remaining / 60000);
      const secs = Math.floor((remaining % 60000) / 1000);
      setTimeLeft(`${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`);
    };
    update();
    intervalRef.current = setInterval(update, 1000);
    return () => clearInterval(intervalRef.current);
  }, [createdAt, onExpire]);

  return <span className="countdown-timer">{timeLeft}</span>;
}

export default function OrderList() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const { toast, confirm } = useToast();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState(null);
  const [statusFilter, setStatusFilter] = useState('ALL');

  const loadOrders = async () => {
    if (!user) return;
    try {
      const data = await getUserOrders(user.id);
      setOrders(data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => {
    loadOrders();
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
    if (!await confirm('确定取消此订单？')) return;
    try {
      const updated = await cancelOrder(orderId);
      setOrders(orders.map(o => o.id === orderId ? { ...o, status: updated.status || 'CANCELLED' } : o));
    } catch (err) {
      toast(err.message, 'error');
    }
  };

  const handleConfirmReceipt = async (e, orderId) => {
    e.stopPropagation();
    if (!await confirm('确认已收到商品？')) return;
    try {
      const updated = await updateOrderStatus(orderId, 'COMPLETED');
      setOrders(orders.map(o => o.id === orderId ? { ...o, status: updated.status || 'COMPLETED' } : o));
    } catch (err) {
      toast(err.message, 'error');
    }
  };

  const handleTimeoutCancel = async (orderId) => {
    try {
      await cancelOrder(orderId);
      setOrders(orders.map(o => o.id === orderId ? { ...o, status: 'CANCELLED' } : o));
    } catch (err) {
      console.error(err);
    }
  };

  const filteredOrders = statusFilter === 'ALL'
    ? orders
    : orders.filter(o => o.status === statusFilter);

  if (!user) return <p className="loading">请先登录</p>;
  if (loading) return <p className="loading">加载中...</p>;

  return (
    <div className="orders-page">
      <h1>我的订单</h1>
      <div className="order-filter">
        <button className={statusFilter === 'ALL' ? 'active' : ''} onClick={() => setStatusFilter('ALL')}>全部</button>
        {Object.entries(statusMap).map(([key, label]) => (
          <button key={key} className={statusFilter === key ? 'active' : ''} onClick={() => setStatusFilter(key)}>
            {label}
          </button>
        ))}
      </div>
      {filteredOrders.length === 0 ? (
        <p className="empty-orders">暂无订单</p>
      ) : (
        <div className="orders-list">
          {filteredOrders.map(order => (
            <div key={order.id} className="order-card">
              <div className="order-header" onClick={() => toggleDetail(order.id)}>
                <span className="order-id">订单 #{order.id}</span>
                <span className="order-status" style={{ color: statusColors[order.status] || '#333' }}>
                  {statusMap[order.status] || order.status}
                </span>
                <span className="order-amount">¥{order.totalPrice}</span>
                <span className="order-date">{new Date(order.createdAt).toLocaleString()}</span>
                <span className={`order-arrow ${expandedId === order.id ? 'expanded' : ''}`}>&#9660;</span>
              </div>
              {expandedId === order.id && (
                <div className="order-detail">
                  {order.status === 'UNPAID' && (
                    <div className="order-countdown">
                      支付倒计时：<CountdownTimer createdAt={order.createdAt} onExpire={() => handleTimeoutCancel(order.id)} />
                    </div>
                  )}
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
                    {order.status === 'UNPAID' && (
                      <>
                        <button className="btn-cancel-order" onClick={(e) => handleCancel(e, order.id)}>取消订单</button>
                        <button className="btn-pay-order" onClick={(e) => handlePay(e, order.id)}>去支付</button>
                      </>
                    )}
                    {order.status === 'DELIVERED' && (
                      <button className="btn-confirm-receipt" onClick={(e) => handleConfirmReceipt(e, order.id)}>确认收货</button>
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
