<template>
  <div class="buyer-dashboard">
    <!-- Top Buttons -->
    <div class="flex justify-end gap-4 mb-4">
      <!-- View Cart and Checkout -->
      <router-link to="/cart" class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
        🧾 View Cart
      </router-link>
      <router-link to="/checkout" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
        💳 Checkout
      </router-link>
    </div>

    <!-- My Orders -->
    <div class="my-orders mb-6">
      <h2 class="text-2xl font-bold mb-4">🧾 My Orders</h2>
      <div v-if="orders.length === 0">No orders found.</div>
      <div v-else>
        <div
          v-for="order in orders"
          :key="order.id"
          class="order-card border border-gray-300 p-4 mb-4 rounded shadow bg-white"
        >
          <div class="flex justify-between items-center mb-2">
            <p><strong>Order ID:</strong> {{ order.id }}</p>
            <p><strong>Status:</strong> {{ order.status }}</p>
          </div>
          <p><strong>Total:</strong> KES {{ order.total_price }}</p>
          <p><strong>Placed:</strong> {{ formatDate(order.order_date) }}</p>

          <!-- Order Items -->
          <div class="order-items mt-4">
            <h3 class="font-semibold mb-2">Items:</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              <div
                v-for="item in order.items"
                :key="item.product_id"
                class="order-item card-hover border border-gray-300 p-4 rounded-lg shadow-md bg-white"
              >
                <img
                  :src="baseURL + item.product_image"
                  alt="Product"
                  class="w-full h-40 object-cover rounded mb-4"
                />
                <div>
                  <p class="font-medium">{{ item.product_name }}</p>
                  <p>Price: KES {{ item.product_price }}</p>
                  <p>Quantity: {{ item.quantity }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Search -->
    <div class="search-container mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search products..."
        class="search-input"
      />
    </div>

    <!-- Product List -->
    <div class="product-list">
      <h1 class="text-2xl font-bold mb-4">Available Products</h1>
      <div v-if="loading">Loading products...</div>
      <div v-else>
        <div class="products-grid">
          <div class="products-row" v-for="(row, rowIndex) in productRows" :key="rowIndex">
            <div
              v-for="product in row"
              :key="product.id"
              class="product-card"
            >
              <img
                :src="baseURL + product.image_url"
                alt="Product"
                class="product-image"
              />
              <h2 class="product-name">{{ product.name }}</h2>
              <p class="product-description">{{ product.description }}</p>
              <p class="product-price">{{ product.price }} KES / {{ product.unit }}</p>
              <p class="product-availability">Available: {{ product.quantity }}</p>
              <button
                @click="addToCart(product)"
                class="add-to-cart-button"
              >
                Add to Cart
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast Notification -->
    <div
      v-if="showToast"
      class="fixed bottom-5 right-5 bg-green-600 text-white px-4 py-2 rounded shadow-lg z-50"
    >
      {{ toastMessage }}
    </div>
  </div>
</template>

<script>
export default {
  name: "BuyerDashboard",
  data() {
    return {
      products: [],
      cartItems: JSON.parse(localStorage.getItem("cart")) || [],
      orders: [],
      loading: true,
      searchQuery: "",
      baseURL: "http://127.0.0.1:5000/",
      toastMessage: "",
      showToast: false,
      productsPerRow: 4
    };
  },
  computed: {
    filteredProducts() {
      return this.products.filter((product) =>
        product.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    productRows() {
      const rows = [];
      for (let i = 0; i < this.filteredProducts.length; i += this.productsPerRow) {
        rows.push(this.filteredProducts.slice(i, i + this.productsPerRow));
      }
      return rows;
    }
  },
  mounted() {
    // Fetch products
    fetch("http://127.0.0.1:5000/products/products")
      .then((res) => res.json())
      .then((data) => {
        this.products = data;
        this.loading = false;
      })
      .catch((err) => {
        console.error("Error fetching products:", err);
        this.loading = false;
      });

    // Fetch orders
    const token = localStorage.getItem("token");
    if (token) {
      fetch("http://127.0.0.1:5000/cart/orders", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((res) => res.json())
        .then((data) => {
          this.orders = data.orders || [];
        })
        .catch((err) => {
          console.error("Error fetching orders:", err);
        });
    }
  },
  methods: {
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleString("en-KE", {
        weekday: "short",
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },
    addToCart(product) {
      const token = localStorage.getItem("token");
      if (!token) {
        alert("You must be logged in to add items to your cart.");
        return;
      }

      fetch("http://127.0.0.1:5000/cart", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          product_id: product.id,
          quantity: 1,
        }),
      })
        .then((res) => {
          if (!res.ok) throw new Error("Failed to add to cart");
          return res.json();
        })
        .then((data) => {
          const existingProduct = this.cartItems.find(
            (item) => item.product_id === data.product_id
          );

          if (existingProduct) {
            existingProduct.quantity += 1;
          } else {
            this.cartItems.push({
              id: data.id,
              name: data.product_name,
              price: data.product_price,
              quantity: data.quantity,
              image_url: data.product_image,
              product_id: data.product_id,
            });
          }

          localStorage.setItem("cart", JSON.stringify(this.cartItems));
          this.triggerToast("✅ Added to cart!");
        })
        .catch((err) => {
          console.error("Error adding to cart:", err);
          alert("Error adding to cart.");
        });
    },
    triggerToast(message) {
      this.toastMessage = message;
      this.showToast = true;
      setTimeout(() => {
        this.showToast = false;
      }, 2500);
    },
  },
};
</script>

<style scoped>
.buyer-dashboard {
  padding: 2rem;
}

.search-container {
  text-align: center;
  margin-bottom: 20px;
}

.search-input {
  width: 80%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.product-list {
  margin-top: 20px;
}

.products-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.products-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.product-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease-in-out;
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 12px;
}

.product-name {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 8px;
}

.product-description {
  font-size: 14px;
  color: #777;
  margin-bottom: 10px;
}

.product-price {
  font-size: 16px;
  font-weight: bold;
  color: #27a745;
  margin-bottom: 10px;
}

.product-availability {
  font-size: 14px;
  color: #333;
}

.add-to-cart-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s ease;
  width: 100%;
}

.add-to-cart-button:hover {
  background-color: #0056b3;
}

.order-item {
  padding: 10px;
  display: flex;
  align-items: center;
  transition: border 0.3s ease;
}

.order-item:hover {
  border: 2px solid #007bff;
}

.order-item img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
  margin-right: 16px;
}

.order-items {
  margin-top: 12px;
}

.cart-count-badge {
  background-color: red;
  color: white;
  font-size: 12px;
  border-radius: 50%;
  padding: 2px 6px;
  position: absolute;
  top: -10px;
  right: -10px;
}

@media (max-width: 1200px) {
  .products-row {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 900px) {
  .products-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .products-row {
    grid-template-columns: 1fr;
  }
}
</style>
