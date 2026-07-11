import { useState, useEffect, useMemo } from 'react';
import { getProducts } from '../api/product';
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

  const loadMore = async () => {
    if (loadingMore || !hasMore) return;
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

  const filtered = useMemo(() => {
    if (!keyword.trim()) return products;
    const kw = keyword.trim().toLowerCase();
    return products.filter(p =>
      p.name.toLowerCase().includes(kw) ||
      (p.category && p.category.toLowerCase().includes(kw))
    );
  }, [products, keyword]);

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
            <button className="btn-clear-input" onClick={() => setKeyword('')}>&times;</button>
          )}
        </div>
      </div>
      {loading ? (
        <p className="loading">加载中...</p>
      ) : (
        <>
          {filtered.length === 0 ? (
            <p className="no-results">未找到匹配「{keyword}」的商品</p>
          ) : (
            <div className="product-grid">
              {filtered.map(p => (
                <ProductCard key={p.id} product={p} />
              ))}
            </div>
          )}
          {hasMore && !keyword && (
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
import { useState, useEffect, useMemo } from 'react';
import { getProducts } from '../api/product';
import ProductCard from '../components/ProductCard';
import './Home.css';

export default function Home() {
  const [allProducts, setAllProducts] = useState([]);
  const [keyword, setKeyword] = useState('');
  const [page, setPage] = useState(0);
  const [loading, setLoading] = useState(true);
  const pageSize = 8;

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getProducts(0, 100);
        setAllProducts(data.content || []);
      } catch (err) {
        console.error(err);
      }
      setLoading(false);
    };
    load();
  }, []);

  const filtered = useMemo(() => {
    if (!keyword.trim()) return allProducts;
    const kw = keyword.trim().toLowerCase();
    return allProducts.filter(p =>
      p.name.toLowerCase().includes(kw) ||
      (p.category && p.category.toLowerCase().includes(kw))
    );
  }, [allProducts, keyword]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / pageSize));
  const currentPage = Math.min(page, totalPages - 1);
  const displayProducts = filtered.slice(currentPage * pageSize, (currentPage + 1) * pageSize);

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
            onChange={(e) => { setKeyword(e.target.value); setPage(0); }}
          />
          {keyword && (
            <button className="btn-clear-input" onClick={() => { setKeyword(''); setPage(0); }}>&times;</button>
          )}
        </div>
      </div>
      {loading ? (
        <p className="loading">加载中...</p>
      ) : (
        <>
          {displayProducts.length === 0 ? (
            <p className="no-results">未找到匹配「{keyword}」的商品</p>
          ) : (
            <div className="product-grid">
              {displayProducts.map(p => (
                <ProductCard key={p.id} product={p} />
              ))}
            </div>
          )}
          {filtered.length > pageSize && (
            <div className="pagination">
              <button disabled={currentPage === 0} onClick={() => setPage(currentPage - 1)}>上一页</button>
              <span>{currentPage + 1} / {totalPages}</span>
              <button disabled={currentPage >= totalPages - 1} onClick={() => setPage(currentPage + 1)}>下一页</button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
