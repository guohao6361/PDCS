import { useState, useEffect } from 'react';
import { getProducts, searchProducts } from '../api/product';
import ProductCard from '../components/ProductCard';
import './Home.css';

export default function Home() {
  const [products, setProducts] = useState([]);
  const [keyword, setKeyword] = useState('');
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const pageSize = 8;

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const data = await getProducts(0, pageSize);
        setProducts(data.content || []);
        setHasMore(!data.last);
        setPage(1);
      } catch (err) {
        console.error(err);
      }
      setLoading(false);
    };
    load();
  }, []);

  useEffect(() => {
    if (!keyword.trim()) return;
    const timer = setTimeout(async () => {
      setLoading(true);
      try {
        const data = await searchProducts(keyword.trim(), 0, 100);
        setProducts(data.content || []);
        setHasMore(!data.last);
        setPage(1);
      } catch (err) {
        console.error(err);
      }
      setLoading(false);
    }, 300);
    return () => clearTimeout(timer);
  }, [keyword]);

  const loadMore = async () => {
    if (loadingMore || !hasMore || keyword.trim()) return;
    setLoadingMore(true);
    try {
      const data = await getProducts(page, pageSize);
      setProducts(prev => [...prev, ...(data.content || [])]);
      setHasMore(!data.last);
      setPage(prev => prev + 1);
    } catch (err) {
      console.error(err);
    }
    setLoadingMore(false);
  };

  const handleClearSearch = () => {
    setKeyword('');
    setLoading(true);
    getProducts(0, pageSize).then(data => {
      setProducts(data.content || []);
      setHasMore(!data.last);
      setPage(1);
    }).catch(console.error).finally(() => setLoading(false));
  };

  return (
    <div className="home-page">
      <h1 className="page-title">全部商品</h1>
      <div className="search-bar">
        <div className="search-input-wrapper">
          <span className="search-icon">&#128269;</span>
          <input
            type="text"
            placeholder="搜索商品名称或分类..."
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
          />
          {keyword && (
            <button className="btn-clear-input" onClick={handleClearSearch}>&times;</button>
          )}
        </div>
      </div>
      {loading ? (
        <p className="loading">加载中...</p>
      ) : (
        <>
          {products.length === 0 ? (
            <p className="no-results">未找到匹配「{keyword}」的商品</p>
          ) : (
            <div className="product-grid">
              {products.map(p => (
                <ProductCard key={p.id} product={p} />
              ))}
            </div>
          )}
          {hasMore && !keyword.trim() && (
            <div className="load-more">
              <button onClick={loadMore} disabled={loadingMore}>
                {loadingMore ? '加载中...' : '加载更多'}
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
