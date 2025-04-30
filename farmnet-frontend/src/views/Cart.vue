<template>
  <div class="cart-container">
    <h2>Your Cart</h2>

    <!-- If cart is empty -->
    <div v-if="cart.length === 0">
      <p>Your cart is empty.</p>
    </div>

    <!-- If cart has items -->
    <div v-else>
      <div v-for="(item, index) in cart" :key="item.id" class="cart-item">
        <div class="product-image-container">
          <img
            :src="baseURL + item.product_image"
            alt="Product"
            class="product-image"
          />
        </div>

        <div class="product-details">
          <h3>{{ item.product_name }}</h3>
          <p>Price: {{ item.price | currency }}</p>
          <div class="quantity-control">
            <button @click="decreaseQuantity(item)">−</button>
            <span>{{ item.quantity }}</span>
            <button @click="increaseQuantity(item)">+</button>
          </div>
          <p>Total: {{ (item.price * item.quantity) | currency }}</p>
        </div>

        <div class="remove-item">
          <button @click="removeItem(item.id)">Remove</button>
        </div>
      </div>

      <!-- Total price and Proceed to Checkout -->
      <div class="total-section">
        <div class="total-price">
          <h3>Total Price: {{ total_price | currency }}</h3>
        </div>
        <div class="checkout-btn">
          <button @click="goToCheckout">Proceed to Checkout</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  name: 'Cart',
  data() {
    return {
      cart: [],
      total_price: 0,
      baseURL: 'http://localhost:5000/', 
    };
  },
  mounted() {
    this.fetchCart();
  },
  methods: {
    async fetchCart() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:5000/cart', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const { cart, total_price } = response.data;
        this.cart = cart;
        this.total_price = total_price;
      } catch (error) {
        console.error("Error fetching cart:", error);
      }
    },

    async removeItem(itemId) {
      try {
        const token = localStorage.getItem('token');
        await axios.delete(`http://localhost:5000/cart/${itemId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.fetchCart(); 
      } catch (error) {
        console.error("Error removing item:", error);
      }
    },

    async increaseQuantity(item) {
      try {
        const token = localStorage.getItem('token');
        const updatedItem = { quantity: item.quantity + 1 };
        await axios.put(`http://localhost:5000/cart/${item.id}`, updatedItem, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.fetchCart();
      } catch (error) {
        console.error("Error increasing quantity:", error);
      }
    },

    async decreaseQuantity(item) {
      if (item.quantity > 1) {
        try {
          const token = localStorage.getItem('token');
          const updatedItem = { quantity: item.quantity - 1 };
          await axios.put(`http://localhost:5000/cart/${item.id}`, updatedItem, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.fetchCart();
        } catch (error) {
          console.error("Error decreasing quantity:", error);
        }
      }
    },

    goToCheckout() {
      this.$router.push('/checkout');
    }
  },
  filters: {
    currency(value) {
      return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
    },
  },
};
</script>

<style scoped>
.cart-container {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}
h2 {
  text-align: center;
  margin-bottom: 20px;
}
.cart-item {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}
.product-image-container {
  margin-right: 20px;
}
.product-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
}
.product-details {
  flex: 1;
}
.product-details h3 {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
}
.product-details p {
  margin: 5px 0;
}
.quantity-control {
  display: flex;
  align-items: center;
  margin: 10px 0;
}
.quantity-control button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 6px 12px;
  font-size: 16px;
  margin: 0 5px;
  cursor: pointer;
  border-radius: 5px;
}
.quantity-control button:hover {
  background-color: #388E3C;
}
.remove-item button {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 5px;
}
.remove-item button:hover {
  background-color: #d32f2f;
}
.total-section {
  margin-top: 30px;
  text-align: center;
}
.total-price {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 20px;
}
.checkout-btn button {
  background-color: #2196F3;
  color: white;
  padding: 12px 20px;
  font-size: 16px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}
.checkout-btn button:hover {
  background-color: #1976D2;
}
</style>
