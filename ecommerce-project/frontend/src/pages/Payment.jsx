import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getOrder, payOrder, cancelOrder } from '../api/order';
import { getAddresses, createAddress, deleteAddress } from '../api/user';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../components/Toast';
import './Payment.css';

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

const PAYMENT_TIMEOUT = 15 * 60 * 1000;

export default function Payment() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, refreshUser } = useAuth();
  const { toast, confirm } = useToast();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [paying, setPaying] = useState(false);
  const [payPassword, setPayPassword] = useState('');
  const [addresses, setAddresses] = useState([]);
  const [selectedAddressId, setSelectedAddressId] = useState(null);
  const [showNewAddress, setShowNewAddress] = useState(false);
  const [newAddress, setNewAddress] = useState({ receiverName: '', phone: '', province: '', city: '', district: '', detailAddress: '' });
  const [countdown, setCountdown] = useState('');
  const intervalRef = useRef(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [orderData, addrData] = await Promise.all([
          getOrder(id),
          user ? getAddresses(user.id) : Promise.resolve([])
        ]);
        setOrder(orderData);
        setAddresses(addrData || []);
        const defaultAddr = (addrData || []).find(a => a.isDefault);
        if (defaultAddr) setSelectedAddressId(defaultAddr.id);
        else if (addrData?.length > 0) setSelectedAddressId(addrData[0].id);
      } catch (err) {
        console.error(err);
      }
      setLoading(false);
    };
    load();
  }, [id, user]);

  useEffect(() => {
    if (!order || order.status !== 'UNPAID') return;
    const update = () => {
      const elapsed = Date.now() - new Date(order.createdAt).getTime();
      const remaining = PAYMENT_TIMEOUT - elapsed;
      if (remaining <= 0) {
        setCountdown('已超时');
        clearInterval(intervalRef.current);
        handleAutoCancel();
        return;
      }
      const mins = Math.floor(remaining / 60000);
      const secs = Math.floor((remaining % 60000) / 1000);
      setCountdown(`${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`);
    };
    update();
    intervalRef.current = setInterval(update, 1000);
    return () => clearInterval(intervalRef.current);
  }, [order]);

  const handleAutoCancel = async () => {
    try {
      await cancelOrder(order.id);
      toast('订单已超时，已自动取消', 'error');
      navigate('/orders');
    } catch (err) {
      console.error(err);
    }
  };

  const handlePay = async () => {
    if (!selectedAddressId) return toast('请选择收货地址', 'error');
    if (!/^\d{6}$/.test(payPassword)) return toast('请输入6位数字支付密码', 'error');
    setPaying(true);
    try {
      await payOrder(order.id, { payPassword, addressId: selectedAddressId });
      setOrder({ ...order, status: 'PAID' });
      await refreshUser();
    } catch (err) {
      toast('支付失败：' + err.message, 'error');
    }
    setPaying(false);
  };

  const handleCancel = async () => {
    if (!await confirm('确定取消此订单？')) return;
    try {
      await cancelOrder(order.id);
      setOrder({ ...order, status: 'CANCELLED' });
    } catch (err) {
      toast('取消失败：' + err.message, 'error');
    }
  };

  const handleCreateAddress = async () => {
    if (!newAddress.receiverName || !newAddress.phone || !newAddress.detailAddress) {
      return toast('请填写完整地址信息', 'error');
    }
    try {
      const addr = await createAddress(user.id, newAddress);
      setAddresses([...addresses, addr]);
      setSelectedAddressId(addr.id);
      setShowNewAddress(false);
      setNewAddress({ receiverName: '', phone: '', province: '', city: '', district: '', detailAddress: '' });
    } catch (err) {
      toast(err.message, 'error');
    }
  };

  const handleDeleteAddress = async (addrId) => {
    if (!await confirm('确定删除此地址？')) return;
    try {
      
      await deleteAddress(user.id, addrId);
      const updated = addresses.filter(a => a.id !== addrId);
      setAddresses(updated);
      if (selectedAddressId === addrId) {
        setSelectedAddressId(updated.length > 0 ? updated[0].id : null);
      }
    } catch (err) {
      toast(err.message, 'error');
    }
  };

  if (loading) return <p className="loading">加载中...</p>;
  if (!order) return <p>订单不存在</p>;

  return (
    <div className="payment-page">
      <button className="btn-back-orders" onClick={() => navigate('/orders')}>&#8592; 返回我的订单</button>
      <h1>订单支付</h1>

      <div className="payment-card">
        {order.status === 'UNPAID' && (
          <div className="payment-countdown">
            支付倒计时：<span className="countdown-value">{countdown}</span>
          </div>
        )}

        <div className="payment-order-info">
          <div className="info-row">
            <span className="label">订单编号</span>
            <span className="value">#{order.id}</span>
          </div>
          <div className="info-row">
            <span className="label">订单状态</span>
            <span className="value status-badge" style={{ color: statusColors[order.status] || '#333' }}>
              {statusMap[order.status] || order.status}
            </span>
          </div>
          <div className="info-row">
            <span className="label">创建时间</span>
            <span className="value">{new Date(order.createdAt).toLocaleString()}</span>
          </div>
        </div>

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

        <div className="payment-actions">
          {order.status === 'UNPAID' && (
            <>
              <div className="address-section">
                <h3>收货地址</h3>
                {addresses.length === 0 && !showNewAddress && (
                  <p className="no-address">暂无收货地址，请先添加</p>
                )}
                <div className="address-list">
                  {addresses.map(addr => (
                    <div key={addr.id} className={`address-item ${selectedAddressId === addr.id ? 'selected' : ''}`}>
                      <label className="address-radio">
                        <input
                          type="radio"
                          name="address"
                          checked={selectedAddressId === addr.id}
                          onChange={() => setSelectedAddressId(addr.id)}
                        />
                        <span className="address-info">
                          <strong>{addr.receiverName}</strong> {addr.phone}
                          <br />
                          {addr.province}{addr.city}{addr.district} {addr.detailAddress}
                          {addr.isDefault && <span className="default-tag">默认</span>}
                        </span>
                      </label>
                      <button className="btn-delete-address" onClick={() => handleDeleteAddress(addr.id)}>删除</button>
                    </div>
                  ))}
                </div>
                {addresses.length < 10 && (
                  <>
                    {showNewAddress ? (
                      <div className="new-address-form">
                        <input placeholder="收件人姓名" value={newAddress.receiverName} onChange={e => setNewAddress({ ...newAddress, receiverName: e.target.value })} required />
                        <input placeholder="手机号" value={newAddress.phone} onChange={e => setNewAddress({ ...newAddress, phone: e.target.value })} required />
                        <input placeholder="省" value={newAddress.province} onChange={e => setNewAddress({ ...newAddress, province: e.target.value })} />
                        <input placeholder="市" value={newAddress.city} onChange={e => setNewAddress({ ...newAddress, city: e.target.value })} />
                        <input placeholder="区" value={newAddress.district} onChange={e => setNewAddress({ ...newAddress, district: e.target.value })} />
                        <input placeholder="详细地址" value={newAddress.detailAddress} onChange={e => setNewAddress({ ...newAddress, detailAddress: e.target.value })} required />
                        <div className="address-form-actions">
                          <button onClick={handleCreateAddress}>保存</button>
                          <button onClick={() => setShowNewAddress(false)}>取消</button>
                        </div>
                      </div>
                    ) : (
                      <button className="btn-new-address" onClick={() => setShowNewAddress(true)}>+ 新增地址</button>
                    )}
                  </>
                )}
              </div>

              <div className="pay-password-section">
                <h3>支付密码</h3>
                <input
                  type="password"
                  placeholder="请输入6位支付密码"
                  value={payPassword}
                  onChange={e => setPayPassword(e.target.value)}
                  maxLength={6}
                  className="pay-password-input"
                />
              </div>

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
                  disabled={paying || user.balance < order.totalPrice || !selectedAddressId}
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

          {['SHIPPED', 'IN_TRANSIT', 'DELIVERED', 'COMPLETED'].includes(order.status) && (
            <div className="pay-info">
              <p>订单状态：{statusMap[order.status]}</p>
              <button onClick={() => navigate('/orders')} className="btn-back">查看订单</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
