import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getOrder } from '../api/order';
import { payOrder, cancelOrder } from '../api/payment';
import { useAuth } from '../context/AuthContext';
import './Payment.css';

const statusMap = {
  CREATED: '待支付',
  PAID: '已支付',
  CANCELLED: '已取消'
};

export default function Payment() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, updateUser } = useAuth();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [paying, setPaying] = useState(false);
  const [payResult, setPayResult] = useState(null); // 'success' | 'fail'

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getOrder(id);
        setOrder(data);
      } catch (err) {
        console.error(err);
      }
      setLoading(false);
    };
    load();
  }, [id]);

  const handlePay = async () => {
    setPaying(true);
    try {
      const result = await payOrder(order.id);
      setPayResult('success');
      setOrder({ ...order, status: 'PAID', paidAt: result.paidAt });
      // 更新本地余额
      updateUser({ ...user, balance: result.remainBalance });
    } catch (err) {
      setPayResult('fail');
      alert('支付失败：' + err.message);
    }
    setPaying(false);
  };

  const handleCancel = async () => {
    if (!window.confirm('确定取消此订单？')) return;
    try {
      await cancelOrder(order.id);
      setOrder({ ...order, status: 'CANCELLED' });
    } catch (err) {
      alert('取消失败：' + err.message);
    }
  };

  if (loading) return <p className="loading">加载中...</p>;
  if (!order) return <p>订单不存在</p>;

  return (
    <div className="payment-page">
      <button className="btn-back-orders" onClick={() => navigate('/orders')}>&#8592; 返回我的订单</button>
      <h1>订单支付</h1>

      {/* 订单信息卡片 */}
      <div className="payment-card">
        <div className="payment-order-info">
          <div className="info-row">
            <span className="label">订单编号</span>
            <span className="value">#{order.id}</span>
          </div>
          <div className="info-row">
            <span className="label">订单状态</span>
            <span className={`value status-badge status-${order.status.toLowerCase()}`}>
              {statusMap[order.status] || order.status}
            </span>
          </div>
          <div className="info-row">
            <span className="label">创建时间</span>
            <span className="value">{new Date(order.createdAt).toLocaleString()}</span>
          </div>
          {order.paidAt && (
            <div className="info-row">
              <span className="label">支付时间</span>
              <span className="value">{new Date(order.paidAt).toLocaleString()}</span>
            </div>
          )}
        </div>

        {/* 商品明细 */}
        <div className="payment-items">
          <h3>商品明细</h3>
          {order.items.map((item, idx) => (
            <div key={idx} className="payment-item">
              <span className="item-name">{item.productName}</span>
              <span className="item-qty">x{item.quantity}</span>
              <span className="item-price">¥{item.price * item.quantity}</span>
            </div>
          ))}
          <div className="payment-total">
            <span>应付总额</span>
            <span className="total-amount">¥{order.totalPrice}</span>
          </div>
        </div>

        {/* 操作区域 */}
        <div className="payment-actions">
          {order.status === 'CREATED' && (
            <>
              <div className="balance-info">
                当前余额：<strong>¥{user.balance}</strong>
                {user.balance < order.totalPrice && (
                  <span className="balance-warn">（余额不足）</span>
                )}
              </div>
              <div className="action-buttons">
                <button onClick={handleCancel} className="btn-cancel" disabled={paying}>
                  取消订单
                </button>
                <button
                  onClick={handlePay}
                  className="btn-pay"
                  disabled={paying || user.balance < order.totalPrice}
                >
                  {paying ? '支付中...' : '确认支付'}
                </button>
              </div>
            </>
          )}

          {order.status === 'PAID' && (
            <div className="pay-success">
              <div className="success-icon">&#10003;</div>
              <p>支付成功！</p>
              <button onClick={() => navigate('/orders')} className="btn-back">查看订单</button>
            </div>
          )}

          {order.status === 'CANCELLED' && (
            <div className="pay-cancelled">
              <p>订单已取消</p>
              <button onClick={() => navigate('/')} className="btn-back">继续购物</button>
            </div>
          )}

          {payResult === 'fail' && order.status === 'CREATED' && (
            <p className="pay-error">支付失败，请检查余额后重试</p>
          )}
        </div>
      </div>
    </div>
  );
}
