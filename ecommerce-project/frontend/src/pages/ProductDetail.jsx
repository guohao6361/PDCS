import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getProduct, getReviews, addReview } from '../api/product';
import { addToCart } from '../api/cart';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../components/Toast';
import ReviewList from '../components/ReviewList';
import { getImageUrl } from '../utils/image';
import './ProductDetail.css';

export default function ProductDetail() {
  const { id } = useParams();
  const { user } = useAuth();
  const { toast } = useToast();
  const [product, setProduct] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [rating, setRating] = useState(5);
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const [p, r] = await Promise.all([getProduct(id), getReviews(id)]);
        setProduct(p);
        setReviews(r);
      } catch (err) {
        console.error(err);
      }
      setLoading(false);
    };
    load();
  }, [id]);

  const outOfStock = !product?.stock || product?.stock <= 0;

  const handleAddToCart = async () => {
    if (!user) return toast('请先登录', 'error');
    if (outOfStock) return toast('商品已售罄', 'error');
    try {
      await addToCart(user.id, product.id);
      toast('已加入购物车', 'success');
    } catch (err) {
      toast(err.message, 'error');
    }
  };

  const handleAddReview = async (e) => {
    e.preventDefault();
    if (!user) return toast('请先登录', 'error');
    try {
      const review = await addReview({
        productId: parseInt(id),
        username: user.username,
        rating,
        content
      });
      setReviews([...reviews, review]);
      setContent('');
    } catch (err) {
      toast(err.message, 'error');
    }
  };

  if (loading) return <p className="loading">加载中...</p>;
  if (!product) return <p>商品不存在</p>;

  return (
    <div className="detail-page">
      <div className="detail-header">
        <div className="detail-image">
          {product.imageUrl ? (
            <img src={getImageUrl(product.imageUrl)} alt={product.name} className="detail-product-image" />
          ) : (
            <div className="detail-image-placeholder">暂无图片</div>
          )}
        </div>
        <div className="detail-info">
          <span className="detail-category">{product.category}</span>
          <h1>{product.name}</h1>
          <p className="detail-price">¥{product.price}</p>
          <p className="detail-stock">库存：{product.stock ?? 0}</p>
          {product.description && <p className="detail-description">{product.description}</p>}
          {product.attributes && (
            <div className="detail-attributes">
              {Object.entries(product.attributes).map(([key, val]) => (
                <span key={key} className="attr-tag">{key}: {val}</span>
              ))}
            </div>
          )}
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

      <div className="review-section">
        <h2>用户评价</h2>
        <ReviewList reviews={reviews} />

        {user && (
          <form className="review-form" onSubmit={handleAddReview}>
            <h3>发表评价</h3>
            <select value={rating} onChange={e => setRating(Number(e.target.value))}>
              {[5, 4, 3, 2, 1].map(n => (
                <option key={n} value={n}>{'★'.repeat(n)}{'☆'.repeat(5 - n)}</option>
              ))}
            </select>
            <textarea
              placeholder="写下你的评价..."
              value={content}
              onChange={e => setContent(e.target.value)}
              required
            />
            <button type="submit">提交评价</button>
          </form>
        )}
      </div>
    </div>
  );
}
