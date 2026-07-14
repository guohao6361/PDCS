import { useState, useEffect } from 'react';
import { getProducts, searchProducts } from '../api/product';
import ProductCard from '../components/ProductCard';
import './Home.css';

export default function Home() {
  const [products, setProducts] = useState([]);
  const [keyword, setKeyword] = useState('');
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(0);  // 当前页码（从0开始）
  const [totalPages, setTotalPages] = useState(0);     // 总页数
  const [totalElements, setTotalElements] = useState(0); // 总商品数
  const pageSize = 16;  // 每页显示16个商品

  // 加载商品数据
  const loadProducts = async (page, searchKeyword = '') => {
    setLoading(true);
    try {
      let data;
      if (searchKeyword.trim()) {
        data = await searchProducts(searchKeyword.trim(), page, pageSize);
      } else {
        data = await getProducts(page, pageSize);
      }
      setProducts(data.content || []);
      setCurrentPage(page);
      setTotalPages(data.totalPages || 0);
      setTotalElements(data.totalElements || 0);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  // 初始加载
  useEffect(() => {
    loadProducts(0);
  }, []);

  // 搜索处理
  useEffect(() => {
    if (!keyword.trim()) {
      loadProducts(0);
      return;
    }
    const timer = setTimeout(() => {
      loadProducts(0, keyword);
    }, 300);
    return () => clearTimeout(timer);
  }, [keyword]);

  // 跳转到指定页
  const goToPage = (page) => {
    if (page < 0 || page >= totalPages) return;
    loadProducts(page, keyword);
    // 滚动到页面顶部
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // 上一页
  const goToPrevPage = () => {
    if (currentPage > 0) {
      goToPage(currentPage - 1);
    }
  };

  // 下一页
  const goToNextPage = () => {
    if (currentPage < totalPages - 1) {
      goToPage(currentPage + 1);
    }
  };

  // 清除搜索
  const handleClearSearch = () => {
    setKeyword('');
    loadProducts(0);
  };

  // 生成页码数组
  const getPageNumbers = () => {
    const pages = [];
    const maxVisible = 5;  // 最多显示5个页码
    
    let start = Math.max(0, currentPage - Math.floor(maxVisible / 2));
    let end = Math.min(totalPages, start + maxVisible);
    
    if (end - start < maxVisible) {
      start = Math.max(0, end - maxVisible);
    }
    
    for (let i = start; i < end; i++) {
      pages.push(i);
    }
    
    return pages;
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
            <>
              <div className="product-grid">
                {products.map(p => (
                  <ProductCard key={p.id} product={p} />
                ))}
              </div>

              {/* 分页导航 */}
              <div className="pagination">
                <div className="pagination-info">
                  共 {totalElements} 个商品，第 {currentPage + 1} / {totalPages} 页
                </div>
                
                <div className="pagination-controls">
                  <button 
                    className="pagination-btn"
                    onClick={goToPrevPage} 
                    disabled={currentPage === 0}
                  >
                    &laquo; 上一页
                  </button>

                  {getPageNumbers().map(pageNum => (
                    <button
                      key={pageNum}
                      className={`pagination-btn ${pageNum === currentPage ? 'active' : ''}`}
                      onClick={() => goToPage(pageNum)}
                    >
                      {pageNum + 1}
                    </button>
                  ))}

                  <button 
                    className="pagination-btn"
                    onClick={goToNextPage} 
                    disabled={currentPage === totalPages - 1}
                  >
                    下一页 &raquo;
                  </button>
                </div>
              </div>
            </>
          )}
        </>
      )}
    </div>
  );
}
