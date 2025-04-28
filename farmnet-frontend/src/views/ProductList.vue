<template>
  <div class="product-list">
    <h1>Product Listings</h1>

    <!-- Filter Options (e.g., Category, Search) -->
    <div class="filters">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="Search products..."
        class="filter-input"
      />
      <select v-model="selectedCategory" class="category-select">
        <option value="">All Categories</option>
        <option v-for="category in categories" :key="category" :value="category">
          {{ category }}
        </option>
      </select>
      <button @click="applyFilters" class="button filter-btn">Apply Filters</button>
    </div>

    <!-- Product List -->
    <div class="products-container">
      <div v-if="loading" class="loading-spinner">Loading...</div>
      <div v-if="filteredProducts.length === 0 && !loading" class="no-products">
        <p>No products found matching your criteria.</p>
      </div>

      <div 
        v-for="product in filteredProducts" 
        :key="product.id" 
        class="product-card"
      >
        <img :src="product.image" alt="Product Image" class="product-image" />
        <div class="product-info">
          <h3>{{ product.name }}</h3>
          <p>{{ product.description }}</p>
          <span class="product-price">${{ product.price.toFixed(2) }}</span>
          <button @click="viewProductDetails(product.id)" class="button view-details-btn">View Details</button>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div class="pagination">
      <button 
        :disabled="currentPage === 1" 
        @click="currentPage--" 
        class="button pagination-btn"
      >
        Previous
      </button>
      <span>Page {{ currentPage }}</span>
      <button 
        :disabled="currentPage === totalPages" 
        @click="currentPage++" 
        class="button pagination-btn"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, computed, onMounted } from 'vue';

export default {
  name: 'ProductList',
  data() {
    return {
      searchQuery: '',
      selectedCategory: '',
      currentPage: 1,
      products: [],
      categories: ['Vegetables', 'Fruits', 'Poultry', 'Dairy', 'Grains'],
      pageSize: 6, // Number of products per page
      loading: true,
    };
  },
  computed: {
    filteredProducts() {
      const filtered = this.products.filter(product => {
        const matchesSearch = product.name.toLowerCase().includes(this.searchQuery.toLowerCase());
        const matchesCategory = this.selectedCategory ? product.category === this.selectedCategory : true;
        return matchesSearch && matchesCategory;
      });

      // Pagination logic
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;

      return filtered.slice(startIndex, endIndex);
    },
    totalPages() {
      return Math.ceil(this.products.length / this.pageSize);
    },
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await axios.get('/products/products');  // Updated API endpoint
        this.products = response.data; // Assuming response data is an array of products
        this.loading = false;
      } catch (error) {
        console.error("Error fetching products:", error);
        this.loading = false;
      }
    },
    applyFilters() {
      this.currentPage = 1; // Reset to first page after applying filters
    },
    viewProductDetails(productId) {
      this.$router.push(`/product/${productId}`);
    },
  },
  onMounted() {
    this.fetchProducts(); // Fetch products when the component is mounted
  },
};
</script>

<style scoped>
.product-list {
  padding: 20px;
}

h1 {
  text-align: center;
  font-size: 36px;
  margin-bottom: 20px;
}

.filters {
  text-align: center;
  margin-bottom: 20px;
}

.filter-input,
.category-select {
  padding: 8px 12px;
  margin-right: 12px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.filter-btn {
  padding: 10px 15px;
  background-color: #4CAF50;
  color: white;
  border-radius: 4px;
  border: none;
}

.products-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.product-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  margin: 10px;
  width: 300px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.product-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

.product-info {
  text-align: center;
  padding-top: 10px;
}

.product-price {
  display: block;
  margin-top: 10px;
  font-size: 18px;
  font-weight: bold;
}

.view-details-btn {
  margin-top: 10px;
  background-color: #007BFF;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.view-details-btn:hover {
  background-color: #0056b3;
}

.no-products {
  text-align: center;
  font-size: 18px;
  color: #888;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.pagination-btn {
  padding: 10px 20px;
  background-color: #007BFF;
  color: white;
  border-radius: 4px;
  border: none;
  margin: 0 10px;
}

.pagination-btn:disabled {
  background-color: #d6d6d6;
  cursor: not-allowed;
}

.loading-spinner {
  text-align: center;
  font-size: 18px;
  color: #4CAF50;
}
</style>
