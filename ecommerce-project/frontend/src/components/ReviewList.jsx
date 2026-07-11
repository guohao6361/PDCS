import './ReviewList.css';

export default function ReviewList({ reviews }) {
  if (!reviews || reviews.length === 0) {
    return <p className="no-reviews">暂无评价</p>;
  }

  return (
    <div className="review-list">
      {reviews.map(review => (
        <div key={review.id} className="review-item">
          <div className="review-header">
            <span className="review-username">{review.username}</span>
            <span className="review-rating">{'★'.repeat(review.rating)}{'☆'.repeat(5 - review.rating)}</span>
          </div>
          <p className="review-content">{review.content}</p>
        </div>
      ))}
    </div>
  );
}
