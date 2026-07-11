import { useAuth } from '../context/AuthContext';
import { addToCart } from '../api/cart';
import './ProductCard.css';

export default function ProductCard({ product, onRefresh }) {
  const { user } = useAuth();

  const handleAddToCart = async () => {
    if (!user) {
      alert('请先登录');
      return;
    }
    try {
      await addToCart(user.id, product.id);
      alert('已加入购物车');
      if (onRefresh) onRefresh();
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className="product-card">
      <div className="product-category">{product.category}</div>
      <div className="product-info">
        <h3 className="product-name">{product.name}</h3>
        <p className="product-price">¥{product.price}</p>
        <p className="product-stock">库存: {product.stock}</p>
        <button onClick={handleAddToCart} className="btn-add-cart">加入购物车</button>
      </div>
    </div>
  );
}
