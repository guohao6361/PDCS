import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getProduct, getReviews, addReview } from '../api/product';
import { addToCart } from '../api/cart';
import { useAuth } from '../context/AuthContext';
import ReviewList from '../components/ReviewList';
import './ProductDetail.css';

export default function ProductDetail() {
  const { id } = useParams();
  const { user } = useAuth();
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

  const handleAddToCart = async () => {
    if (!user) return alert('请先登录');
    try {
      await addToCart(user.id, product.id);
      alert('已加入购物车');
    } catch (err) {
      alert(err.message);
    }
  };

  const handleAddReview = async (e) => {
    e.preventDefault();
    if (!user) return alert('请先登录');
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
      alert(err.message);
    }
  };

  if (loading) return <p className="loading">加载中...</p>;
  if (!product) return <p>商品不存在</p>;

  return (
    <div className="detail-page">
      <div className="detail-header">
        <div className="detail-info">
          <span className="detail-category">{product.category}</span>
          <h1>{product.name}</h1>
          <p className="detail-price">¥{product.price}</p>
          <p className="detail-stock">库存：{product.stock}</p>
          {product.attributes && (
            <div className="detail-attributes">
              {Object.entries(product.attributes).map(([key, val]) => (
                <span key={key} className="attr-tag">{key}: {val}</span>
              ))}
            </div>
          )}
          <button onClick={handleAddToCart} className="btn-add-cart">加入购物车</button>
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
