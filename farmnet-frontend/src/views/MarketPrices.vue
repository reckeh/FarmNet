<template>
  <div class="market-prices">
    <h1 class="heading">📈 Market Prices Dashboard</h1>

    <!-- Filters -->
    <div class="filters">
      <input v-model="filters.commodity" type="text" placeholder="Product" class="input" />
      <input v-model="filters.county" type="text" placeholder="County" class="input" />
      <input v-model="filters.start_date" type="date" class="input" />
      <input v-model="filters.end_date" type="date" class="input" />
      <button @click="fetchPrices" class="filter-button">Filter</button>
    </div>

    <!-- Table -->
    <div class="table-container">
      <table class="price-table">
        <thead>
          <tr>
            <th>Commodity</th>
            <th>County</th>
            <th>Retail Price</th>
            <th>Wholesale Price</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="price in marketPrices" :key="price.id">
            <td>{{ price.commodity }}</td>
            <td>{{ price.county }}</td>
            <td class="retail">{{ price.retail_price }}</td>
            <td class="wholesale">{{ price.wholesale_price }}</td>
            <td>{{ price.date }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div class="pagination">
      <button
        :disabled="pagination.page <= 1"
        @click="changePage(pagination.page - 1)"
        class="pagination-button"
      >
        ⬅️ Previous
      </button>
      <span>Page {{ pagination.page }} of {{ pagination.pages }}</span>
      <button
        :disabled="pagination.page >= pagination.pages"
        @click="changePage(pagination.page + 1)"
        class="pagination-button"
      >
        Next ➡️
      </button>
    </div>

    <!-- Error -->
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import apiClient from '@/services/api';

export default {
  name: 'MarketPrices',
  data() {
    return {
      marketPrices: [],
      pagination: {
        page: 1,
        pages: 1,
        per_page: 10,
      },
      filters: {
        product: '',
        county: '',
        start_date: '',
        end_date: '',
      },
      error: '',
    };
  },
  methods: {
    async fetchPrices(page = 1) {
      this.error = '';
      const params = {
        ...this.filters,
        page,
        per_page: this.pagination.per_page,
      };

      try {
        const res = await apiClient.get('/prices', { params });
        this.marketPrices = res.data.data;
        this.pagination = {
          page: res.data.pagination.page,
          per_page: res.data.pagination.per_page,
          pages: res.data.pagination.pages,
        };
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to fetch market prices.';
      }
    },
    changePage(newPage) {
      this.fetchPrices(newPage);
    },
  },
  mounted() {
    this.fetchPrices();
  },
};
</script>

<style scoped>
.market-prices {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.heading {
  font-size: 28px;
  font-weight: bold;
  text-align: center;
  color: #2f855a;
  margin-bottom: 24px;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
  margin-bottom: 24px;
}

.input {
  padding: 10px;
  width: 200px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
}

.filter-button {
  background-color: #2f855a;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.filter-button:hover {
  background-color: #276749;
}

.table-container {
  overflow-x: auto;
  margin-bottom: 24px;
}

.price-table {
  width: 100%;
  border-collapse: collapse;
}

.price-table th,
.price-table td {
  border: 1px solid #ccc;
  padding: 12px;
  text-align: center;
}

.price-table th {
  background-color: #e6fffa;
  color: #2d3748;
}

.price-table tr:hover {
  background-color: #f7fafc;
}

.retail {
  color: #2f855a;
  font-weight: bold;
}

.wholesale {
  color: #2b6cb0;
  font-weight: bold;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 16px;
}

.pagination-button {
  padding: 8px 16px;
  border: none;
  background-color: #e2e8f0;
  color: #2d3748;
  border-radius: 6px;
  cursor: pointer;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-button:hover:not(:disabled) {
  background-color: #cbd5e0;
}

.error {
  color: red;
  text-align: center;
  margin-top: 20px;
  font-weight: bold;
}
</style>
