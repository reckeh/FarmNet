<template>
  <div class="cart-page">
    <h1 class="text-3xl font-bold mb-6">🛒 My Cart</h1>

    <div v-if="cart.length === 0" class="text-gray-600 text-lg">Your cart is empty.</div>
    <div v-else>
      <div class="cart-items">
        <div
          v-for="item in cart"
          :key="item.product_id"
          class="cart-item"
        >
          <img
            :src="baseURL + item.image_url"
            alt="Product Image"
            class="item-image"
          />
          <div class="item-details">
            <h2 class="item-name">{{ item.name }}</h2>
            <p class="item-price">KES {{ item.price }}</p>
            <div class="quantity-controls">
              <button @click="decreaseQty(item)">−</button>
              <span>{{ item.quantity }}</span>
              <button @click="increaseQty(item)">＋</button>
            </div>
            <p class="item-subtotal">
              Subtotal: KES {{ (item.price * item.quantity).toFixed(2) }}
            </p>
            <button @click="removeItem(item)" class="remove-btn">Remove</button>
          </div>
        </div>
      </div>

      <div class="cart-summary">
        <h2 class="text-xl font-semibold mb-2">Cart Summary</h2>
        <p class="summary-total">Total: KES {{ totalAmount.toFixed(2) }}</p>
        <router-link to="/checkout" class="checkout-button">
          Proceed to Checkout 💳
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CartView",
  data() {
    return {
      cart: JSON.parse(localStorage.getItem("cart")) || [],
      baseURL: "http://127.0.0.1:5000/"
    };
  },
  computed: {
    totalAmount() {
      return this.cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    }
  },
  methods: {
    increaseQty(item) {
      item.quantity++;
      this.updateCart();
    },
    decreaseQty(item) {
      if (item.quantity > 1) {
        item.quantity--;
        this.updateCart();
      }
    },
    removeItem(item) {
      this.cart = this.cart.filter(i => i.product_id !== item.product_id);
      this.updateCart();
    },
    updateCart() {
      localStorage.setItem("cart", JSON.stringify(this.cart));
    }
  }
};
</script>

<style scoped>
.cart-page {
  padding: 2rem;
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.cart-item {
  display: flex;
  gap: 1.5rem;
  border: 1px solid #e0e0e0;
  padding: 1rem;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.item-image {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 8px;
}

.item-details {
  flex: 1;
}

.item-name {
  font-size: 18px;
  font-weight: 600;
}

.item-price {
  color: #28a745;
  font-weight: 500;
  margin: 0.5rem 0;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0.5rem 0;
}

.quantity-controls button {
  background: #007bff;
  color: #fff;
  border: none;
  padding: 4px 10px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 4px;
}

.item-subtotal {
  font-weight: 500;
}

.remove-btn {
  margin-top: 8px;
  color: #dc3545;
  background: none;
  border: none;
  font-size: 14px;
  cursor: pointer;
  text-decoration: underline;
}

.cart-summary {
  border-top: 2px solid #eaeaea;
  padding-top: 1rem;
  text-align: right;
}

.summary-total {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 1rem;
}

.checkout-button {
  background: #28a745;
  color: white;
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 16px;
  text-decoration: none;
  transition: background 0.3s ease;
}

.checkout-button:hover {
  background: #218838;
}

@media (max-width: 768px) {
  .cart-item {
    flex-direction: column;
    align-items: center;
  }

  .item-details {
    text-align: center;
  }

  .cart-summary {
    text-align: center;
  }
}
</style>
