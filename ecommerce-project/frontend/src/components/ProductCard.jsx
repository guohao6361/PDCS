import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useToast } from './Toast';
import { addToCart } from '../api/cart';
import { getImageUrl } from '../utils/image';
import './ProductCard.css';

export default function ProductCard({ product, onRefresh }) {
  const { user } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();
  const outOfStock = !product.stock || product.stock <= 0;

  const handleAddToCart = async (e) => {
    e.stopPropagation();
    if (!user) {
      toast('请先登录', 'error');
      return;
    }
    if (outOfStock) return;
    try {
      await addToCart(user.id, product.id);
      toast('已加入购物车', 'success');
      if (onRefresh) onRefresh();
    } catch (err) {
      toast(err.message, 'error');
    }
  };

  return (
    <div className="product-card" onClick={() => navigate(`/product/${product.id}`)}>
      <div className="product-image-wrapper">
        {product.imageData ? (
          <img src={product.imageData} alt={product.name} className="product-image" />
        ) : product.imageUrl ? (
          <img src={getImageUrl(product.imageUrl)} alt={product.name} className="product-image" />
        ) : (
          <div className="product-image-placeholder">暂无图片</div>
        )}
        {outOfStock && <div className="sold-out-badge">已售罄</div>}
      </div>
      <div className="product-category">{product.category}</div>
      <div className="product-info">
        <h3 className="product-name">{product.name}</h3>
        <p className="product-price">¥{product.price}</p>
        <p className="product-stock">库存: {product.stock ?? 0}</p>
        {user?.role === 'USER' && (
          <button
            onClick={handleAddToCart}
            className="btn-add-cart"
            disabled={outOfStock}
          >
            {outOfStock ? '已售罄' : '加入购物车'}
          </button>
        )}
      </div>
    </div>
  );
}
