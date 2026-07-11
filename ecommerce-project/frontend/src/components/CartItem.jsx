import './CartItem.css';

export default function CartItem({ item, onUpdate, onRemove }) {
  const { product, quantity } = item;

  return (
    <div className="cart-item">
      <img src={product.image} alt={product.name} className="cart-item-image" />
      <div className="cart-item-info">
        <h3>{product.name}</h3>
        <p className="cart-item-price">¥{product.price}</p>
      </div>
      <div className="cart-item-quantity">
        <button onClick={() => onUpdate(product.id, quantity - 1)} disabled={quantity <= 1}>-</button>
        <span>{quantity}</span>
        <button onClick={() => onUpdate(product.id, quantity + 1)}>+</button>
      </div>
      <p className="cart-item-subtotal">¥{product.price * quantity}</p>
      <button onClick={() => onRemove(product.id)} className="btn-remove">删除</button>
    </div>
  );
}
