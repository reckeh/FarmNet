<template>
  <div class="container">
    <h1 class="heading">🌾 Welcome, Farmer</h1>

    <!-- Add Product Section -->
    <div class="section">
      <h2 class="sub-heading">➕ Add New Product</h2>
      <div class="form">
        <div class="input-group">
          <input v-model="newProduct.name" placeholder="Name" />
          <input v-model="newProduct.description" placeholder="Description" />
        </div>
        <div class="input-group">
          <input v-model="newProduct.price" type="number" placeholder="Price (KES)" />
          <input v-model="newProduct.quantity" type="number" placeholder="Quantity" />
        </div>
        <div class="input-group">
          <input v-model="newProduct.unit" placeholder="Unit (e.g. Kg, Ltrs)" />
          <input type="file" @change="handleImageUpload($event, 'new')" />
        </div>
        <div v-if="previewNewImage" class="preview-wrapper">
          <img :src="previewNewImage" class="preview-img" />
        </div>
        <button class="btn primary" @click="submitProduct">Save Product</button>
      </div>
    </div>

    <!-- My Products Section -->
    <div class="section">
      <h2 class="sub-heading">📦 My Products</h2>
      <div v-if="loading" class="empty">Loading products...</div>
      <div v-else-if="products.length === 0" class="empty">No products found.</div>
      <div v-else class="grid">
        <div class="card" v-for="product in products" :key="product.id">
          <div v-if="isEditing === product.id">
            <input v-model="editCache.name" placeholder="Name" />
            <input v-model="editCache.description" placeholder="Description" />
            <input v-model="editCache.price" type="number" placeholder="Price" />
            <input v-model="editCache.quantity" type="number" placeholder="Quantity" />
            <input v-model="editCache.unit" placeholder="Unit" />
            <input type="file" @change="handleImageUpload($event, 'edit')" />
            <div v-if="previewEditImage" class="preview-wrapper">
              <img :src="previewEditImage" class="preview-img" />
            </div>
            <div class="btn-group">
              <button class="btn success" @click="saveEdit(product.id)">Save</button>
              <button class="btn danger" @click="cancelEdit">Cancel</button>
            </div>
          </div>
          <div v-else>
            <img :src="baseURL + product.image_url" class="product-img" />
            <h3>{{ product.name }}</h3>
            <p>{{ product.description }}</p>
            <p><strong>Price:</strong> {{ product.price }} KES</p>
            <p><strong>Qty:</strong> {{ product.quantity }} {{ product.unit }}</p>
            <div class="btn-group">
              <button class="btn edit" @click="editProduct(product)">Edit</button>
              <button class="btn danger" @click="deleteProduct(product.id)">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Orders Section -->
    <div class="section">
      <h2 class="sub-heading">📬 Orders Received</h2>
      <div v-if="orderLoading" class="empty">Loading orders...</div>
      <div v-else-if="orders.length === 0" class="empty">No orders yet.</div>
      <div v-else class="grid">
        <div class="card" v-for="order in orders" :key="order.id">
          <h3>Order ID: {{ order.id }}</h3>
          <p><strong>Customer:</strong> {{ order.customer_name }}</p>
          <p><strong>Quantity:</strong> {{ order.quantity }} {{ order.product_unit }}</p>
          <p><strong>Status:</strong> {{ order.status }}</p>
          <p><strong>Payment No:</strong> {{ order.payment_no }}</p>

          <div v-if="order.delivery">
            <p><strong>Delivery Address:</strong> {{ order.delivery.address }}</p>
            <p><strong>Tracking No:</strong> {{ order.delivery.tracking_number }}</p>
          </div>

          <a
            :href="`${baseURL}api/orders/${order.id}/pdf`"
            target="_blank"
            class="btn download"
          >
            📄 Download PDF
          </a>
        </div>
      </div>
    </div>

    <!-- Delivery Info Section -->
    <div class="section">
      <h2 class="sub-heading">🚚 Delivery Details</h2>
      <div v-if="deliveryLoading" class="empty">Loading delivery info...</div>
      <div v-else-if="deliveries.length === 0" class="empty">No deliveries yet.</div>
      <div v-else class="grid">
        <div class="card" v-for="delivery in deliveries" :key="delivery.id">
          <h3>Delivery ID: {{ delivery.id }}</h3>
          <p><strong>Order ID:</strong> {{ delivery.order_id }}</p>
          <p><strong>Status:</strong> {{ delivery.status }}</p>
          <p><strong>Tracking Number:</strong> {{ delivery.tracking_number }}</p>
          <p><strong>Address:</strong> {{ delivery.address }}</p>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "FarmerDashboard",
  data() {
    return {
      products: [],
      orders: [],
      deliveries: [],
      loading: true,
      orderLoading: true,
      deliveryLoading: true,
      baseURL: "http://127.0.0.1:5000/",
      newProduct: { name: "", description: "", price: "", quantity: "", unit: "", image_url: "" },
      previewNewImage: null,
      previewEditImage: null,
      isEditing: null,
      editCache: {},
    };
  },
  mounted() {
    this.fetchProducts();
    this.fetchDeliveries();
    this.fetchOrders();
  },
  methods: {
    async fetchProducts() {
      const token = localStorage.getItem("token");
      try {
        const res = await axios.get(`${this.baseURL}farmer/products`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.products = res.data;
      } catch (err) {
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    async fetchOrders() {
      const token = localStorage.getItem("token");
      try {
        const res = await axios.get(`${this.baseURL}api/orders`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.orders = res.data.map(order => ({
          ...order,
          delivery: this.deliveries.find(del => del.order_id === order.id) || null,
        }));
      } catch (err) {
        console.error(err);
      } finally {
        this.orderLoading = false;
      }
    },
    async fetchDeliveries() {
      const token = localStorage.getItem("token");
      try {
        const res = await axios.get(`${this.baseURL}api/deliveries/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.deliveries = res.data;
      } catch (err) {
        console.error(err);
      } finally {
        this.deliveryLoading = false;
      }
    },
    handleImageUpload(event, type) {
      const file = event.target.files[0];
      if (!file) return;
      const url = URL.createObjectURL(file);
      if (type === "new") {
        this.newProduct.image_url = file;
        this.previewNewImage = url;
      } else {
        this.editCache.image_url = file;
        this.previewEditImage = url;
      }
    },
    async submitProduct() {
      const token = localStorage.getItem("token");
      try {
        const formData = new FormData();
        for (const key in this.newProduct) {
          formData.append(key, this.newProduct[key]);
        }
        const res = await axios.post(`${this.baseURL}products/products`, formData, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        });
        this.products.push(res.data);
        this.newProduct = { name: "", description: "", price: "", quantity: "", unit: "", image_url: "" };
        this.previewNewImage = null;
      } catch (err) {
        console.error(err);
      }
    },
    editProduct(product) {
      this.isEditing = product.id;
      this.editCache = { ...product };
    },
    cancelEdit() {
      this.isEditing = null;
      this.editCache = {};
      this.previewEditImage = null;
    },
    async saveEdit(id) {
      const token = localStorage.getItem("token");
      try {
        const formData = new FormData();
        for (const key in this.editCache) {
          formData.append(key, this.editCache[key]);
        }
        const res = await axios.put(`${this.baseURL}products/products/${id}`, formData, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        });
        const index = this.products.findIndex(p => p.id === id);
        this.$set(this.products, index, res.data);
        this.cancelEdit();
      } catch (err) {
        console.error(err);
      }
    },
    async deleteProduct(id) {
      const token = localStorage.getItem("token");
      try {
        await axios.delete(`${this.baseURL}products/products/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.products = this.products.filter(p => p.id !== id);
      } catch (err) {
        console.error(err);
      }
    },
  },
};
</script>

<style scoped>
.container {
  padding: 20px;
}
.heading {
  text-align: center;
  margin-bottom: 30px;
  color: #2f855a;
}
.section {
  margin-bottom: 40px;
}
.sub-heading {
  margin-bottom: 20px;
  font-weight: bold;
  color: #2d3748;
}
.form {
  background: #f7fafc;
  padding: 20px;
  border-radius: 8px;
}
.input-group {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}
.input-group input {
  flex: 1;
  padding: 10px;
  border: 1px solid #cbd5e0;
  border-radius: 4px;
}
.preview-wrapper {
  margin-bottom: 15px;
}
.preview-img {
  max-width: 100px;
  border-radius: 8px;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}
.card {
  background: #edf2f7;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
}
.product-img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 10px;
}
.btn-group {
  margin-top: 10px;
}
.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin: 5px;
}
.primary {
  background-color: #38a169;
  color: white;
}
.success {
  background-color: #48bb78;
  color: white;
}
.danger {
  background-color: #e53e3e;
  color: white;
}
.edit {
  background-color: #3182ce;
  color: white;
}
.download {
  background-color: #805ad5;
  color: white;
}
.empty {
  text-align: center;
  color: #718096;
  font-style: italic;
}
</style>
